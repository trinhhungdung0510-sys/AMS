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
from app.api.api_health import router as api_health_router
from app.api.demo import router as demo_router
from app.api.deployment import router as deployment_router
from app.api.devices import router as devices_router
from app.api.detectors import router as detectors_router
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
from app.api.notification import router as notification_router
from app.api.observations import router as observations_router
from app.api.realtime import router as realtime_router
from app.api.reports import router as reports_router
from app.api.biosecurity_rules import router as biosecurity_rules_router
from app.api.runtime_metrics import router as runtime_metrics_router
from app.api.rules import router as rules_router
from app.api.smart_farm import router as smart_farm_router
from app.api.snapshots import router as snapshots_router
from app.api.stress import router as stress_router
from app.api.streams import router as streams_router
from app.api.tasks import router as tasks_router
from app.api.tracks import router as tracks_router
from app.api.transitions import router as transitions_router
from app.api.system import router as system_router
from app.api.uniforms import router as uniforms_router
from app.api.users import router as users_router
from app.api.zone_transitions import router as zone_transitions_router
from app.api.visitors import router as visitors_router
from app.api.workflows import router as workflows_router
from app.api.zones import router as zones_router
from app.core.config import get_settings
from app.services.event_stream_service import event_stream_service
from app.compliance.compliance_engine import init_compliance_engine
from app.biosecurity_workflow.workflow_manager import init_workflow_manager
from app.services.pipeline_subscribers import register_pipeline_subscribers
from app.services.violation_notification_service import register_violation_notification_subscriber
from app.services.system_alert_notification_service import register_system_alert_gmail_subscriber
from app.services.rtsp_simulator import rtsp_simulator_worker
from app.services.detector_runtime_service import register_default_detectors, shutdown_detectors
from app.services.runtime_metrics_service import register_metrics_subscribers
from app.services.camera_health_service import camera_health_service
from app.services.retention_service import run_retention_cleanup
from app.services.demo_assets_service import demo_assets_dir, ensure_demo_assets
from app.services.demo_event_generator import demo_event_generator
from app.services.demo_mode_service import is_demo_mode
from app.database.session import SessionLocal
from app.ws.event_gateway import router as ws_events_router

settings = get_settings()

app = FastAPI(title=settings.app_name, version="4.0.0")
app.state.rtsp_stop_event = asyncio.Event()
app.state.rtsp_task = None
app.state.health_task = None

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
app.include_router(api_health_router, prefix=settings.api_prefix)
app.include_router(deployment_router, prefix=settings.api_prefix)
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
app.include_router(demo_router, prefix=settings.api_prefix)
app.include_router(detectors_router, prefix=settings.api_prefix)
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
app.include_router(notification_router, prefix=settings.api_prefix)
app.include_router(smart_farm_router, prefix=settings.api_prefix)
app.include_router(snapshots_router, prefix=settings.api_prefix)
app.include_router(stress_router, prefix=settings.api_prefix)
app.include_router(streams_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)
app.include_router(uniforms_router, prefix=settings.api_prefix)
app.include_router(users_router, prefix=settings.api_prefix)
app.include_router(system_router, prefix=settings.api_prefix)
app.include_router(transitions_router, prefix=f"{settings.api_prefix}/transitions")
app.include_router(zone_transitions_router, prefix=f"{settings.api_prefix}/zone-transitions")
app.include_router(workflows_router, prefix=settings.api_prefix)
app.include_router(zones_router, prefix=settings.api_prefix)
app.include_router(employees_router, prefix=settings.api_prefix)
app.include_router(visitors_router, prefix=settings.api_prefix)
app.include_router(tracks_router, prefix=settings.api_prefix)
app.include_router(realtime_router)
app.include_router(reports_router, prefix=settings.api_prefix)
app.include_router(ws_events_router)
app.include_router(biosecurity_rules_router, prefix=settings.api_prefix)
app.include_router(runtime_metrics_router, prefix=settings.api_prefix)
app.include_router(rules_router, prefix=settings.api_prefix)

storage_root = Path(settings.storage_root)
storage_root.mkdir(parents=True, exist_ok=True)
Path(settings.employee_storage_dir).mkdir(parents=True, exist_ok=True)
app.mount("/storage", StaticFiles(directory=str(storage_root)), name="storage")

uploads_root = Path(settings.uploads_root)
uploads_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_root)), name="uploads")

ensure_demo_assets()
demo_assets_path = demo_assets_dir()
demo_assets_path.mkdir(parents=True, exist_ok=True)
app.mount("/demo-assets", StaticFiles(directory=str(demo_assets_path)), name="demo-assets")


@app.on_event("startup")
async def start_rtsp_simulator() -> None:
    register_pipeline_subscribers()
    register_violation_notification_subscriber()
    register_system_alert_gmail_subscriber()
    init_compliance_engine()
    init_workflow_manager()
    register_metrics_subscribers()
    event_stream_service.set_app_loop(asyncio.get_running_loop())
    event_stream_service.register()

    db = SessionLocal()
    try:
        demo_enabled = is_demo_mode(db)
    finally:
        db.close()

    if demo_enabled:
        if settings.demo_auto_start:
            await demo_event_generator.start()
        elif settings.demo_seed_on_startup:
            db = SessionLocal()
            try:
                demo_event_generator.seed_baseline(db, count=settings.demo_seed_count, publish=True)
            finally:
                db.close()
    else:
        register_default_detectors()

    app.state.rtsp_stop_event = asyncio.Event()
    if not demo_enabled:
        app.state.rtsp_task = asyncio.create_task(rtsp_simulator_worker(app.state.rtsp_stop_event))
    else:
        app.state.rtsp_task = None
    app.state.health_task = asyncio.create_task(_camera_health_monitor_worker(app.state.rtsp_stop_event))
    app.state.retention_task = asyncio.create_task(_retention_worker(app.state.rtsp_stop_event))


async def _camera_health_monitor_worker(stop_event: asyncio.Event) -> None:
    from app.services.health import check_database
    from app.services.system_alert_notification_service import notify_database_unavailable

    while not stop_event.is_set():
        db = SessionLocal()
        try:
            try:
                check_database(db)
            except Exception as exc:
                notify_database_unavailable(error=str(exc))
            camera_health_service.evaluate_statuses(db)
        finally:
            db.close()
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=30.0)
        except asyncio.TimeoutError:
            continue


async def _retention_worker(stop_event: asyncio.Event) -> None:
    while not stop_event.is_set():
        db = SessionLocal()
        try:
            run_retention_cleanup(db)
        finally:
            db.close()
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=21600.0)
        except asyncio.TimeoutError:
            continue


@app.on_event("shutdown")
async def stop_rtsp_simulator() -> None:
    await demo_event_generator.stop()
    shutdown_detectors()
    if app.state.rtsp_task:
        app.state.rtsp_stop_event.set()
        app.state.rtsp_task.cancel()
    if getattr(app.state, "health_task", None):
        app.state.health_task.cancel()
    if getattr(app.state, "retention_task", None):
        app.state.retention_task.cancel()
