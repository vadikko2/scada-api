from service_layer.event_driven import container, middlewares, requests
from service_layer.event_driven.dispatcher import dispatch_result


class DefaultDispatcher:
    def __init__(
        self,
        request_map: requests.RequestMap,
        container: container.Container,
        middleware_chain: middlewares.MiddlewareChain | None = None,
    ) -> None:
        self._request_map = request_map
        self._container = container
        self._middleware_chain = middleware_chain or middlewares.MiddlewareChain()

    async def dispatch(self, request: requests.Request) -> dispatch_result.DispatchResult:
        handler_type = self._request_map.get(type(request))
        handler = await self._container.resolve(handler_type)
        wrapped_handle = self._middleware_chain.wrap(handler.handle)
        response = await wrapped_handle(request)
        return dispatch_result.DispatchResult(response=response, events=handler.events)
