import typing

from service_layer.event_driven import container, dispatcher, events, middlewares, requests, response

Req = typing.TypeVar("Req", bound=requests.Request, contravariant=True)
Resp = typing.TypeVar("Resp", bound=response.Response, covariant=True)
E = typing.TypeVar("E", bound=events.Event, contravariant=True)


class Mediator:
    """
    The main mediator object.

    Usage::

      redis_client = Redis()  # async redis client
      message_broker = RedisMessageBroker(redis_client)
      event_map = EventMap()
      event_map.bind(UserJoinedDomainEvent, UserJoinedDomainEventHandler)
      request_map = RequestMap()
      request_map.bind(JoinUserCommand, JoinUserCommandHandler)
      event_emitter = EventEmitter(event_map, container, message_broker)

      mediator = Mediator(
        event_emitter=event_emitter,
        request_map=request_map,
        container=container
      )

      # Handles command and published events by the command handler.
      await mediator.send(join_user_command)

    """

    def __init__(
        self,
        request_map: requests.RequestMap,
        container: container.Container,
        event_emitter: events.EventEmitter | None = None,
        middleware_chain: middlewares.MiddlewareChain | None = None,
        *,
        dispatcher_type: typing.Type[dispatcher.Dispatcher] = dispatcher.DefaultDispatcher,
    ) -> None:
        self._event_emitter = event_emitter
        self._dispatcher = dispatcher_type(
            request_map=request_map, container=container, middleware_chain=middleware_chain  # type: ignore
        )

    async def send(self, request: Req) -> Resp | None:
        dispatch_result = await self._dispatcher.dispatch(request)

        if dispatch_result.events:
            await self._send_events(dispatch_result.events.copy())

        return dispatch_result.response

    async def _send_events(self, events: list[E]) -> None:
        if not self._event_emitter:
            return

        while events:
            event = events.pop()
            await self._event_emitter.emit(event)
