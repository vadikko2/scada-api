import asyncio
import typing
from functools import partial

from aio_pika import Channel, abc, connect_robust, pool

M = typing.TypeVar("M")


class EventConsumer:
    async def consume(self, on_message: typing.Callable[[M], typing.Awaitable[None]]):
        pass


async def connection_pool_factory(url: str) -> abc.AbstractRobustConnection:
    return await connect_robust(url=url)


async def channel_pool_factory(connection_pool: pool.Pool) -> Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


class AMQPConsumer(EventConsumer):
    def __init__(
        self,
        url: str,
        exchange_name: str,
        routing_key: str,
        queue_name: str,
        max_connection_pool_size=2,
        max_channel_pool_size=10,
    ):
        self.url = url
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.queue_name = queue_name
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.max_connection_pool_size = max_connection_pool_size
        self.max_channel_pool_size = max_channel_pool_size
        self.connection_pool: pool.Pool = pool.Pool(
            partial(connection_pool_factory, url=url),
            max_size=self.max_connection_pool_size,
        )
        self.channel_pool: pool.Pool = pool.Pool(
            partial(channel_pool_factory, connection_pool=self.connection_pool),
            max_size=self.max_channel_pool_size,
        )

    async def consume(self, on_message: typing.Callable[[abc.AbstractIncomingMessage], typing.Awaitable[None]]):
        async with self.channel_pool.acquire() as channel:
            await channel.set_qos(prefetch_count=1)
            exchange = await channel.declare_exchange(self.exchange_name, type="topic")
            queue = await channel.declare_queue(self.queue_name, auto_delete=False)
            await queue.bind(exchange, self.routing_key)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await on_message(message)
