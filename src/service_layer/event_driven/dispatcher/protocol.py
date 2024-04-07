import typing

from service_layer.event_driven import requests
from service_layer.event_driven.dispatcher import dispatch_result


class Dispatcher(typing.Protocol):
    async def dispatch(self, request: requests.Request) -> dispatch_result.DispatchResult: ...
