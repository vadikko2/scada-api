import asyncio
import typing

import fastapi
from starlette import websockets

from infrastructire import logging
from presentation.models import paths

router = fastapi.APIRouter(
    prefix="/nests",
    tags=["Технические узлы", "Subscriptions"],
)


@router.websocket("/{nest}/ws")
async def subscribe_tech_nests(
    nest: typing.Annotated[int, paths.IdPath()],
    websocket: fastapi.WebSocket,
):
    await websocket.accept()
    logging.logger.debug("Open websocket")
    while True:
        try:
            await websocket.send_json(f"Hello {nest}")
            await asyncio.sleep(3)
        except websockets.WebSocketDisconnect:
            logging.logger.debug("Close websocket")
            return
