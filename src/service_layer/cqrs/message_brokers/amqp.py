import aio_pika
import orjson

from infrastructire import publishers, settings
from service_layer.cqrs.message_brokers import protocol


class AMQPMessageBroker:
    def __init__(
        self,
        url: str,
        routing_key: str = None,
        exchange_name: str = None,
    ):
        amqp_settings = settings.Amqp()
        self.publisher = publishers.AMQPPublisher(
            url=url,
            routing_key=routing_key or amqp_settings.EVENTS_ROUTEING_KEY,
            exchange_name=exchange_name or amqp_settings.EVENTS_EXCHANGE,
        )

    async def send_message(self, message: protocol.Message) -> None:
        await self.publisher.__call__(message=aio_pika.Message(body=orjson.dumps(message.model_dump(mode="json"))))
