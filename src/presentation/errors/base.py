"""
Отвечает за описание общих ошибок,
которые обрабатываются на последнем этапе обработки запроса.
"""

import typing

__all__ = (
    "BaseError",
    "BadRequestError",
    "UnprocessableError",
    "NotFoundError",
    "DatabaseError",
    "AuthenticationError",
    "AuthorizationError",
)

from starlette import status


class BaseError(Exception):
    def __init__(
        self,
        *_: typing.Tuple[typing.Any],
        message: typing.Text = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.message: typing.Text = message
        self.status_code: int = status_code

        super().__init__(message)


class BadRequestError(BaseError):
    def __init__(self, *_: typing.Tuple[typing.Any], message: typing.Text = "Bad request") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnprocessableError(BaseError):
    def __init__(self, *_: typing.Tuple[typing.Any], message: typing.Text = "Validation error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class NotFoundError(BaseError):
    def __init__(self, *_: typing.Tuple[typing.Any], message: typing.Text = "Not found") -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class DatabaseError(BaseError):
    def __init__(self, *_: tuple[typing.Any], message: typing.Text = "Database error") -> None:
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthenticationError(BaseError):
    def __init__(self, *_: typing.Tuple[typing.Any], message: typing.Text = "Authentication error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(BaseError):
    def __init__(self, *_: typing.Tuple[typing.Any], message: typing.Text = "Authorization error") -> None:
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)
