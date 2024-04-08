import abc
import contextlib
import typing

from sqlalchemy.ext.asyncio import session as sql_session

from infrastructire import factories, repository

R = typing.TypeVar("R", bound=repository.Repository, contravariant=True)
S = typing.TypeVar("S", contravariant=True)
TEvent = typing.TypeVar("TEvent")


class UoW(typing.Generic[R, S], abc.ABC):
    session: S
    repository: R

    def __init__(
        self,
        repository_factory: factories.RepositoryFactory[S],
        session_factory: factories.SessionFactory[S],
    ):
        self.repository_factory = repository_factory
        self.session_factory = session_factory

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.Self:
        self.session = self.session_factory()
        try:
            self.repository = self.repository_factory(self.session)
            yield self
        finally:
            await self._close()

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...

    @abc.abstractmethod
    async def _close(self):
        ...


class SQLAlchemyUoW(UoW[repository.SQLAlchemyRepository, sql_session.AsyncSession]):
    async def commit(self):
        try:
            await self.session.commit()
        except Exception:
            await self.rollback()
            raise

    async def rollback(self):
        await self.session.rollback()

    async def _close(self):
        session = getattr(self, "session", None)
        if session:
            await session.close()
