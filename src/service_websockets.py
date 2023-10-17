import asyncio
from typing import List

from fastapi import WebSocket

from src.schema import StatusMessage


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await asyncio.sleep(0)

    async def broadcast(self, message: StatusMessage):
        for connection in self.active_connections:
            await connection.send_json(dict(message))
            await asyncio.sleep(0)

    async def sent(self, message: StatusMessage, websocket: WebSocket):
        await websocket.send_json(dict(message))
        await asyncio.sleep(0)

    async def send_generic_error(self, exc: str, websocket: WebSocket):
        message = {"code": 500, "detail": exc, "status": "ERROR"}
        await websocket.send_json(message)
        await asyncio.sleep(0)


manager = ConnectionManager()
