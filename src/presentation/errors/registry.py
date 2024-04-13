import types
import typing

import pydantic

from service_layer.cqrs import registry

Ex = typing.TypeVar("Ex", bound=typing.Type[Exception])
S = typing.TypeVar("S", bound=typing.Dict[int, typing.Dict])


__exception_registry = types.new_class("ExceptionRegistry", (registry.InMemoryRegistry[Ex, S],), {})()


def register_exception(exc: Ex, status_code: int, response_model: typing.Type[pydantic.BaseModel]):
    __exception_registry[exc] = {
        status_code: {
            "model": response_model,
            "description": exc.__doc__,
        }
    }


def get_exception_responses(*exceptions: Ex) -> S:
    result = {}
    for exc in exceptions:
        result.update(__exception_registry[exc])
    return result
