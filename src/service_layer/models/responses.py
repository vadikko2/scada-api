import pydantic

from domain import models
from service_layer.cqrs import response
from service_layer.models import validation


class Holder(models.Company, response.Response):
    """Данные о владельце технического узла"""


class TechNests(response.Response):
    """Коллекция технических узлов"""

    holder: int = validation.IdField(description="Идентификатор владельца узлов")
    tech_nests: list[models.TechNest] = pydantic.Field(
        description="Коллекция технических узлов",
        default_factory=list,
    )


class Devices(response.Response):
    """Коллекция устройств технического узла"""

    tech_nest: int = validation.IdField(description="Идентификатор технического узла")
    devices: list[models.Device] = pydantic.Field(
        description="Коллекция устройств технического узла",
        default_factory=list,
    )


class HolderCreated(response.Response):
    id: int = validation.IdField(description="Идентификатор владельца технического узла")


class TechNestAdded(response.Response):
    id: int = validation.IdField(description="Идентификатор технического узла")


class DeviceAdded(response.Response):
    id: int = validation.IdField(description="Идентификатор устройства")
