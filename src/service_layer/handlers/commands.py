from domain import exceptions, models
from infrastructire import storages
from infrastructire import uow as unit_of_work
from service_layer.cqrs import requests
from service_layer.cqrs.events import event
from service_layer.models import commands, events, responses


class CreateHolderHandler(requests.RequestHandler[commands.CreateHolder, responses.HolderCreated]):
    """Создает новую компанию владельца"""

    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: commands.CreateHolder) -> responses.HolderCreated:
        async with self.uow.transaction() as uow:
            new_holder = models.Holder(name=request.name, inn=request.inn, kpp=request.kpp)
            new_holder_id = await uow.repository.add_holder(new_holder)
            await uow.commit()
            return responses.HolderCreated(id=new_holder_id)


class AddTechNestHandler(requests.RequestHandler[commands.AddTechNest, responses.TechNestAdded]):
    """Добавляет новый технический узел"""

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
                name=request.name,
                location=new_location,
            )
            holder = await uow.repository.get_holder(request.holder)
            if holder is None:
                raise exceptions.NotFound(f"Holder with id {request.holder} not found")
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
            existed_nest = await uow.repository.get_nest(nest_id=request.nest)
            if existed_nest is None:
                raise exceptions.NotFound(f"Nest with nest_id {request.nest} not found")
            device = models.Device(name=request.name, model=request.model, nest_id=request.nest)
            new_device_id = await uow.repository.add_device(device)
            await uow.commit()
            return responses.DeviceAdded(id=new_device_id)


class UpdateTechNestIndicatorsHandler(requests.RequestHandler[commands.UpdateTechNestIndicators, None]):
    """Обновляет данные индикаторов технического узла"""

    def __init__(self, uow: unit_of_work.UoW, storage: storages.TechNestIndicatorValuesStorage):
        self.uow = uow
        self.storage = storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.UpdateTechNestIndicators) -> None:
        await self.storage.set_value(request.nest, request.values)
        self._events.append(
            events.TechNestIndicatorsUpdated(
                payload=models.TechNestIndicators(
                    nest=request.nest,
                    values=request.values,
                )
            )
        )


class UpdatedDeviceIndicatorsHandler(requests.RequestHandler[commands.UpdateDeviceIndicators, None]):
    """Обновляет данные индикаторов устройства"""

    def __init__(self, uow: unit_of_work.UoW, storage: storages.DeviceIndicatorValuesStorage):
        self.uow = uow
        self.storage = storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.UpdateDeviceIndicators) -> None:
        await self.storage.set_value(request.device, request.values)
        self._events.append(
            events.DeviceIndicatorsUpdated(
                payload=models.DeviceIndicators(
                    nest=request.nest,
                    device=request.device,
                    values=request.values,
                )
            )
        )
