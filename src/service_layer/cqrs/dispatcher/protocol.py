import typing

from service_layer.cqrs import requests
from service_layer.cqrs.dispatcher import dispatch_result


class Dispatcher(typing.Protocol):
    async def dispatch(self, request: requests.Request) -> dispatch_result.DispatchResult:
        ...
