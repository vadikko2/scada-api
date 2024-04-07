import typing

M = typing.TypeVar("M")
C = typing.TypeVar("C")


class EventPublisher(typing.Generic[C]):
    channel: C

    def __init__(self, channel: C):
        self.channel = channel

    async def publish(self, message: M) -> None:
        """Публикует события в канал. При необходимости делает необходимую обработку."""
