import decimal

import petrovna
import pydantic

from domain import models
from service_layer.cqrs import requests
from service_layer.models import validation


class Command(requests.Request):
    """Базовый класс команды"""


class CreateHolder(Command):
    name: str = models.HolderNameField()
    inn: str = models.INN()
    kpp: str | None = models.KPP()

    @pydantic.field_validator("inn")
    @classmethod
    def inn_validator(cls, v: str) -> str:
        if not petrovna.validate_inn(v):
            raise ValueError("Invalid INN value")
        return v

    @pydantic.field_validator("kpp")
    @classmethod
    def kpp_validator(cls, v: str | None) -> str | None:
        if v and not petrovna.validate_kpp(v):
            raise ValueError("Invalid KPP value")
        return v


class AddTechNest(Command):
    holder: int = validation.IdField(description="Владелец технического узла")
    name: str = models.TechNestNameField()
    latitude: decimal.Decimal = models.LatitudeField()
    longitude: decimal.Decimal = models.LongitudeField()
    address: str = models.AddressField()


class AddDevice(Command):
    nest: int = validation.IdField(description="Идентификатор технического узла")
    name: str = models.DeviceNameField()
    model: str | None = models.DeviceModelField()


class UpdateTechNestIndicators(Command, models.TechNestIndicators):
    pass


class UpdateDeviceIndicators(Command, models.DeviceIndicators):
    pass


class PublishTargetIndicators(Command):
    """
    Команда на публикацию текущих значений индикаторов технического узла и устройств на нем
    """

    nest: int = validation.IdField(description="Идентификатор технического узла")
