import aio_pika
import orjson

from infrastructire import amqp
from service_layer.event_driven.message_brokers import protocol


class AMQPMessageBroker:
    def __init__(
        self,
        url: str,
        queue_name: str = "configurations_events",
        exchange_name: str = "configurations",
    ):
        self.publisher = amqp.AMQPPublisher(url=url)
        self.queue_name = queue_name
        self.exchange_name = exchange_name

    async def send_message(self, message: protocol.Message) -> None:
        await self.publisher.publish(
            message=aio_pika.Message(body=orjson.dumps(message.model_dump(mode="json"))),
            exchange_name=self.exchange_name,
            queue_name=self.queue_name,
        )
