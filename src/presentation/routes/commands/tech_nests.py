import fastapi
from starlette import status

from domain import exceptions
from presentation import dependencies
from presentation.errors import registry
from presentation.models import requests
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import commands
from service_layer.models import responses as service_responses

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Commands"],
)


@router.put(
    "/device",
    status_code=status.HTTP_201_CREATED,
    responses=registry.get_exception_responses(
        exceptions.AlreadyExists,
        exceptions.NotFound,
    ),
)
async def add_device(
    command: requests.CommandRequest[commands.AddDevice],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.DeviceAdded]:
    """
    Добавляет новое устройство в технический узел
    """
    result = await mediator.send(command.body)
    return pres_responses.Response(result=result)
