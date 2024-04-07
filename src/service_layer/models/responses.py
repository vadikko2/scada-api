import pydantic

from domain import models

from service_layer.event_driven import response
from service_layer.models import validation


class TechNests(response.Response):
    """Коллекция технических узлов"""

    tech_nests: list[models.TechNest]


class Holder(models.Company, response.Response):
    """Данные о владельце технического узла"""


class HolderCreated(response.Response):
    id: int = validation.IdField(description="Идентификатор владельца технического узла")


class TechNestAdded(response.Response):
    id: int = validation.IdField(description="Идентификатор технического узла")


class DeviceAdded(response.Response):
    id: int = validation.IdField(description="Идентификатор устройства")
