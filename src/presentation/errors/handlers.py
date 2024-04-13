"""
Используется для представления обработчиков ошибок FastAPI,
которые отправляются автоматически движком fastapi.
"""

import functools
import inspect
import typing

import decohints
import pydantic
from fastapi import responses
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request

from domain import exceptions
from presentation.errors.registry import register_exception
from presentation.models.responses import ErrorResponse, ErrorResponseMulti

__all__ = (
    "pydantic_request_validation_errors_handler",
    "not_found_handler",
    "already_exists_handler",
    "python_base_error_handler",
)


@decohints.decohints
def bind_exception(status_code: int, response_model: typing.Type[pydantic.BaseModel]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        spec = inspect.getfullargspec(func)
        exc = spec.annotations.get(spec.args[1])
        register_exception(exc, status_code, response_model)

        return wrapper

    return decorator


@bind_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, response_model=ErrorResponse)
def python_base_error_handler(_: Request, error: Exception) -> responses.JSONResponse:
    response = ErrorResponseMulti(results=[ErrorResponse(message=f"Unhandled error: {error}")])

    return responses.JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@bind_exception(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, response_model=ErrorResponseMulti)
def pydantic_request_validation_errors_handler(_: Request, error: RequestValidationError) -> responses.JSONResponse:
    """This function is called if the Pydantic validation error was raised."""

    response = ErrorResponseMulti(
        results=[
            ErrorResponse(
                message=err["msg"],
                path=list(err["loc"]),
            )
            for err in error.errors()
        ]
    )

    return responses.JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@bind_exception(status_code=status.HTTP_404_NOT_FOUND, response_model=ErrorResponse)
def not_found_handler(_: Request, error: exceptions.NotFound) -> responses.JSONResponse:
    response = ErrorResponse(message=error.message)

    return responses.JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_404_NOT_FOUND,
    )


@bind_exception(status_code=status.HTTP_409_CONFLICT, response_model=ErrorResponse)
def already_exists_handler(_: Request, error: exceptions.AlreadyExists) -> responses.JSONResponse:
    response = ErrorResponse(message=error.message, path=error.path)

    return responses.JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_409_CONFLICT,
    )
