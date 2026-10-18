import asyncio
import json
import threading
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import jwt
from backend.contracts.topics import INCIDENTS_UPDATES
from backend.core.kafka import consume
from backend.core.security import decode_token

router = APIRouter()
clients: set[WebSocket] = set()


@router.websocket("/ws/incidents")
async def ws_incidents(ws: WebSocket, token: str):
    try:
        user = decode_token(token)
    except jwt.PyJWTError:
        await ws.close(code=4401)
        return
    if user["role"] not in ("operator", "admin", "department"):
        await ws.close(code=4403)
        return
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()   # keep-alive
    except WebSocketDisconnect:
        clients.discard(ws)


async def _broadcast(msg: dict):
    for c in list(clients):
        try:
            await c.send_text(json.dumps(msg))
        except Exception:  # noqa: BLE001
            clients.discard(c)


def start_kafka_listener(loop: asyncio.AbstractEventLoop) -> None:
    """thread بيقرا incidents.updates ويبثها. الـ WebSocket إشعار بس، والـ DB هي الحقيقة."""
    def handler(msg: dict):
        asyncio.run_coroutine_threadsafe(_broadcast(msg), loop)
    threading.Thread(target=consume, args=([INCIDENTS_UPDATES], "api_ws", handler), daemon=True).start()
