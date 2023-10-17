import asyncio
from typing import Any

from fastapi import APIRouter
from fastapi import status, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from redis.asyncio.cluster import RedisCluster
from transitions.core import MachineError
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from src.auth import authorize_user
from src.logger import server_logger
from src.microwave import state_machine
from src.redis_session import Cacher, aget_redis_client
from src.schema import StatusMessage, ButtonsMessage, Buttons, Claims
from src.service import ButtonService
from src.service_websockets import manager

router = APIRouter()


@router.get("/status", response_model=StatusMessage)
async def microwave_data() -> Any:
    service = ButtonService(state_machine)
    result = await service.return_results()
    return result


@router.post(
    "/handle_button_push",
    response_model=StatusMessage,
    status_code=status.HTTP_201_CREATED,
)
async def handle_button_push(
    button: ButtonsMessage, redis_client: RedisCluster = Depends(aget_redis_client)
):
    service = ButtonService(state_machine)
    result = await service.process_action(button.button)
    await Cacher(redis_client).aredis_dump(state_machine)
    return result


@router.post(
    "/cancel",
    response_model=StatusMessage,
    status_code=status.HTTP_201_CREATED,
)
async def handle_button_cancel(
    redis_client: RedisCluster = Depends(aget_redis_client),
    _: Claims = Depends(authorize_user),
):
    service = ButtonService(state_machine)
    result = await service.process_action(Buttons.CANCEL)
    await Cacher(redis_client).aredis_dump(state_machine)
    return result


@router.websocket("/ws_status")
async def websocket_status(websocket: WebSocket):
    await manager.connect(websocket)
    service = ButtonService(state_machine)
    try:
        while True:
            msg = await service.return_results()
            await manager.sent(msg, websocket)
            await asyncio.sleep(1)

            try:
                async with asyncio.timeout(0):
                    _ = await websocket.receive()
            except TimeoutError:
                pass

    except (
        WebSocketDisconnect,
        ConnectionClosedOK,
        ConnectionClosedError,
        RuntimeError,
    ):
        server_logger.warning("WebSocketDisconnect")
    except (MachineError, ValidationError) as ex:
        server_logger.error(str(ex))
        await manager.send_generic_error(str(ex), websocket)
    finally:
        await manager.disconnect(websocket)
