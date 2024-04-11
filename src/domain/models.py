from __future__ import annotations

import abc
import decimal
import enum
import functools
import typing

import pydantic


class ModeEnum(enum.Enum):
    AUTO = "auto"
    MANUAL = "manual"
    ACCIDENT = "accident"


class DeviceStatus(enum.Enum):
    TURNED_ON = "turned_on"
    TURNED_OFF = "turned_off"


HolderIdField = functools.partial(pydantic.Field, description="Идентификатор владельца технического узла", gt=0)

HolderNameField = functools.partial(
    pydantic.Field,
    description="Наименование организации",
    examples=['ООО "Рога и копыта"'],
)

INN = functools.partial(
    pydantic.Field,
    description="ИНН организации",
    examples=[
        "7812003110",
    ],
    min_length=10,
    max_length=12,
)
KPP = functools.partial(
    pydantic.Field,
    description="КПП организации",
    examples=["783801001", None],
    min_length=9,
    max_length=9,
    default=None,
)


TechNestNameField = functools.partial(
    pydantic.Field,
    description="Название технического узла",
    examples=["Насосная станция 1"],
)
TechNestListField = functools.partial(
    pydantic.Field,
    description="Набор технических узлов",
    default_factory=list,
)

LatitudeField = functools.partial(
    pydantic.Field,
    description="Широта",
    examples=["59.938924"],
)

LongitudeField = functools.partial(
    pydantic.Field,
    description="Долгота",
    examples=["30.315311"],
)

AddressField = functools.partial(
    pydantic.Field,
    description="Адрес",
    examples=["Дворцовая пл., Санкт-Петербург, 191186"],
)

DeviceNameField = functools.partial(
    pydantic.Field,
    description="Наименование устройства",
    examples=["Насос 1"],
)

DeviceModelField = functools.partial(
    pydantic.Field,
    description="Модель устройства",
    default=None,
)

DevicesListField = functools.partial(
    pydantic.Field,
    description="Набор устройств в узле",
    default_factory=list,
)


class TechNest(pydantic.BaseModel):
    """Технический узел"""

    id: int | None = pydantic.Field(description="Идентификатор технического узла", default=None)
    name: str = TechNestNameField()
    devices: list[Device] = DevicesListField()
    holder_id: int = HolderIdField()
    location: TechNestLocation = pydantic.Field(description="Местоположение")

    model_config = pydantic.ConfigDict(from_attributes=True)


class TechNestLocation(pydantic.BaseModel):
    """Локация технического узла"""

    id: int | None = pydantic.Field(description="Идентификатор локации", default=None)
    latitude: decimal.Decimal = LatitudeField()
    longitude: decimal.Decimal = LongitudeField()
    address: str = pydantic.Field()

    model_config = pydantic.ConfigDict(from_attributes=True)


class Holder(pydantic.BaseModel):
    """Компания владелец технического узла"""

    id: int | None = HolderIdField(default=None)
    name: str = HolderNameField()
    inn: str = INN()
    kpp: str | None = KPP()

    model_config = pydantic.ConfigDict(from_attributes=True)


class Device(pydantic.BaseModel):
    """Устройство на техническом узле"""

    id: int | None = pydantic.Field(description="Идентификатор устройства", default=None)
    name: str = DeviceNameField()
    model: str | None = DeviceModelField()
    nest_id: int

    model_config = pydantic.ConfigDict(from_attributes=True)


VT = typing.TypeVar("VT")


class IndicatorValue(pydantic.BaseModel, typing.Generic[VT], abc.ABC):
    _unit: typing.ClassVar[str]
    value: VT = pydantic.Field(description="Значение на индикаторе")

    @pydantic.computed_field()
    @property
    def unit(self) -> str:
        return self._unit  # noqa


class IndicatorsGroup(pydantic.BaseModel):
    """Группа индикаторов"""


class TechNestIndicatorsValues(pydantic.BaseModel):
    """Значения на индикаторах технического узла"""

    class PowerIndicatorsGroup(IndicatorsGroup):
        """Группа индикаторов электропитания"""

        class PowerInputIndicators(pydantic.BaseModel):
            """Показатели на входе"""

        inputs: list[PowerInputIndicators] = pydantic.Field(description="Показатели на входе", default=[])

    class ConsumptionIndicatorsGroup(IndicatorsGroup):
        """Группа индикаторов потребления"""

    power: PowerIndicatorsGroup = pydantic.Field(description="Показатели на группе индикаторов электропитания")
    consumption: ConsumptionIndicatorsGroup = pydantic.Field(description="Показатели на группе индикаторов потребления")


class TechNestIndicators(pydantic.BaseModel):
    """Показатели на узле"""

    nest: int | None = pydantic.Field(description="Идентификатор технического узла")
    values: TechNestIndicatorsValues = pydantic.Field(description="Значения на индикаторах")
    # TODO добавить временную метку получения показателя


class AmmeterValue(IndicatorValue[decimal.Decimal]):
    """Показатель силы тока"""

    _unit: typing.ClassVar[str] = "A"
    value: decimal.Decimal = pydantic.Field(ge=0)


class Frequency(IndicatorValue[decimal.Decimal]):
    _unit: typing.ClassVar[str] = "HZ"
    value: decimal.Decimal = pydantic.Field(ge=0)


class DeviceIndicatorsValues(pydantic.BaseModel):
    """Значения на индикаторах устройства"""

    ammeter: AmmeterValue = pydantic.Field(description="Значение силы тока")
    mode: ModeEnum = pydantic.Field(description="Режим работы", default=ModeEnum.MANUAL)
    frequency: Frequency = pydantic.Field(description="Частота работы")
    status: DeviceStatus = pydantic.Field(description="Статус устройства")


class DeviceIndicators(pydantic.BaseModel):
    """Показатели на устройстве"""

    nest: int | None = pydantic.Field(description="Идентификатор технического узла")
    device: int | None = pydantic.Field(description="Идентификатор устройства")
    values: DeviceIndicatorsValues = pydantic.Field(description="Значения на индикаторах")
    # TODO добавить временную метку получения показателя
