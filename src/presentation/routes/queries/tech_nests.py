import typing

import fastapi
from starlette import status

from presentation import dependencies
from presentation.models import paths
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import queries, responses

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Queries"],
)


@router.get("/{nest}/devices", status_code=status.HTTP_200_OK)
async def get_devices(
    nest: typing.Annotated[int, paths.IdPath()],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[responses.Devices]:
    """Возвращает коллекцию устройств на техническом узле"""
    return await mediator.send(queries.Devices(tech_nest=nest))
