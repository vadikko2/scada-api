import abc
import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import session as sql_session
from sqlalchemy.orm import joinedload

from domain import models
from infrastructire import orm

N = typing.TypeVar("N", bound=models.TechNest, contravariant=True)
L = typing.TypeVar("L", bound=models.TechNestLocation, contravariant=True)
H = typing.TypeVar("H", bound=models.Holder, contravariant=True)
D = typing.TypeVar("D", bound=models.Device, contravariant=True)


class Repository(abc.ABC):
    @abc.abstractmethod
    async def add_holder(self, item: H) -> int:
        pass

    @abc.abstractmethod
    async def add_nest(self, item: N) -> int:
        pass

    @abc.abstractmethod
    async def add_device(self, item: D) -> int:
        pass

    @abc.abstractmethod
    async def get_holder(self, holder: int) -> H | None:
        pass

    @abc.abstractmethod
    async def get_nests_by_holder(self, holder: int) -> list[N]:
        pass

    @abc.abstractmethod
    async def get_nests_by_location(self, location: int) -> list[N]:
        pass

    @abc.abstractmethod
    async def get_devices(self, nest: int) -> list[D]:
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, session: sql_session.AsyncSession):
        self.session = session

    async def add_holder(self, item: H) -> int:
        holder_orm = orm.Company(**item.model_dump(mode="json"))
        self.session.add(holder_orm)
        await self.session.flush()
        return holder_orm.id

    async def add_nest(self, item: N) -> int:
        item_dict = item.model_dump(mode="json")
        item_dict.pop("location")
        item_dict.pop("devices")
        location_orm = orm.Locations(**item.location.model_dump(mode="json"))
        item_dict["location"] = location_orm
        nest_orm = orm.TechNest(**item_dict)
        self.session.add(nest_orm)
        await self.session.flush()
        return nest_orm.id

    async def add_device(self, item: D) -> int:
        orm_device = orm.Devices(**item.model_dump(mode="json"))
        self.session.add(orm_device)
        await self.session.flush()
        return orm_device.id

    async def get_holder(self, holder: int) -> H:
        result = await self.session.execute(sqlalchemy.select(orm.Company).filter_by(id=holder))
        return models.Holder.model_validate(result.scalar())

    async def get_nests_by_holder(self, holder: int) -> list[N]:
        nests_result = await self.session.execute(
            sqlalchemy.select(orm.TechNest).filter_by(holder_id=holder).options(joinedload("*"))
        )
        nests = nests_result.unique().scalars().all()
        return list(map(models.TechNest.model_validate, nests))

    async def get_nests_by_location(self, location: int) -> list[N]:
        pass

    async def get_devices(self, nest: int) -> list[D]:
        devices = await self.session.execute(sqlalchemy.select(orm.Devices).filter_by(nest_id=nest))
        devices = devices.scalars().all()
        return list(map(models.Device.model_validate, devices))
