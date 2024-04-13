from aio_pika import abc

from infrastructire import publishers
from service_layer import cqrs


class NestIndicatorValuesPublisher(publishers.AbstractFromAmqpToWebsocketPublisher):
    def __init__(self, mediator: cqrs.Mediator):
        self.mediator = mediator

    async def __call__(self, message: abc.AbstractIncomingMessage) -> None:
        payload = self.extract_payload(message)
        if payload is None:
            return
        await self.channel.send_json(payload)
