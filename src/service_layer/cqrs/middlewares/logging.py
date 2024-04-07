import logging
import typing

from infrastructire import logging as log
from service_layer.cqrs import requests, response

Req = typing.TypeVar("Req", bound=requests.Request, contravariant=True)
Res = typing.TypeVar("Res", response.Response, None, covariant=True)
HandleType = typing.Callable[[Req], typing.Awaitable[Res]]


class LoggingMiddleware:
    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or log.logger

    async def __call__(self, request: Req, handle: HandleType) -> Res:
        self._logger.debug(
            "Handle %s request",
            type(request).__name__,
            extra={
                "request_json_fields": {"request": request.model_dump(mode="json")},
                "to_mask": True,
            },
        )
        r = await handle(request)
        self._logger.debug(
            "Request %s handled",
            type(request).__name__,
            extra={
                "request_json_fields": {"response": r.model_dump(mode="json") if r else {}},
                "to_mask": True,
            },
        )

        return r
