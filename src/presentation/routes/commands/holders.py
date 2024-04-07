import fastapi
from starlette import status

from presentation import dependencies
from presentation.models import requests
from presentation.models import responses as pres_responses
from service_layer import cqrs
from service_layer.models import commands
from service_layer.models import responses as service_responses

router = fastapi.APIRouter(
    prefix="/holders",
    tags=["Владельцы-компании технических узлов", "Commands"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_holder(
    command: requests.CommandRequest[commands.CreateHolder],
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.HolderCreated]:
    """
    Создает нового владельца технического узла
    """
    result = await mediator.send(command.body)
    return pres_responses.Response(result=result)
