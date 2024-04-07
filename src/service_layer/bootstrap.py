import typing

import di

from infrastructire import settings
from service_layer import cqrs, dependencies
from service_layer.cqrs import events, requests
from service_layer.cqrs.container import di as ed_di_container
from service_layer.cqrs.message_brokers import amqp, protocol
from service_layer.cqrs.middlewares import base as mediator_middlewares
from service_layer.cqrs.middlewares import logging as logging_middleware
from service_layer.handlers import commands as command_handlers
from service_layer.handlers import queries as query_handlers
from service_layer.models import commands, queries


def init_commands(mapper: requests.RequestMap):
    """Инициализирует обработчики команд"""
    mapper.bind(commands.CreateHolder, command_handlers.CreateHolderHandler)
    mapper.bind(commands.UpdateTechNestIndicators, command_handlers.UpdateTechNestIndicatorsHandler)
    mapper.bind(commands.UpdateDeviceIndicators, command_handlers.UpdatedDeviceIndicatorsHandler)


def init_events(mapper: events.EventMap):
    """Инициализирует обработчики событий"""


def init_queries(mapper: requests.RequestMap):
    """Инициализирует обработчики запросов"""
    mapper.bind(queries.TechNests, query_handlers.GetTechNestsHandler)
    mapper.bind(queries.Devices, query_handlers.GetDevicesHandler)


def setup_mediator(
    message_broker: protocol.MessageBroker,
    external_container: di.Container,
    middlewares: typing.Iterable[mediator_middlewares.Middleware] | None = None,
    commands_mapper: typing.Callable[[requests.RequestMap], None] = init_commands,
    events_mapper: typing.Callable[[events.EventMap], None] = init_events,
    queries_mapper: typing.Callable[[requests.RequestMap], None] = init_queries,
) -> cqrs.Mediator:
    container = ed_di_container.DIContainer()
    container.attach_external_container(external_container)

    event_mapper = events.EventMap()
    requests_mapper = requests.RequestMap()

    commands_mapper(requests_mapper)
    events_mapper(event_mapper)
    queries_mapper(requests_mapper)

    event_emitter = events.EventEmitter(
        event_map=event_mapper,
        container=container,
        message_broker=message_broker,
    )
    middleware_chain = mediator_middlewares.MiddlewareChain()
    if middlewares is None:
        middlewares = []

    for middleware in middlewares:
        middleware_chain.add(middleware)

    return cqrs.Mediator(
        event_emitter=event_emitter,
        request_map=requests_mapper,
        container=container,
        middleware_chain=middleware_chain,
    )


DEFAULT_MESSAGE_BROKER = amqp.AMQPMessageBroker(settings.get_amqp_url())


def bootstrap(
    message_broker: protocol.MessageBroker | None = None,
    di_container: di.Container | None = None,
    middlewares: typing.Iterable[mediator_middlewares.Middleware] | None = None,
    commands_mapper: typing.Callable[[requests.RequestMap], None] = init_commands,
    events_mapper: typing.Callable[[events.EventMap], None] = init_events,
    queries_mapper: typing.Callable[[requests.RequestMap], None] = init_queries,
) -> cqrs.Mediator:
    if message_broker is None:
        message_broker = DEFAULT_MESSAGE_BROKER
    if di_container is None:
        di_container = dependencies.container
    if middlewares is None:
        middlewares = []
    return setup_mediator(
        message_broker,
        di_container,
        middlewares=middlewares + [logging_middleware.LoggingMiddleware()],
        commands_mapper=commands_mapper,
        events_mapper=events_mapper,
        queries_mapper=queries_mapper,
    )
