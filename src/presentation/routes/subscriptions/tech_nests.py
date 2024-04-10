import asyncio
import typing

import fastapi
import websockets.exceptions as ws_exc

from domain import models
from infrastructire import consumers, logging, publishers
from presentation import dependencies
from presentation.models import paths
from presentation.routes.subscriptions import heartbeat
from service_layer import cqrs
from service_layer.models import commands

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Subscriptions"],
)


async def init(mediator, command: commands.Command) -> None:
    """Выполняет инициирующие действия"""
    await asyncio.sleep(1)
    await mediator.send(command)


@router.websocket("/{nest}/ws")
async def subscribe_tech_nests(
    nest: typing.Annotated[int, paths.IdPath()],
    websocket: fastapi.WebSocket,
    consumer: consumers.EventConsumer = fastapi.Depends(dependencies.get_consumer),
    publisher_type: typing.Type[publishers.EventPublisher[fastapi.WebSocket]] = fastapi.Depends(
        dependencies.get_publisher_type,
    ),
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
) -> models.TechNestIndicators | models.DeviceIndicators:
    logging.logger.debug("Open websocket")
    publisher = publisher_type()
    publisher.channel = websocket

    try:
        await websocket.accept()
        heartbeat_task = asyncio.create_task(heartbeat.send_heartbeat(websocket))
        init_task = asyncio.create_task(init(mediator, commands.PublishTargetIndicators(nest=nest)))
        publisher.heartbeat = heartbeat_task
        consume_task = asyncio.create_task(consumer.consume(publisher.publish))
        await asyncio.wait((init_task, heartbeat_task, consume_task))
    except ws_exc.ConnectionClosed:
        logging.logger.debug("Close websocket")
