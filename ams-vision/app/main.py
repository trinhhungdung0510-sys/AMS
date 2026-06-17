import asyncio

from fastapi import FastAPI

from app.config import get_settings
from app.worker import RTSPStreamWorker

settings = get_settings()
worker = RTSPStreamWorker(settings)

app = FastAPI(title=settings.service_name, version="3.0.0")
app.state.stop_event = asyncio.Event()
app.state.worker_task = None


@app.on_event("startup")
async def startup() -> None:
    app.state.stop_event = asyncio.Event()
    app.state.worker_task = asyncio.create_task(worker.run_forever(app.state.stop_event))


@app.on_event("shutdown")
async def shutdown() -> None:
    if app.state.worker_task:
        app.state.stop_event.set()
        app.state.worker_task.cancel()


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": settings.service_name,
        "mock_detection": settings.mock_detection,
        "camera_id": settings.camera_id,
        "backend_base_url": settings.backend_base_url,
        "detections_published": worker.detections_published,
        "tracks_total": len(worker.tracking.list_tracks()),
        "last_detection": worker.last_detection,
    }


@app.post("/mock-detection")
async def mock_detection() -> dict:
    return await worker.run_once()


@app.get("/api/tracks")
def list_tracks() -> list[dict]:
    return worker.tracking.list_tracks()
