from domain import models
from service_layer import cqrs


class Event(cqrs.NotificationEvent):
    """Базовый класс события"""


class TechNestIndicatorsUpdated(Event, models.TechNestIndicators):
    """Событие об обновлении данных на индикаторах технического узла"""


class DeviceIndicatorsUpdated(Event, models.DeviceIndicators):
    """Событие об обновлении данных на индикаторах устройства"""
