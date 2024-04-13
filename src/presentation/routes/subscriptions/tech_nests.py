import asyncio
import typing

import fastapi
import websockets.exceptions as ws_exc

from infrastructire import consumers, logging, publishers
from presentation import dependencies
from presentation.models import paths
from presentation.routes.subscriptions import heartbeat
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
    consumer: consumers.EventConsumer = fastapi.Depends(dependencies.inject_consumer),
    publisher: publishers.AbstractFromAmqpToWebsocketPublisher = fastapi.Depends(dependencies.inject_publisher),
):
    """WebSocket подписка на получение обновлений показателей на техническом узле и устройствах"""
    logging.logger.debug(f"Websocket for {nest=} opened")
    publisher.channel = websocket

    try:
        await websocket.accept()
        heartbeat_task = asyncio.create_task(heartbeat.send_heartbeat(websocket))
        publisher.heartbeat = heartbeat_task
        consume_task = asyncio.create_task(consumer.consume(publisher))
        await asyncio.wait((heartbeat_task, consume_task))
    except ws_exc.ConnectionClosed:
        logging.logger.debug(f"Websocket for {nest=} closed")
