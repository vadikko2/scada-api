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
            devices = await uow.repository.get_devices(request.tech_nest)
            return responses.Devices(tech_nest=request.tech_nest, devices=devices)
