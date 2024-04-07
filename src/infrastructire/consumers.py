import typing

M = typing.TypeVar("M")


class EventConsumer:
    async def consume(self, on_message: typing.Callable[[M], typing.Awaitable[None]]):
        pass
