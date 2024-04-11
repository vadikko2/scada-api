import typing

import fastapi
from starlette import status

from domain import models
from presentation.models import paths
from presentation.models import responses as pres_responses
from service_layer.models import responses

router = fastapi.APIRouter(
    prefix="/indicators",
    tags=["Показатели на индикаторах", "Queries"],
)


@router.get("/nest/{nest}", status_code=status.HTTP_200_OK)
async def get_nest_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
) -> pres_responses.Response[responses.TechNestIndicators]:
    """Возвращает актуальные значения на индикаторах технического узла"""
    pass


@router.get("/nest/{nest}/devices/", status_code=status.HTTP_200_OK)
async def get_device_indicators(
    nest: typing.Annotated[int, paths.IdPath()],
    devices: typing.Annotated[list[int], fastapi.Query(description="Список идентификаторов устройств")],
) -> pres_responses.Response[models.DeviceIndicatorsValues]:
    """Возвращает актуальные значения на индикаторах устройства"""
    pass
