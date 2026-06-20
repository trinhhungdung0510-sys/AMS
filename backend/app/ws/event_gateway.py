from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.ws.connection_manager import events_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["realtime-events"])


@router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket) -> None:
    await events_manager.connect(websocket)
    try:
        await websocket.send_json(
            {
                "type": "connected",
                "message": "AMS event stream connected",
                "supported": [
                    "observation.created",
                    "track.updated",
                    "rule.evaluated",
                    "event.created",
                    "event.updated",
                    "notification.created",
                    "camera.status",
                ],
            }
        )
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "heartbeat", "message": "alive"})
    except WebSocketDisconnect:
        events_manager.disconnect(websocket)
    except Exception:
        logger.exception("WebSocket events gateway error")
        events_manager.disconnect(websocket)
