from domain import models
from infrastructire import storages
from infrastructire import uow as unit_of_work
from service_layer.cqrs import requests
from service_layer.cqrs.events import event
from service_layer.models import commands, events, responses


class CreateHolderHandler(requests.RequestHandler[commands.CreateHolder, responses.HolderCreated]):
    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: commands.CreateHolder) -> responses.HolderCreated:
        async with self.uow.transaction() as uow:
            new_holder = models.Company(name=request.name, inn=request.inn, kpp=request.kpp)
            new_holder_id = await uow.repository.add_holder(new_holder)
            await uow.commit()
            return responses.HolderCreated(id=new_holder_id)


class AddTechNestHandler(requests.RequestHandler[commands.AddTechNest, responses.TechNestAdded]):
    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: commands.AddTechNest) -> responses.TechNestAdded:
        async with self.uow.transaction() as uow:
            new_location = models.TechNestLocation(
                latitude=request.latitude,
                longitude=request.longitude,
                address=request.address,
            )
            new_nest = models.TechNest(
                holder_id=request.holder,
                location=new_location,
            )
            new_nest_id = await uow.repository.add_nest(new_nest)
            await uow.commit()
            return responses.TechNestAdded(id=new_nest_id)


class AddDeviceHandler(requests.RequestHandler[commands.AddDevice, responses.DeviceAdded]):
    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: commands.AddDevice) -> responses.DeviceAdded:
        async with self.uow.transaction() as uow:
            device = models.Device(name=request.name, model=request.model, nest_id=request.nest)
            new_device_id = await uow.repository.add_device(device)
            await uow.commit()
            return responses.DeviceAdded(id=new_device_id)


class UpdateTechNestIndicatorsHandler(requests.RequestHandler[commands.UpdateTechNestIndicators, None]):
    def __init__(self, storage: storages.TechNestIndicatorValuesStorage):
        self.storage = storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.UpdateTechNestIndicators) -> None:
        await self.storage.set_value(request.tech_nest_id, request.body)
        self._events.append(
            events.TechNestIndicatorsUpdated(
                tech_nest_id=request.tech_nest_id,
                body=request.body,
            )
        )


class UpdatedDeviceIndicatorsHandler(requests.RequestHandler[commands.UpdateDeviceIndicators, None]):
    def __init__(self, storage: storages.DeviceIndicatorValuesStorage):
        self.storage = storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.UpdateDeviceIndicators) -> None:
        await self.storage.set_value(request.device_id, request.body)
        self._events.append(
            events.DeviceIndicatorsUpdated(
                tech_nest_id=request.tech_nest_id,
                device_id=request.device_id,
                body=request.body,
            )
        )
