"""Simulate AMS v4.0 Biosecurity AI Engine scenarios."""

from __future__ import annotations

import httpx

BASE = "http://127.0.0.1:8000"
CAMERA_ID = "CAM-001"


def cross(track_id: int, zone_id: str, timestamp: str, object_type: str = "person") -> None:
    response = httpx.post(
        f"{BASE}/api/zone-transitions/cross",
        json={
            "track_id": track_id,
            "camera_id": CAMERA_ID,
            "zone_id": zone_id,
            "timestamp": timestamp,
            "object_type": object_type,
        },
    )
    if response.status_code not in {200, 204}:
        response.raise_for_status()


def sync_truck(track_id: int, zone_id: str, object_type: str, timestamp: str) -> None:
    httpx.post(
        f"{BASE}/api/tracks/sync",
        json={
            "tracks": [
                {
                    "track_id": track_id,
                    "camera_id": CAMERA_ID,
                    "object_type": object_type,
                    "current_zone": zone_id,
                    "previous_zone": None,
                    "enter_time": timestamp,
                    "leave_time": None,
                    "last_seen": timestamp,
                    "confidence": 95,
                }
            ]
        },
    ).raise_for_status()


def main() -> None:
    rules = httpx.get(f"{BASE}/api/biosecurity-rules/enabled").json()
    v4_rules = [rule for rule in rules if rule["ma_quy_tac"].startswith(("FORBIDDEN", "ANIMAL", "DIRTY", "WORKER"))]
    print(f"Enabled ATSH rules: {len(rules)} (v4 core: {len(v4_rules)})")

    areas = httpx.get(f"{BASE}/api/biosecurity-rules/farm-areas").json()
    print(f"Farm area types: {len(areas)}")

    cross(9001, "feed_storage", "2026-06-17T11:01:00")
    cross(9002, "gestation_barn", "2026-06-17T11:02:00", object_type="dog")
    cross(9003, "worker_housing", "2026-06-17T11:03:00")
    cross(9003, "gestation_barn", "2026-06-17T11:04:00")

    sync_truck(8801, "pig_loading_zone", "pig_truck", "2026-06-17T11:05:00")
    cross(9004, "pig_loading_zone", "2026-06-17T11:06:00")

    sync_truck(8802, "feed_storage", "feed_truck", "2026-06-17T11:07:00")
    cross(9005, "feed_storage", "2026-06-17T11:08:00")

    summary = httpx.get(f"{BASE}/api/dashboard/summary").json()
    print(f"ATSH violations total: {summary['tong_vi_pham_atsh']}")
    print(f"Today: {summary['vi_pham_atsh_hom_nay']}")
    print(f"By severity: CRITICAL={summary['vi_pham_atsh_critical']} WARNING={summary['vi_pham_atsh_warning']}")

    transitions = httpx.get(f"{BASE}/api/zone-transitions/recent?limit=5").json()
    print(f"Recent zone transitions: {transitions['total']}")

    print("Simulation complete.")


if __name__ == "__main__":
    main()
