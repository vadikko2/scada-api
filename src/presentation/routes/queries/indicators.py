import typing

import fastapi
from starlette import status

from domain import exceptions, models
from presentation import dependencies
from presentation.errors import registry
from presentation.models import paths
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import queries, responses

router = fastapi.APIRouter(
    prefix="/indicators",
    tags=["Показатели на индикаторах"],
    responses=registry.get_exception_responses(exceptions.NotFound),
)


@router.get("/nest/{nest}", status_code=status.HTTP_200_OK)
async def get_nest_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[responses.TechNestIndicators]:
    """Возвращает актуальные значения на индикаторах технического узла"""
    result = await mediator.send(queries.TechNestIndicators(nest=nest))
    return pres_responses.Response(result=result)


@router.get("/nest/{nest}/devices", status_code=status.HTTP_200_OK)
async def get_devices_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.ResponseMulti[models.DeviceIndicators]:
    """Возвращает актуальные значения на индикаторах устройств узла"""
    result: responses.DeviceIndicators = await mediator.send(queries.DevicesIndicators(nest=nest))
    return pres_responses.ResponseMulti[models.DeviceIndicators](result=result.devices)
