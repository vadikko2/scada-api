import typing

import fastapi
from starlette import status

from domain import models
from presentation import dependencies
from presentation.models import paths, requests
from service_layer import cqrs
from service_layer.models import commands

router = fastapi.APIRouter(
    prefix="/indicators",
    tags=["Показатели на индикаторах", "Commands"],
)


@router.put("/nest/{nest}", status_code=status.HTTP_204_NO_CONTENT)
async def publish_tech_nest_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    command: requests.CommandRequest[models.TechNestIndicatorsValues],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
):
    """Публикует значения на индикаторах технического узла"""
    await mediator.send(commands.UpdateTechNestIndicators(tech_nest_id=nest, values=command.body))


@router.put("/nest/{nest}/device/{device}", status_code=status.HTTP_204_NO_CONTENT)
async def publish_device_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    device: typing.Annotated[int, paths.IdPath()],
    command: requests.CommandRequest[models.DeviceIndicatorsValues],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> None:
    """Публикует значения на индикаторах устройства"""
    await mediator.send(commands.UpdateDeviceIndicators(tech_nest_id=nest, device_id=device, values=command.body))
