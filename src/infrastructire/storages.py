import abc
import typing

from orjson import orjson

from domain import models
from infrastructire import factories

V = typing.TypeVar("V", covariant=True)


class IndicatorValuesStorage(typing.Generic[V], abc.ABC):
    @abc.abstractmethod
    async def set_value(self, id: int, value: V) -> None:
        pass

    @abc.abstractmethod
    async def get_value(self, id: int) -> V | None:
        pass

    @abc.abstractmethod
    async def get_values(self, *id: int) -> list[V]:
        pass


class TechNestIndicatorValuesStorage(IndicatorValuesStorage[models.TechNestIndicatorsValues], abc.ABC):
    pass


class DeviceIndicatorValuesStorage(IndicatorValuesStorage[models.DeviceIndicatorsValues], abc.ABC):
    pass


class RedisTechNestIndicatorValuesStorage(TechNestIndicatorValuesStorage):
    PREFIX = "nest@{}"

    def __init__(self, client_factory: factories.RedisClientFactory):
        self.client = client_factory()

    async def set_value(self, id: int, value: models.TechNestIndicatorsValues):
        key = self.PREFIX.format(id)
        await self.client.set(key, orjson.dumps(value.model_dump(mode="json")))

    async def get_value(self, id: int) -> models.TechNestIndicatorsValues | None:
        key = self.PREFIX.format(id)
        value = await self.client.get(key)
        if not value:
            return
        return models.TechNestIndicatorsValues.model_validate(orjson.loads(value), context={"assume_validated": True})

    async def get_values(self, *id: int) -> list[V]:
        keys = list(map(self.PREFIX.format, id))
        values = await self.client.mget(keys)
        return list(
            map(
                lambda v: models.TechNestIndicatorsValues.model_validate(
                    orjson.loads(v), context={"assume_validated": True}
                ),
                values,
            )
        )


class RedisDeviceIndicatorValuesStorage(TechNestIndicatorValuesStorage):
    PREFIX = "device@{}"

    def __init__(self, client_factory: factories.RedisClientFactory):
        self.client = client_factory()

    async def set_value(self, id: int, value: models.DeviceIndicatorsValues):
        key = self.PREFIX.format(id)
        await self.client.set(key, orjson.dumps(value.model_dump(mode="json")))

    async def get_value(self, id: int) -> models.DeviceIndicatorsValues | None:
        key = self.PREFIX.format(id)
        value = await self.client.get(key)
        if not value:
            return
        return models.DeviceIndicatorsValues.model_validate(orjson.loads(value), context={"assume_validated": True})

    async def get_values(self, *id: int) -> list[V]:
        keys = list(map(self.PREFIX.format, id))
        values = await self.client.mget(keys)
        return list(
            map(
                lambda v: models.DeviceIndicatorsValues.model_validate(
                    orjson.loads(v), context={"assume_validated": True}
                ),
                values,
            )
        )
