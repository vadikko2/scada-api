import decimal

import pydantic

from domain import models
from service_layer.event_driven import requests
from service_layer.models import validation


class Command(requests.Request):
    """Базовый класс команды"""


class CreateHolder(Command):
    name: str = pydantic.Field(description="Наименование организации")
    inn: int = pydantic.Field(description="ИНН организации")
    kpp: int = pydantic.Field(description="КПП организации")


class AddTechNest(Command):
    holder: int = validation.IdField(description="Владелец технического узла")
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    address: str


class AddDevice(Command):
    tech_nest: int = validation.IdField(description="Идентификатор технического узла")
    name: str = pydantic.Field(description="Наименование устройства")
    model: str | None = pydantic.Field(description="Модель устройства", default=None)


class UpdateTechNestIndicators(Command, models.TechNestIndicators):
    pass


class UpdateDeviceIndicators(Command, models.DeviceIndicators):
    pass
