import typing

from domain import models
from service_layer import cqrs


class Event(cqrs.NotificationEvent):
    """Базовый класс события"""


T = typing.TypeVar("T")


class IndicatorsUpdatedEvent(cqrs.NotificationEvent, typing.Generic[T]):
    payload: T


class TechNestIndicatorsUpdated(IndicatorsUpdatedEvent[models.TechNestIndicators]):
    """Событие об обновлении данных на индикаторах технического узла"""

    payload: models.TechNestIndicators


class DeviceIndicatorsUpdated(IndicatorsUpdatedEvent[models.DeviceIndicators]):
    """Событие об обновлении данных на индикаторах устройства"""

    payload: models.DeviceIndicators
