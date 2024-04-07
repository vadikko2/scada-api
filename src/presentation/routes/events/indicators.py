import typing

import fastapi
from starlette import status

from domain import models
from presentation import dependencies
from presentation.models import paths, requests
from service_layer import event_driven
from service_layer.models import events

router = fastapi.APIRouter(
    prefix="/indicators",
    tags=["Владельцы-компании технических узлов", "Events"],
)


@router.put("/nest/{nest}", status_code=status.HTTP_204_NO_CONTENT)
async def publish_tech_nest_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    event: requests.EventRequest[events.TechNestIndicatorsUpdated],
    mediator: event_driven.Mediator = fastapi.Depends(dependencies.inject_mediator),
):
    """Публикует значения на индикаторах технического узла"""
    pass


@router.put("/nest/{nest}/device/{device}", status_code=status.HTTP_204_NO_CONTENT)
async def publish_device_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    device: typing.Annotated[int, paths.IdPath()],
    event: requests.EventRequest[models.DeviceIndicatorsValues],
    mediator: event_driven.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> None:
    """Публикует значения на индикаторах устройства"""
    event_body = events.DeviceIndicatorsUpdated(
        tech_nest_id=nest,
        device_id=device,
        body=event.body
    )
    await mediator.send_events([event_body])
