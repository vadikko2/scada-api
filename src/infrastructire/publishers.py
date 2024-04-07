import asyncio
import functools
import typing

import aio_pika
import fastapi
from aio_pika import abc, pool
from orjson import orjson

from infrastructire import factories

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


class AMQPPublisher:
    def __init__(self, url: str, max_connection_pool_size=2, max_channel_pool_size=10):
        self.url = url
        self.max_connection_pool_size = max_connection_pool_size
        self.max_channel_pool_size = max_channel_pool_size
        self.connection_pool: pool.Pool = pool.Pool(
            functools.partial(factories.amqp_connection_pool_factory, url=url),
            max_size=self.max_connection_pool_size,
        )
        self.channel_pool: pool.Pool = pool.Pool(
            functools.partial(factories.amqp_channel_pool_factory, connection_pool=self.connection_pool),
            max_size=self.max_channel_pool_size,
        )

    async def publish(self, message: abc.AbstractMessage, routing_key: str, exchange_name: str) -> None:
        async with self.channel_pool.acquire() as channel:
            exchange: aio_pika.Exchange = await channel.declare_exchange(exchange_name, type="topic", auto_delete=False)
            await exchange.publish(message=message, routing_key=routing_key)
