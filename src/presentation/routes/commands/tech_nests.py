import typing

import fastapi
from starlette import status

from presentation import dependencies
from presentation.models import paths, requests
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import commands
from service_layer.models import responses as service_responses

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Commands"],
)


@router.put("/{nest}/device", status_code=status.HTTP_201_CREATED)
async def add_device(
    nest: typing.Annotated[int, paths.IdPath()],
    command: requests.CommandRequest[commands.AddDevice],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.DeviceAdded]:
    """
    Добавляет новое устройство в технический узел
    """
    assert command.body.nest == nest
    result = await mediator.send(command.body)
    return pres_responses.Response(result=result)
