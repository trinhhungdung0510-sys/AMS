#!/usr/bin/env python3
"""Run YOLO detector worker (separate process from FastAPI).

Examples:
  # Webcam test (local pipeline + DB)
  python scripts/run_yolo_detector.py --camera-id CAM-01 --source webcam

  # RTSP stream via API ingest (requires running backend + auth)
  python scripts/run_yolo_detector.py \\
    --camera-id CAM-01 \\
    --source rtsp://user:pass@192.168.1.10/stream1 \\
    --ingest api \\
    --api-url http://127.0.0.1:8000 \\
    --email admin@example.com \\
    --password secret

  # Video file
  python scripts/run_yolo_detector.py --camera-id CAM-01 --source /path/to/video.mp4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.workers.detector_worker import DetectorWorkerConfig, run_detector_worker  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="AMS YOLO detector worker (v1.6)")
    parser.add_argument("--camera-id", required=True, help="AMS camera id")
    parser.add_argument(
        "--source",
        required=True,
        help="Video source: rtsp://..., file path, webcam, or 0",
    )
    parser.add_argument("--model", default="yolov8n.pt", help="Ultralytics model path")
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--fps-limit", type=float, default=5.0, help="Max observations/sec")
    parser.add_argument(
        "--ingest",
        choices=["local", "api"],
        default="local",
        help="local=DB+EventBus in worker; api=POST to running backend",
    )
    parser.add_argument("--api-url", default="http://127.0.0.1:8000")
    parser.add_argument("--token", dest="api_token", default=None)
    parser.add_argument("--email", dest="api_email", default=None)
    parser.add_argument("--password", dest="api_password", default=None)
    parser.add_argument(
        "--no-bytetrack",
        action="store_true",
        help="Force simple tracker even if supervision is installed",
    )
    args = parser.parse_args()

    config = DetectorWorkerConfig(
        camera_id=args.camera_id,
        video_source=args.source,
        model_path=args.model,
        confidence=args.confidence,
        fps_limit=args.fps_limit,
        prefer_bytetrack=not args.no_bytetrack,
        ingest_mode=args.ingest,
        api_url=args.api_url,
        api_token=args.api_token,
        api_email=args.api_email,
        api_password=args.api_password,
    )
    run_detector_worker(config)


if __name__ == "__main__":
    main()
