import abc
import typing
import uuid

import sqlalchemy

from domain import models
from sqlalchemy.ext.asyncio import session as sql_session

N = typing.TypeVar("N", bound=models.TechNest, contravariant=True)
L = typing.TypeVar("L", bound=models.TechNestLocation, contravariant=True)
H = typing.TypeVar("H", bound=models.Company, contravariant=True)
D = typing.TypeVar("D", bound=models.Device, contravariant=True)


class Repository(abc.ABC):

    @abc.abstractmethod
    async def add_holder(self, item: H) -> None:
        pass

    @abc.abstractmethod
    async def add_nest(self, item: N) -> None:
        pass

    @abc.abstractmethod
    async def add_device(self, item: D) -> None:
        pass

    @abc.abstractmethod
    async def get_holder(self, holder: int) -> H:
        pass

    @abc.abstractmethod
    async def get_nests_by_holder(self, holder: int) -> list[N]:
        pass

    @abc.abstractmethod
    async def get_nests_by_location(self, location: int) -> list[N]:
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, session: sql_session.AsyncSession):
        self.session = session

    async def add_holder(self, item: H) -> None:
        self.session.add(item)

    async def add_nest(self, item: N) -> None:
        pass

    async def add_device(self, item: D) -> None:
        pass

    async def get_holder(self, holder: int) -> H:
        pass

    async def get_nests_by_holder(self, holder: int) -> list[N]:
        nests = await self.session.execute(sqlalchemy.select(models.TechNest).filter_by(holder=holder))
        return nests.scalar().all()

    async def get_nests_by_location(self, location: int) -> list[N]:
        pass
