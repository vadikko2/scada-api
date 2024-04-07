import asyncio
import typing
import uuid

import fastapi
import websockets.exceptions as ws_exc
from aio_pika import abc
from fastapi import websockets
from orjson import orjson

from infrastructire import amqp, consumers, logging, publishers, settings
from presentation.models import paths

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Subscriptions"],
)


class FromAmqpToWebsocketPublisher(publishers.EventPublisher[fastapi.WebSocket]):
    channel: fastapi.WebSocket
    heartbeat: asyncio.Task | None = None

    async def publish(self, message: abc.AbstractIncomingMessage) -> None:
        message_body = orjson.loads(message.body)

        if message_body.get("type") == "state":
            self.heartbeat.cancel()
        payload = message_body.get("payload")
        if not payload:
            return
        await self.channel.send_json(payload)


def get_consumer() -> consumers.EventConsumer:
    amqp_settings = settings.Amqp()
    session_guid = uuid.uuid4()
    queue_name = f"{amqp_settings.EVENTS_QUEUE}-{session_guid}"
    return amqp.AMQPConsumer(
        url=str(amqp_settings.dsn),
        exchange_name=amqp_settings.EVENTS_EXCHANGE,
        routing_key=amqp_settings.EVENTS_ROUTEING_KEY,
        queue_name=queue_name,
    )


def get_publisher_type() -> typing.Type[publishers.EventPublisher[fastapi.WebSocket]]:
    return FromAmqpToWebsocketPublisher


async def send_heartbeat(websocket: fastapi.WebSocket, consumer):
    while True:
        try:
            await websocket.send_json({"type": "heartbeat"})
            await asyncio.sleep(10)
        except websockets.WebSocketDisconnect:
            logging.logger.debug("Websocket disconnected")
            return


@router.websocket("/{nest}/ws")
async def subscribe_tech_nests(
    nest: typing.Annotated[int, paths.IdPath()],
    websocket: fastapi.WebSocket,
    consumer: consumers.EventConsumer = fastapi.Depends(get_consumer),
    publisher_type: typing.Type[publishers.EventPublisher[fastapi.WebSocket]] = fastapi.Depends(
        get_publisher_type,
    ),
):
    logging.logger.debug("Open websocket")
    publisher = publisher_type(websocket)
    try:
        await websocket.accept()
        heartbeat_task = asyncio.create_task(send_heartbeat(websocket, consumer))
        publisher.heartbeat = heartbeat_task
        consume_task = asyncio.create_task(consumer.consume(publisher.publish))
        _, pending = await asyncio.wait((heartbeat_task, consume_task))
    except ws_exc.ConnectionClosed:
        logging.logger.debug("Close websocket")
