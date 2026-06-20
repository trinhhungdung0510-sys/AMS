import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.animal_intrusion import router as animal_intrusion_router
from app.api.ai_detections import router as ai_detections_router
from app.api.ai_models import router as ai_models_router
from app.api.audit import router as audit_router
from app.api.auth import router as auth_router
from app.api.camera_health import router as camera_health_router
from app.api.camera_zone_rules import router as camera_zone_rules_router
from app.api.camera_zones import router as camera_zones_router
from app.api.camera_snapshots import router as camera_snapshots_router
from app.api.cameras import router as cameras_router
from app.api.compliance import router as compliance_router
from app.api.dashboard import router as dashboard_router
from app.api.devices import router as devices_router
from app.api.employees import router as employees_router
from app.api.events import router as events_router
from app.api.farm_zones import router as farm_zones_router
from app.api.farms import router as farms_router
from app.api.templates import router as templates_router
from app.api.gateways import router as gateways_router
from app.api.health import router as health_router
from app.api.licenses import router as licenses_router
from app.api.map import router as map_router
from app.api.notifications import router as notifications_router
from app.api.observations import router as observations_router
from app.api.realtime import router as realtime_router
from app.api.biosecurity_rules import router as biosecurity_rules_router
from app.api.rules import router as rules_router
from app.api.smart_farm import router as smart_farm_router
from app.api.snapshots import router as snapshots_router
from app.api.streams import router as streams_router
from app.api.tasks import router as tasks_router
from app.api.tracks import router as tracks_router
from app.api.transitions import router as transitions_router
from app.api.zone_transitions import router as zone_transitions_router
from app.api.visitors import router as visitors_router
from app.api.workflows import router as workflows_router
from app.api.zones import router as zones_router
from app.core.config import get_settings
from app.services.rtsp_simulator import rtsp_simulator_worker

settings = get_settings()

app = FastAPI(title=settings.app_name, version="4.0.0")
app.state.rtsp_stop_event = asyncio.Event()
app.state.rtsp_task = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list(),
    allow_origin_regex=(
        r"https://.*\.trycloudflare\.com|"
        r"http://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)(:\d+)?"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(animal_intrusion_router, prefix=settings.api_prefix)
app.include_router(ai_detections_router, prefix=settings.api_prefix)
app.include_router(ai_models_router, prefix=settings.api_prefix)
app.include_router(audit_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(camera_health_router, prefix=settings.api_prefix)
app.include_router(cameras_router, prefix=settings.api_prefix)
app.include_router(camera_snapshots_router, prefix=settings.api_prefix)
app.include_router(camera_zones_router, prefix=settings.api_prefix)
app.include_router(camera_zone_rules_router, prefix=settings.api_prefix)
app.include_router(compliance_router, prefix=settings.api_prefix)
app.include_router(dashboard_router, prefix=settings.api_prefix)
app.include_router(devices_router, prefix=settings.api_prefix)
app.include_router(events_router, prefix=settings.api_prefix)
app.include_router(farms_router, prefix=settings.api_prefix)
app.include_router(farm_zones_router, prefix=settings.api_prefix)
app.include_router(templates_router, prefix=settings.api_prefix)
app.include_router(gateways_router, prefix=settings.api_prefix)
app.include_router(map_router, prefix=settings.api_prefix)
app.include_router(licenses_router, prefix=settings.api_prefix)
app.include_router(observations_router, prefix=settings.api_prefix)
app.include_router(notifications_router, prefix=settings.api_prefix)
app.include_router(smart_farm_router, prefix=settings.api_prefix)
app.include_router(snapshots_router, prefix=settings.api_prefix)
app.include_router(streams_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)
app.include_router(transitions_router, prefix=f"{settings.api_prefix}/transitions")
app.include_router(zone_transitions_router, prefix=f"{settings.api_prefix}/zone-transitions")
app.include_router(workflows_router, prefix=settings.api_prefix)
app.include_router(zones_router, prefix=settings.api_prefix)
app.include_router(employees_router, prefix=settings.api_prefix)
app.include_router(visitors_router, prefix=settings.api_prefix)
app.include_router(tracks_router, prefix=settings.api_prefix)
app.include_router(realtime_router)
app.include_router(biosecurity_rules_router, prefix=settings.api_prefix)
app.include_router(rules_router, prefix=settings.api_prefix)

storage_root = Path(settings.storage_root)
storage_root.mkdir(parents=True, exist_ok=True)
Path(settings.employee_storage_dir).mkdir(parents=True, exist_ok=True)
app.mount("/storage", StaticFiles(directory=str(storage_root)), name="storage")

uploads_root = Path(settings.uploads_root)
uploads_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_root)), name="uploads")


@app.on_event("startup")
async def start_rtsp_simulator() -> None:
    app.state.rtsp_stop_event = asyncio.Event()
    app.state.rtsp_task = asyncio.create_task(rtsp_simulator_worker(app.state.rtsp_stop_event))


@app.on_event("shutdown")
async def stop_rtsp_simulator() -> None:
    if app.state.rtsp_task:
        app.state.rtsp_stop_event.set()
        app.state.rtsp_task.cancel()
