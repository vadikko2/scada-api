import asyncio

import fastapi
from fastapi import websockets

from infrastructire import logging


async def send_heartbeat(websocket: fastapi.WebSocket):
    while True:
        try:
            await websocket.send_json({"type": "heartbeat"})
            await asyncio.sleep(10)
        except websockets.WebSocketDisconnect:
            logging.logger.debug("Websocket disconnected")
            return
