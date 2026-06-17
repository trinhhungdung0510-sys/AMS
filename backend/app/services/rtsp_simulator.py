import asyncio
import json
import uuid
from datetime import datetime, timezone

from app.api.realtime import dashboard_manager, manager
from app.database.session import SessionLocal
from app.models import AITask
from app.services.alert_engine import process_ai_task

SIMULATED_ALERTS = [
    ("CAM-001", "restricted_zone_intrusion", 9),
    ("CAM-002", "pig_fever", 8),
    ("CAM-004", "pig_abnormal", 10),
    ("CAM-005", "camera_offline", 10),
    ("CAM-008", "vehicle_disinfection", 7),
]


async def rtsp_simulator_worker(stop_event: asyncio.Event) -> None:
    index = 0
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=30)
            continue
        except asyncio.TimeoutError:
            pass

        camera_id, category, priority = SIMULATED_ALERTS[index % len(SIMULATED_ALERTS)]
        index += 1

        db = SessionLocal()
        try:
            task = AITask(
                id=f"TASK-RT-{uuid.uuid4().hex[:8].upper()}",
                camera_id=camera_id,
                category=category,
                status="queued",
                priority=priority,
                result=json.dumps({"source": "rtsp_simulator"}, ensure_ascii=False),
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            db.add(task)
            db.flush()
            payload = process_ai_task(db, task)
            db.commit()
        finally:
            db.close()

        await manager.broadcast(payload)
        await dashboard_manager.broadcast(
            {
                "type": "dashboard_update",
                "source": "rtsp_simulator",
                "last_alert": payload,
            }
        )
