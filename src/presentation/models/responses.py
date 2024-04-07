import typing

import pydantic
from service_layer.event_driven import response

__all__ = (
    "ResponseMulti",
    "Response",
    "ErrorResponse",
    "ErrorResponseMulti",
)


R = typing.TypeVar("R", bound=response.Response)


class ResponseMulti(pydantic.BaseModel, typing.Generic[R]):
    """Generic response model that consist multiple results."""

    result: typing.List[R]


class Response(pydantic.BaseModel, typing.Generic[R]):
    """Generic response model that consist only one result."""

    result: R


class ErrorResponse(pydantic.BaseModel):
    """Error response model."""

    message: typing.Text = pydantic.Field(description="This field represent the message")
    path: typing.List = pydantic.Field(
        description="The path to the field that raised the error",
        default_factory=list,
    )


class ErrorResponseMulti(pydantic.BaseModel):
    """The public error response model that includes multiple objects."""

    results: pydantic.conlist(ErrorResponse, min_length=1)
