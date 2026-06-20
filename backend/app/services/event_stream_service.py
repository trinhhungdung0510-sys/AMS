from __future__ import annotations

import asyncio
import logging
from typing import Any

from app.core.event_bus import get_event_bus
from app.core.event_bus import event_types as topics
from app.ws.connection_manager import events_manager

logger = logging.getLogger(__name__)

TOPIC_TO_WS_TYPE = {
    topics.OBSERVATION_CREATED: "observation.created",
    topics.TRACK_UPDATED: "track.updated",
    topics.RULE_EVALUATED: "rule.evaluated",
    topics.EVENT_CREATED: "event.created",
    topics.NOTIFICATION_CREATED: "notification.created",
    topics.CAMERA_STATUS_CHANGED: "camera.status",
    topics.DETECTOR_STARTED: "detector.started",
    topics.DETECTOR_STOPPED: "detector.stopped",
    topics.DETECTOR_FAILED: "detector.failed",
    topics.DETECTOR_RECOVERED: "detector.recovered",
}


class EventStreamService:
    def __init__(self) -> None:
        self._registered = False
        self._loop: asyncio.AbstractEventLoop | None = None

    def set_app_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def register(self) -> None:
        if self._registered:
            return

        bus = get_event_bus()
        for topic in TOPIC_TO_WS_TYPE:
            bus.subscribe(topic, self._forward_to_websocket)
        self._registered = True
        logger.info("EventStreamService registered on EventBus")

    def _forward_to_websocket(self, payload: dict[str, Any]) -> None:
        topic = payload.get("topic")
        ws_type = TOPIC_TO_WS_TYPE.get(topic, topic)
        message = {
            "type": ws_type,
            "topic": topic,
            "payload": payload.get("data") or payload,
            "timestamp": payload.get("timestamp"),
        }

        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(events_manager.broadcast(message), self._loop)
            return

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(events_manager.broadcast(message))
        except RuntimeError:
            logger.warning("Skipped WS broadcast — no running event loop for topic=%s", topic)


event_stream_service = EventStreamService()
