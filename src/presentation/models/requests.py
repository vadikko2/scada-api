import typing

import pydantic

from service_layer.models import commands, queries

C = typing.TypeVar("C", bound=commands.Command, covariant=True)
Q = typing.TypeVar("Q", bound=queries.Query, covariant=True)


class CommandRequest(pydantic.BaseModel, typing.Generic[C]):
    body: C


class QueryRequest(pydantic.BaseModel, typing.Generic[Q]):
    body: Q
