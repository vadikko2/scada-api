from __future__ import annotations

import decimal
import enum

import pydantic


class ModeEnum(enum.Enum):
    AUTO = "auto"
    MANUAL = "manual"
    ACCIDENT = "accident"


class TechNest(pydantic.BaseModel):
    """Технический узел"""

    id: int = pydantic.Field(description="Идентификатор технического узла", ge=1)
    devices: list[Device] = pydantic.Field(
        description="Набор устройств в узле",
        default_factory=list,
    )
    holder: int = pydantic.Field(description="Владелец технического узла", ge=1)
    location: TechNestLocation = pydantic.Field(description="Местоположение")


class TechNestLocation(pydantic.BaseModel):
    """Локация технического узла"""

    id: int = pydantic.Field(description="Идентификатор локации")
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    address: str


class Company(pydantic.BaseModel):
    """Компания владелец технического узла"""

    id: int = pydantic.Field(description="Идентификатор компании", ge=1)
    name: str = pydantic.Field(description="Наименование организации")
    inn: int = pydantic.Field(description="ИНН организации")
    kpp: int = pydantic.Field(description="КПП организации")


class Device(pydantic.BaseModel):
    """Устройство на техническом узле"""

    id: int = pydantic.Field(description="Идентификатор устройства", ge=1)
    name: str = pydantic.Field(description="Наименование устройства")
    model: str | None = pydantic.Field(description="Модель устройства", default=None)


class TechNestIndicators(pydantic.BaseModel):
    """Показатели на узле"""


class DeviceIndicators(pydantic.BaseModel):
    """Показатели на устройстве"""
