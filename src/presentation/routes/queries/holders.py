import typing

from starlette import status

from presentation import dependencies
from presentation.models import responses as pres_responses, paths
from service_layer.models import responses as service_responses, queries
from service_layer import event_driven
import fastapi

router = fastapi.APIRouter(
    prefix="/holders",
    tags=["Владельцы-компании технических узлов", "Queries"],
)


@router.get("/{holder}/nests", status_code=status.HTTP_200_OK)
async def get_nests(
    holder: typing.Annotated[int, paths.IdPath()],
    mediator: event_driven.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.TechNests]:
    """
    Возвращает все технические узлы владельца
    """
    result = await mediator.send(queries.HolderTechNests(holder=holder))
    return pres_responses.Response(result=result)


@router.get("/{holder}", status_code=status.HTTP_200_OK)
async def get_holder(
    holder: typing.Annotated[int, paths.IdPath()],
    mediator: event_driven.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.Holder]:
    """Возвращает информацию о владельце технических узлов"""
    result = await mediator.send(queries.Holder(holder=holder))
    return pres_responses.Response(result=result)
