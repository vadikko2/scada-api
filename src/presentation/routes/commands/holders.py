import fastapi
from starlette import status

from presentation import dependencies
from presentation.models import requests, responses as pres_responses
from service_layer import event_driven
from service_layer.models import commands, responses as service_responses

router = fastapi.APIRouter(
    prefix="/holders",
    tags=["Tech nests holders"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def get_nests(
    command: requests.CommandRequest[commands.CreateHolder],
    mediator: event_driven.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> pres_responses.Response[service_responses.HolderCreated]:
    """
    Создает нового владельца технического узла
    """
    result = await mediator.send(command.body)
    return pres_responses.Response(result=result)
