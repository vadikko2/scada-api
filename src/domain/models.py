from __future__ import annotations

import abc
import datetime
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


class PhaseControl(enum.Enum):
    NORMAL = "normal"
    ACCIDENT = "accident"


HolderIdField = functools.partial(
    pydantic.Field,
    description="Идентификатор владельца технического узла",
    gt=0,
)

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

UpdatedAtField = functools.partial(
    pydantic.Field,
    description="Временная метка публикации показателей индикаторов",
    default_factory=datetime.datetime.now,
)


class TechNest(pydantic.BaseModel):
    """Технический узел"""

    id: int | None = pydantic.Field(
        description="Идентификатор технического узла",
        default=None,
    )
    name: str = TechNestNameField()
    devices: list[Device] = DevicesListField()
    holder_id: int = HolderIdField()
    location: TechNestLocation = pydantic.Field(
        description="Местоположение",
    )

    model_config = pydantic.ConfigDict(
        from_attributes=True,
    )


class TechNestLocation(pydantic.BaseModel):
    """Локация технического узла"""

    id: int | None = pydantic.Field(
        description="Идентификатор локации",
        default=None,
    )
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

    id: int | None = pydantic.Field(
        description="Идентификатор устройства",
        default=None,
    )
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


class VoltageValue(IndicatorValue[decimal.Decimal]):
    """Напряжение"""

    _unit: typing.ClassVar[str] = "В"


class InputPowerIndicators(pydantic.BaseModel):
    """Показатели на входе"""

    input_number: int = pydantic.Field(
        description="Номер входа",
        json_schema_extra={"nullable": False},
        gt=0,
    )
    supply: bool = pydantic.Field(
        description="Питание на входе",
    )
    voltage: VoltageValue = pydantic.Field(
        description="Напряжение на входе",
    )


class InputPowerIndicatorsGroup(IndicatorsGroup):
    """Группа индикаторов электропитания"""

    inputs: list[InputPowerIndicators] = pydantic.Field(
        description="Показатели на входе",
        default_factory=list,
    )
    phase_control: PhaseControl = pydantic.Field(
        description="Контроль фазы",
        default=PhaseControl.NORMAL,
    )


class PowerConsumptionValue(IndicatorValue[decimal.Decimal]):
    """ "Показатели электропотребления"""

    _unit: typing.ClassVar[str] = "кВ"
    value: decimal.Decimal = pydantic.Field(ge=0)


class CumulativeWaterConsumptionValue(IndicatorValue[decimal.Decimal]):
    """Показатель накопительного расхода воды"""

    _unit: typing.ClassVar[str] = "м. куб."
    value: decimal.Decimal = pydantic.Field(ge=0)


class InstantaneousWaterConsumptionValue(IndicatorValue[decimal.Decimal]):
    """Показатель мгновенного расхода воды"""

    _unit: typing.ClassVar[str] = "м. куб. / сек"
    value: decimal.Decimal = pydantic.Field(ge=0)


class WaterConsumptionIndicators(pydantic.BaseModel):
    """Показатели потребления воды"""

    cumulative: CumulativeWaterConsumptionValue = pydantic.Field(description="Накопительный расход")
    instantaneous: InstantaneousWaterConsumptionValue = pydantic.Field(description="Мгновенный расход")


class ConsumptionIndicatorsGroup(IndicatorsGroup):
    """Группа индикаторов потребления"""

    power: PowerConsumptionValue = pydantic.Field(description="Показатели электропотребления")
    water: WaterConsumptionIndicators = pydantic.Field(description="Потребление воды")


class TechNestIndicatorsValues(pydantic.BaseModel):
    """Значения на индикаторах технического узла"""

    input_power: InputPowerIndicatorsGroup = pydantic.Field(
        description="Показатели на группе индикаторов электропитания",
    )
    consumption: ConsumptionIndicatorsGroup = pydantic.Field(
        description="Показатели на группе индикаторов потребления",
    )
    updated_at: datetime.datetime = UpdatedAtField()


class TechNestIndicators(pydantic.BaseModel):
    """Показатели на узле"""

    nest: int | None = pydantic.Field(description="Идентификатор технического узла")
    values: TechNestIndicatorsValues = pydantic.Field(description="Значения на индикаторах")


class AmmeterValue(IndicatorValue[decimal.Decimal]):
    """Показатель силы тока"""

    _unit: typing.ClassVar[str] = "А"
    value: decimal.Decimal = pydantic.Field(ge=0)


class Frequency(IndicatorValue[decimal.Decimal]):
    _unit: typing.ClassVar[str] = "Гц"
    value: decimal.Decimal = pydantic.Field(ge=0)


class DeviceIndicatorsValues(pydantic.BaseModel):
    """Значения на индикаторах устройства"""

    ammeter: AmmeterValue = pydantic.Field(description="Значение силы тока")
    mode: ModeEnum = pydantic.Field(description="Режим работы", default=ModeEnum.MANUAL)
    frequency: Frequency = pydantic.Field(description="Частота работы")
    status: DeviceStatus = pydantic.Field(description="Статус устройства")
    updated_at: datetime.datetime = UpdatedAtField()


class DeviceIndicators(pydantic.BaseModel):
    """Показатели на устройстве"""

    nest: int | None = pydantic.Field(description="Идентификатор технического узла")
    device: int | None = pydantic.Field(description="Идентификатор устройства")
    values: DeviceIndicatorsValues = pydantic.Field(description="Значения на индикаторах")
