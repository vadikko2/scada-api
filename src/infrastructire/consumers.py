import asyncio
import functools
import typing

from aio_pika import abc, pool

from infrastructire import factories, logging

M = typing.TypeVar("M")


class EventConsumer:
    async def consume(self, on_message: typing.Callable[[M], typing.Awaitable[None]]):
        pass


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
            functools.partial(factories.amqp_connection_pool_factory, url=url),
            max_size=self.max_connection_pool_size,
        )
        self.channel_pool: pool.Pool = pool.Pool(
            functools.partial(factories.amqp_channel_pool_factory, connection_pool=self.connection_pool),
            max_size=self.max_channel_pool_size,
        )

    async def consume(self, on_message: typing.Callable[[abc.AbstractIncomingMessage], typing.Awaitable[None]]):
        async with self.channel_pool.acquire() as channel:
            await channel.set_qos(prefetch_count=1)
            exchange = await channel.declare_exchange(self.exchange_name, type="topic")
            queue = await channel.declare_queue(self.queue_name, auto_delete=True)
            await queue.bind(exchange, self.routing_key)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    logging.logger.debug(f"Got message {message} from queue {self.queue_name}")
                    await on_message(message)
                    await message.ack()
