import functools
import typing
import uuid

import fastapi

from infrastructire import consumers, publishers, settings
from service_layer import bootstrap, cqrs


@functools.lru_cache
def inject_mediator() -> cqrs.Mediator:
    return bootstrap.bootstrap()


def get_consumer() -> consumers.EventConsumer:
    amqp_settings = settings.Amqp()
    session_guid = uuid.uuid4()
    queue_name = f"{amqp_settings.EVENTS_QUEUE}-{session_guid}"
    return consumers.AMQPConsumer(
        url=str(amqp_settings.dsn),
        exchange_name=amqp_settings.EVENTS_EXCHANGE,
        routing_key=amqp_settings.EVENTS_ROUTEING_KEY,
        queue_name=queue_name,
    )


def get_publisher_type() -> typing.Type[publishers.EventPublisher[fastapi.WebSocket]]:
    return publishers.FromAmqpToWebsocketPublisher
