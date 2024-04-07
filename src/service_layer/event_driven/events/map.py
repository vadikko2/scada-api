import collections
import typing

from service_layer.event_driven import registry
from service_layer.event_driven.events import event, event_handler

E = typing.TypeVar("E", bound=event.DomainEvent, contravariant=True)


class EventMap(registry.InMemoryRegistry[typing.Type[E]], list[typing.Type[event_handler.EventHandler]]):
    _registry: collections.defaultdict

    def __init__(self) -> None:
        super().__init__()
        self._registry = collections.defaultdict(list)

    def bind(self, event_type: typing.Type[E], handler_type: typing.Type[event_handler.EventHandler[E]]) -> None:
        self[event_type].append(handler_type)

    def get(self, event_type: typing.Type[E]) -> list[typing.Type[event_handler.EventHandler[E]]]:
        return self._registry[event_type]

    def get_events(self) -> list[typing.Type[E]]:
        return list(self.keys())

    def __str__(self) -> str:
        return str(self._registry)
