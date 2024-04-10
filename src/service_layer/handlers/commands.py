from domain import models
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
    """Обновляет данные индикаторов технического узла"""

    def __init__(self, storage: storages.TechNestIndicatorValuesStorage):
        self.storage = storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.UpdateTechNestIndicators) -> None:
        # TODO добавить проверку существования узла
        await self.storage.set_value(request.tech_nest_id, request.values)
        self._events.append(
            events.TechNestIndicatorsUpdated(
                payload=models.TechNestIndicators(
                    tech_nest_id=request.tech_nest_id,
                    values=request.values,
                )
            )
        )


class UpdatedDeviceIndicatorsHandler(requests.RequestHandler[commands.UpdateDeviceIndicators, None]):
    """Обновляет данные индикаторов устройства"""

    def __init__(self, storage: storages.DeviceIndicatorValuesStorage):
        self.storage = storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.UpdateDeviceIndicators) -> None:
        # TODO добавить проверку существования узла и устройства
        await self.storage.set_value(request.device_id, request.values)
        self._events.append(
            events.DeviceIndicatorsUpdated(
                payload=models.DeviceIndicators(
                    tech_nest_id=request.tech_nest_id,
                    device_id=request.device_id,
                    values=request.values,
                )
            )
        )


class PublishTargetIndicatorsHandler(requests.RequestHandler[commands.PublishTargetIndicators, None]):
    """Публикует события с актуальными данными на индикаторах узла и устройств на нем"""

    def __init__(
        self,
        uow: unit_of_work.UoW,
        tech_nest_storage: storages.TechNestIndicatorValuesStorage,
        device_storage: storages.DeviceIndicatorValuesStorage,
    ):
        self.uow = uow
        self.nest_storage = tech_nest_storage
        self.device_storage = device_storage
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, request: commands.PublishTargetIndicators) -> None:
        async with self.uow.transaction() as uow:
            tech_nest_indicator_values = await self.nest_storage.get_value(request.nest)
            self._events.append(
                events.TechNestIndicatorsUpdated(
                    payload=models.TechNestIndicators(
                        tech_nest_id=request.nest,
                        values=tech_nest_indicator_values,
                    )
                )
            )
            devices = await uow.repository.get_devices(request.nest)
            device_ids = [device.id for device in devices]
            devices_indicator_values = await self.device_storage.get_values(*device_ids)
            for device_id, indicator_values in zip(device_ids, devices_indicator_values):
                self._events.append(
                    events.DeviceIndicatorsUpdated(
                        payload=models.DeviceIndicators(
                            tech_nest_id=request.nest,
                            device_id=device_id,
                            values=indicator_values,
                        )
                    )
                )
