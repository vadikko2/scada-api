import typing

import fastapi
from starlette import status

from domain import exceptions
from presentation import dependencies
from presentation.errors import registry
from presentation.models import paths
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import queries, responses

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы"],
)


@router.get(
    "/{nest}/devices",
    status_code=status.HTTP_200_OK,
    responses=registry.get_exception_responses(
        exceptions.NotFound,
    ),
)
async def get_devices(
    nest: typing.Annotated[int, paths.IdPath()],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[responses.Devices]:
    """Возвращает коллекцию устройств на техническом узле"""
    result = await mediator.send(queries.Devices(nest=nest))
    return pres_responses.Response(result=result)
