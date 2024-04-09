from __future__ import annotations

import decimal
import enum
import typing

import pydantic


class ModeEnum(enum.Enum):
    AUTO = "auto"
    MANUAL = "manual"
    ACCIDENT = "accident"


class DeviceStatus(enum.Enum):
    TURNED_ON = "turned_on"
    TURNED_OFF = "turned_off"


class TechNest(pydantic.BaseModel):
    """Технический узел"""

    id: int | None = pydantic.Field(description="Идентификатор технического узла", default=None)
    devices: list[Device] = pydantic.Field(
        description="Набор устройств в узле",
        default_factory=list,
    )
    holder_id: int = pydantic.Field(description="Владелец технического узла")
    location: TechNestLocation = pydantic.Field(description="Местоположение")

    model_config = pydantic.ConfigDict(from_attributes=True)


class TechNestLocation(pydantic.BaseModel):
    """Локация технического узла"""

    id: int | None = pydantic.Field(description="Идентификатор локации", default=None)
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    address: str

    model_config = pydantic.ConfigDict(from_attributes=True)


class Company(pydantic.BaseModel):
    """Компания владелец технического узла"""

    id: int | None = pydantic.Field(description="Идентификатор компании", default=None)
    name: str = pydantic.Field(description="Наименование организации")
    inn: int = pydantic.Field(description="ИНН организации")
    kpp: int = pydantic.Field(description="КПП организации")

    model_config = pydantic.ConfigDict(from_attributes=True)


class Device(pydantic.BaseModel):
    """Устройство на техническом узле"""

    id: int | None = pydantic.Field(description="Идентификатор устройства", default=None)
    name: str = pydantic.Field(description="Наименование устройства")
    model: str | None = pydantic.Field(description="Модель устройства", default=None)
    nest_id: int

    model_config = pydantic.ConfigDict(from_attributes=True)


VT = typing.TypeVar("VT")


class IndicatorValue(pydantic.BaseModel, typing.Generic[VT]):
    unit: str
    value: VT = pydantic.Field(description="Значение на индикаторе")


class TechNestIndicatorsValues(pydantic.BaseModel):
    """Значения на индикаторах технического узла"""


class TechNestIndicators(pydantic.BaseModel):
    """Показатели на узле"""

    tech_nest_id: int | None = pydantic.Field(description="Идентификатор технического узла")
    values: TechNestIndicatorsValues = pydantic.Field(description="Значения на индикаторах")


class AmmeterValue(IndicatorValue[decimal.Decimal]):
    unit: str = "A"


class Frequency(IndicatorValue[decimal.Decimal]):
    unit: str = "HZ"


class DeviceIndicatorsValues(pydantic.BaseModel):
    """Значения на индикаторах устройства"""

    ammeter: AmmeterValue = pydantic.Field(description="Значение силы тока")
    mode: ModeEnum = pydantic.Field(description="Режим работы", default=ModeEnum.MANUAL)
    frequency: Frequency = pydantic.Field(description="Частота работы")
    status: DeviceStatus = pydantic.Field(description="Статус устройства")


class DeviceIndicators(pydantic.BaseModel):
    """Показатели на устройстве"""

    tech_nest_id: int | None = pydantic.Field(description="Идентификатор технического узла")
    device_id: int | None = pydantic.Field(description="Идентификатор устройства")
    values: DeviceIndicatorsValues = pydantic.Field(description="Значения на индикаторах")
