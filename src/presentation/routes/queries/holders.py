import typing

import fastapi
from starlette import status

from domain import exceptions
from presentation import dependencies
from presentation.errors import registry
from presentation.models import paths
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import queries
from service_layer.models import responses as service_responses

router = fastapi.APIRouter(
    prefix="/holders",
    tags=["Владельцы-компании технических узлов"],
)


@router.get(
    "/{holder}/nests",
    status_code=status.HTTP_200_OK,
    responses=registry.get_exception_responses(
        exceptions.NotFound,
    ),
)
async def get_nests(
    holder: typing.Annotated[int, paths.IdPath()],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.TechNests]:
    """Возвращает все технические узлы владельца"""
    result = await mediator.send(queries.TechNests(holder=holder))
    return pres_responses.Response(result=result)


@router.get(
    "/{holder}",
    status_code=status.HTTP_200_OK,
    responses=registry.get_exception_responses(
        exceptions.NotFound,
    ),
)
async def get_holder_info(
    holder: typing.Annotated[int, paths.IdPath()],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.Holder]:
    """Возвращает информацию о владельце технических узлов"""
    result = await mediator.send(queries.Holder(holder=holder))
    return pres_responses.Response(result=result)
