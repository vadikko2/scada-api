from service_layer.cqrs import requests
from service_layer.models import validation


class Query(requests.Request):
    """Базовый класс запроса"""


class Holder(Query):
    """Запрос данных владельца технического узла"""

    holder: int = validation.IdField(description="Идентификатор владельца технических узлов")


class TechNests(Query):
    """Запрос технических узлов по владельцу"""

    holder: int = validation.IdField(description="Идентификатор владельца технических узлов")


class Devices(Query):
    """Запрос устройств по техническому узлу"""

    tech_nest: int = validation.IdField(description="Идентификатор технического узла")
