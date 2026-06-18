"""Simulate AMS v3.1 workflow scenarios and verify violation events."""

from __future__ import annotations

import time

import httpx

BASE = "http://127.0.0.1:8000"
CAMERA_ID = "CAM-001"
TRACK_BASE = int(time.time()) % 100000 * 10


def cross(track_id: int, zone_id: str, timestamp: str) -> dict | None:
    response = httpx.post(
        f"{BASE}/api/transitions/cross",
        json={
            "track_id": track_id,
            "camera_id": CAMERA_ID,
            "zone_id": zone_id,
            "timestamp": timestamp,
            "object_type": "person",
        },
    )
    if response.status_code == 204:
        return None
    response.raise_for_status()
    return response.json()


def run_scenario(
    name: str,
    track_id: int,
    zones: list[str],
    expected_codes: set[str],
) -> bool:
    print(f"\n=== {name} (track {track_id}) ===")
    base_ts = "2026-06-17T10:00:00"
    for index, zone in enumerate(zones):
        minute = index + 1
        cross(track_id, zone, f"2026-06-17T10:{minute:02d}:00")

    history = httpx.get(
        f"{BASE}/api/workflows/history",
        params={"track_id": track_id, "limit": 20},
    ).json()
    codes = {item["loai_vi_pham"] for item in history if item.get("loai_vi_pham")}
    print("Expected:", sorted(expected_codes))
    print("Actual:", sorted(codes))
    ok = expected_codes.issubset(codes) if expected_codes else len(codes) == 0
    print("PASS" if ok else "FAIL")
    return ok


def main() -> None:
    workflows = httpx.get(f"{BASE}/api/workflows").json()
    print(f"Workflows seeded: {len(workflows)}")
    for workflow in workflows:
        print(f"- {workflow['ten_quy_trinh']}: {len(workflow['steps'])} bước")

    results = [
        run_scenario(
            "Đi đúng quy trình vào chuồng nái",
            track_id=TRACK_BASE + 1,
            zones=[
                "worker_housing",
                "shower_room",
                "handwash_zone",
                "boot_disinfection_tray",
                "gestation_barn",
            ],
            expected_codes=set(),
        ),
        run_scenario(
            "Bỏ qua nhà tắm",
            track_id=TRACK_BASE + 2,
            zones=["worker_housing", "gestation_barn"],
            expected_codes={"KHONG_TAM_SAT_TRUNG", "KHONG_SAT_TRUNG_TAY", "KHONG_SAT_TRUNG_UNG"},
        ),
        run_scenario(
            "Bỏ qua sát trùng tay",
            track_id=TRACK_BASE + 3,
            zones=[
                "worker_housing",
                "shower_room",
                "boot_disinfection_tray",
                "gestation_barn",
            ],
            expected_codes={"KHONG_SAT_TRUNG_TAY"},
        ),
        run_scenario(
            "Bỏ qua sát trùng ủng",
            track_id=TRACK_BASE + 4,
            zones=[
                "worker_housing",
                "shower_room",
                "handwash_zone",
                "gestation_barn",
            ],
            expected_codes={"KHONG_SAT_TRUNG_UNG"},
        ),
        run_scenario(
            "Đi ngược tuyến",
            track_id=TRACK_BASE + 5,
            zones=[
                "worker_housing",
                "shower_room",
                "handwash_zone",
                "boot_disinfection_tray",
                "shower_room",
            ],
            expected_codes={"DI_NGUOC_TUYEN"},
        ),
    ]

    violation_types = httpx.get(f"{BASE}/api/workflows/violation-types").json()
    print(f"\nLoại vi phạm ATSH: {len(violation_types)}")
    pipeline = httpx.get(f"{BASE}/api/workflows/pipeline").json()
    print(f"Pipeline: {pipeline['version']} → {pipeline['next']}")

    track_detail = httpx.get(f"{BASE}/api/tracks/{TRACK_BASE + 1}").json()
    print(f"\nTrack {TRACK_BASE + 1} visits: {len(track_detail['lich_su_vung'])} zones")

    dashboard = httpx.get(f"{BASE}/api/workflows/dashboard").json()
    print(f"Vi phạm hôm nay: {dashboard['vi_pham_hom_nay']}")
    print(f"Top quy trình: {dashboard['top_quy_trinh_bi_vi_pham'][:3]}")

    passed = all(results)
    print(f"\n{'ALL PASS' if passed else 'SOME FAILED'}")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
