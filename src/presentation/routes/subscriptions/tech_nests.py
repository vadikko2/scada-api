import asyncio
import typing

import fastapi
import websockets.exceptions as ws_exc

from infrastructire import consumers, logging, publishers
from presentation import dependencies
from presentation.models import paths
from presentation.routes.subscriptions import heartbeat
from service_layer import cqrs
from service_layer.models import queries, responses

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Subscriptions"],
)


@router.websocket("/{nest}/ws")
async def subscribe_tech_nests(
    nest: typing.Annotated[int, paths.IdPath()],
    websocket: fastapi.WebSocket,
    consumer: consumers.EventConsumer = fastapi.Depends(dependencies.get_consumer),
    publisher_type: typing.Type[publishers.EventPublisher[fastapi.WebSocket]] = fastapi.Depends(
        dependencies.get_publisher_type,
    ),
    mediator: cqrs.Mediator = fastapi.Depends(dependencies.inject_mediator),
):
    logging.logger.debug("Open websocket")
    publisher = publisher_type(websocket)
    get_devices_query = queries.Devices(tech_nest=nest)
    devices: responses.Devices = await mediator.send(get_devices_query)
    device_ids = [device.id for device in devices.devices]  # noqa

    try:
        await websocket.accept()
        heartbeat_task = asyncio.create_task(heartbeat.send_heartbeat(websocket))
        publisher.heartbeat = heartbeat_task
        consume_task = asyncio.create_task(consumer.consume(publisher.publish))
        await asyncio.wait((heartbeat_task, consume_task))
    except ws_exc.ConnectionClosed:
        logging.logger.debug("Close websocket")
