import typing

import di
from di import dependent, executors

from service_layer.cqrs import container

T = typing.TypeVar("T")


class DIContainer(container.Container[di.Container]):
    def __init__(self) -> None:
        self._external_container: di.Container | None = None

    @property
    def external_container(self) -> di.Container:
        if not self._external_container:
            raise AttributeError

        return self._external_container

    def attach_external_container(self, container: di.Container) -> None:
        self._external_container = container

    async def resolve(self, type_: typing.Type[T]) -> T:
        executor = executors.AsyncExecutor()
        solved = self.external_container.solve(dependent.Dependent(type_, scope="request"), scopes=["request"])
        with self.external_container.enter_scope("request") as state:
            return await solved.execute_async(executor=executor, state=state)
