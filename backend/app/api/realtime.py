import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["realtime"])


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except RuntimeError:
                self.disconnect(connection)


manager = ConnectionManager()
dashboard_manager = ConnectionManager()


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        await websocket.send_json(
            {
                "type": "connected",
                "message": "AMS realtime alert stream connected",
            }
        )
        while True:
            await asyncio.sleep(15)
            await websocket.send_json(
                {
                    "type": "heartbeat",
                    "message": "waiting_for_alerts",
                }
            )
    except (RuntimeError, WebSocketDisconnect):
        manager.disconnect(websocket)


@router.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket) -> None:
    await dashboard_manager.connect(websocket)
    try:
        await websocket.send_json(
            {
                "type": "connected",
                "message": "AMS dashboard realtime stream connected",
            }
        )
        while True:
            await asyncio.sleep(10)
            await websocket.send_json(
                {
                    "type": "dashboard_heartbeat",
                    "message": "dashboard_waiting_for_runtime_stats",
                }
            )
    except (RuntimeError, WebSocketDisconnect):
        dashboard_manager.disconnect(websocket)
