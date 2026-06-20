from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list = []

    async def connect(self, websocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict[str, Any]) -> None:
        stale: list = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except RuntimeError:
                stale.append(connection)
            except Exception:
                logger.exception("WebSocket send failed")
                stale.append(connection)

        for connection in stale:
            self.disconnect(connection)


events_manager = ConnectionManager()
legacy_alerts_manager = ConnectionManager()
legacy_dashboard_manager = ConnectionManager()
