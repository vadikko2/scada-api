from domain import models
from infrastructire import uow as unit_of_work
from service_layer.event_driven import requests
from service_layer.event_driven.events import event
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
            await uow.repository.add_holder(new_holder)
            return responses.HolderCreated(id=new_holder.id)


class UpdateTechNestIndicatorsHandler(requests.RequestHandler[commands.UpdateTechNestIndicators, None]):
    def __init__(self):
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, command: commands.UpdateTechNestIndicators) -> None:
        self._events.append(
            events.TechNestIndicatorsUpdated(
                tech_nest_id=command.tech_nest_id,
                body=command.body,
            )
        )


class UpdatedDeviceIndicatorsHandler(requests.RequestHandler[commands.UpdateDeviceIndicators, None]):
    def __init__(self):
        self._events = []

    @property
    def events(self) -> list[event.Event]:
        return self._events

    async def handle(self, command: commands.UpdateDeviceIndicators) -> None:
        self._events.append(
            events.DeviceIndicatorsUpdated(
                tech_nest_id=command.tech_nest_id,
                device_id=command.device_id,
                body=command.body,
            )
        )
