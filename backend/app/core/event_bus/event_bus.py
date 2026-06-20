from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Callable

logger = logging.getLogger(__name__)

EventHandler = Callable[[dict[str, Any]], None]


class EventBus(ABC):
    @abstractmethod
    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic: str, handler: EventHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        raise NotImplementedError


class InMemoryEventBus(EventBus):
    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        message = dict(payload or {})
        message.setdefault("topic", topic)

        for handler in list(self._subscribers.get(topic, [])):
            try:
                handler(message)
            except Exception:
                logger.exception("EventBus handler failed for topic=%s", topic)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        if handler not in self._subscribers[topic]:
            self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        handlers = self._subscribers.get(topic, [])
        if handler in handlers:
            handlers.remove(handler)


_event_bus: InMemoryEventBus | None = None


def get_event_bus() -> InMemoryEventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = InMemoryEventBus()
    return _event_bus
