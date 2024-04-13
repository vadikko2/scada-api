import functools
import uuid

import fastapi

from infrastructire import consumers, settings
from service_layer import bootstrap, cqrs
from service_layer.handlers import subscriptions


@functools.lru_cache
def inject_mediator() -> cqrs.Mediator:
    return bootstrap.bootstrap()


def inject_publisher(mediator: cqrs.Mediator = fastapi.Depends(inject_mediator)):
    return subscriptions.NestIndicatorValuesPublisher(mediator=mediator)


def inject_consumer() -> consumers.EventConsumer:
    amqp_settings = settings.Amqp()
    session_guid = uuid.uuid4()
    queue_name = f"{amqp_settings.EVENTS_QUEUE}-{session_guid}"
    return consumers.AMQPConsumer(
        url=str(amqp_settings.dsn),
        exchange_name=amqp_settings.EVENTS_EXCHANGE,
        routing_key=amqp_settings.EVENTS_ROUTEING_KEY,
        queue_name=queue_name,
    )
