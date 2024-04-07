import datetime
import json
import sys
import types
import typing
import logging
from logging import config

import loguru
import pydantic
import stackprinter

from infrastructire import settings

LEVEL_TO_NAME = {
    logging.CRITICAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARNING",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "NOTSET",
}


class BaseJsonLogSchema(pydantic.BaseModel):
    """
    Main log in JSON format
    """

    thread: typing.Union[int, str]
    level_name: str
    message: str
    source_log: str
    timestamp: str
    app_name: str
    app_version: str
    # app_env: str
    duration: int
    exceptions: typing.Union[typing.List[str], str] = None
    trace_id: str = None
    span_id: str = None
    parent_id: str = None

    model_config = pydantic.ConfigDict(populate_by_name=True)


class ConsoleLogger(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = typing.cast(types.FrameType, frame.f_back)
            depth += 1
        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class JSONLogFormatter(logging.Formatter):
    """
    Custom class-formatter for writing logs to json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Formating LogRecord to json

        :param record: logging.LogRecord
        :return: json string
        """
        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        now = datetime.datetime.fromtimestamp(record.created).astimezone().replace(microsecond=0).isoformat()
        message = record.getMessage()
        duration = record.duration if hasattr(record, "duration") else record.msecs

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level_name=LEVEL_TO_NAME[record.levelno],
            message=message,
            source_log=record.name,
            duration=duration,
            app_name=settings.app_name,
            app_version=settings.version,
        )

        if hasattr(record, "props"):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields.exceptions = (
                # default library traceback
                # traceback.format_exception(*record.exc_info)
                # stackprinter gets all debug information
                # https://github.com/cknd/stackprinter/blob/master/stackprinter/__init__.py#L28-L137
                stackprinter.format(
                    record.exc_info,
                    suppressed_paths=[
                        r"lib/python.*/site-packages/starlette.*",
                    ],
                    add_summary=False,
                ).split("\n")
            )

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        # Pydantic to dict
        json_log_object = json_log_fields.dict(
            exclude_unset=True,
            by_alias=True,
        )
        # getting additional fields
        if hasattr(record, "request_json_fields"):
            json_log_object.update(record.request_json_fields)

        return json_log_object


def handlers():
    return ["json"] if settings.logging_settings.SERIALIZE else ["intercept"]


LOG_HANDLER = handlers()
LOGGING_LEVEL = settings.logging_settings.LEVEL

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JSONLogFormatter,
        },
    },
    "handlers": {
        "json": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "intercept": {
            "()": ConsoleLogger,
        },
    },
    "loggers": {
        "main": {
            "handlers": LOG_HANDLER,
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": LOG_HANDLER,
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": LOG_HANDLER,
            "level": "ERROR",
            "propagate": False,
        },
    },
}


config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("main")
