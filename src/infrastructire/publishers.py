import asyncio
import typing

import fastapi
from aio_pika import abc
from orjson import orjson

M = typing.TypeVar("M")
C = typing.TypeVar("C")


class EventPublisher(typing.Generic[C]):
    channel: C

    def __init__(self, channel: C):
        self.channel = channel

    async def publish(self, message: M) -> None:
        """Публикует события в канал. При необходимости делает необходимую обработку."""


class FromAmqpToWebsocketPublisher(EventPublisher[fastapi.WebSocket]):
    channel: fastapi.WebSocket
    heartbeat: asyncio.Task | None = None

    async def publish(self, message: abc.AbstractIncomingMessage) -> None:
        message_body = orjson.loads(message.body)

        if message_body.get("type") == "state":
            self.heartbeat.cancel()
        payload = message_body.get("payload")
        if not payload:
            return
        await self.channel.send_json(payload)
