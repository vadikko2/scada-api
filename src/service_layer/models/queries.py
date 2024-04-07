import uuid

import pydantic

from service_layer.event_driven import requests
from service_layer.models import validation


class Query(requests.Request):
    """Базовый класс запроса"""


class Holder(Query):
    holder: int = validation.IdField(description="Идентификатор владельца технических узлов")


class HolderTechNests(Query):
    holder: int = validation.IdField(description="Идентификатор владельца технических узлов")
