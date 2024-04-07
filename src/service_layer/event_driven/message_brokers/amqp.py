import aio_pika
import orjson

from infrastructire import amqp, settings
from service_layer.event_driven.message_brokers import protocol


class AMQPMessageBroker:
    def __init__(
        self,
        url: str,
        routing_key: str = None,
        exchange_name: str = None,
    ):
        amqp_settings = settings.Amqp()
        self.publisher = amqp.AMQPPublisher(url=url)
        self.routing_key = routing_key or amqp_settings.EVENTS_ROUTEING_KEY
        self.exchange_name = exchange_name or amqp_settings.EVENTS_EXCHANGE

    async def send_message(self, message: protocol.Message) -> None:
        await self.publisher.publish(
            message=aio_pika.Message(body=orjson.dumps(message.model_dump(mode="json"))),
            exchange_name=self.exchange_name,
            routing_key=self.routing_key,
        )
