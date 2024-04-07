from domain import models
from infrastructire import uow as unit_of_work
from service_layer.event_driven.events import event
from service_layer.models import commands, responses
from service_layer.event_driven import requests


class CreateHolderHandler(requests.RequestHandler[commands.CreateHolder, responses.HolderCreated]):

    def __init__(self, uow: unit_of_work.UoW):
        self.uow = uow

    @property
    def events(self) -> list[event.Event]:
        return []

    async def handle(self, request: commands.CreateHolder) -> responses.HolderCreated:
        async with self.uow.transaction() as uow:
            holder = uow.repository.add_holder(models.Company())
            return responses.HolderCreated(id=holder)
