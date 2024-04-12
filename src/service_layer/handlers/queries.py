from domain import models
from infrastructire import storages
from infrastructire import uow as unit_of_work
from service_layer.cqrs import requests
from service_layer.cqrs.events import event
from service_layer.models import queries, responses


class GetHolderHandler(requests.RequestHandler[queries.Holder, responses.Holder | None]):
    """
    Обрабатывает запросы на получение данных о владельце технического узла
    """

    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: queries.Holder) -> responses.Holder | None:
        async with self.uow.transaction() as uow:
            holder_info = await uow.repository.get_holder(request.holder)
            return responses.Holder(**holder_info.model_dump(mode="json"))


class GetTechNestsHandler(requests.RequestHandler[queries.TechNests, responses.TechNests]):
    """
    Обрабатывает запросы на получение данных о технических узлах
    """

    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: queries.TechNests) -> responses.TechNests:
        async with self.uow.transaction() as uow:
            nests = await uow.repository.get_nests_by_holder(request.holder)
            return responses.TechNests(holder=request.holder, tech_nests=nests)


class GetDevicesHandler(requests.RequestHandler[queries.Devices, responses.Devices]):
    """
    Обрабатывает запросы на получение данных об устройствах
    """

    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: queries.Devices) -> responses.Devices:
        async with self.uow.transaction() as uow:
            devices = await uow.repository.get_devices(request.nest)
            return responses.Devices(nest=request.nest, devices=devices)


class GetTargetNestIndicatorsHandler(requests.RequestHandler[queries.TechNestIndicators, responses.TechNestIndicators]):
    """Возвращает актуальные данные на индикаторах узла"""

    def __init__(
        self,
        tech_nest_storage: storages.TechNestIndicatorValuesStorage,
    ):
        self.nest_storage = tech_nest_storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: queries.TechNestIndicators) -> responses.TechNestIndicators:
        tech_nest_indicator_values = await self.nest_storage.get_value(request.nest)
        return responses.TechNestIndicators(nest=request.nest, values=tech_nest_indicator_values)


class GetDevicesIndicatorsHandler(requests.RequestHandler[queries.DevicesIndicators, responses.DeviceIndicators]):
    """Возвращает актуальные данные на индикаторах устройств узла"""

    def __init__(
        self,
        uow: unit_of_work.UoW,
        device_storage: storages.DeviceIndicatorValuesStorage,
    ):
        self.uow = uow
        self.device_storage = device_storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: queries.DevicesIndicators) -> responses.DeviceIndicators:
        indicators: list[models.DeviceIndicators] = []
        async with self.uow.transaction() as uow:
            devices: list[models.Device] = await uow.repository.get_devices(nest=request.nest)
            devices_ids = [device.id for device in devices]

        values = await self.device_storage.get_values(*devices_ids)
        for device_id, value in zip(devices_ids, values):
            indicators.append(models.DeviceIndicators(nest=request.nest, device=device_id, values=value))
        return responses.DeviceIndicators(devices=indicators)
