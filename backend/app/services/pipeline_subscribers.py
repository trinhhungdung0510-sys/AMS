from __future__ import annotations

import logging
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.core.event_bus import get_event_bus
from app.core.event_bus import event_types as topics
from app.core.runtime.zone_presence_tracker import PRESENCE_ENTER, PRESENCE_EXIT, get_zone_presence_tracker
from app.core.runtime.track_store import get_track_store
from app.core.runtime.zone_mapper import map_observation_to_zones, object_in_zone
from app.database.session import SessionLocal
from app.models import CameraZone, ZoneRule
from app.schemas.observation import EventEngineCreate
from app.services.evaluator_event_service import create_event_from_evaluation
from app.services.observation_service import utc_now_iso
from app.services.zone_rule_service import list_rules_for_camera
from sqlalchemy import select

logger = logging.getLogger(__name__)


def _publish(topic: str, data: dict[str, Any]) -> None:
    get_event_bus().publish(
        topic,
        {
            "topic": topic,
            "timestamp": utc_now_iso(),
            "data": data,
        },
    )


def handle_observation_created(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    observation = payload.get("observation")
    if not observation:
        return

    db = SessionLocal()
    try:
        camera_id = observation.get("camera_id") or observation.get("cameraId")
        zones = [
            {
                "id": zone.id,
                "name": zone.name,
                "parent_zone_id": zone.parent_zone_id,
                "points": zone.points,
                "points_format": zone.points_format,
                "reference_width": zone.reference_width,
                "reference_height": zone.reference_height,
            }
            for zone in db.scalars(
                select(CameraZone).where(CameraZone.camera_id == camera_id)
            )
        ]
        mappings = map_observation_to_zones(observation, zones)
        mapping_by_track = {item["objectId"]: item for item in mappings}
        track_store = get_track_store()

        for obj in observation.get("objects") or []:
            track_id = obj.get("trackId") or obj.get("track_id")
            mapping = mapping_by_track.get(track_id, {"zones": [], "subzones": []})
            track, is_new, previous = track_store.upsert_track(
                camera_id=camera_id,
                track_id=track_id,
                object_class=obj.get("class"),
                timestamp=observation.get("timestamp") or observation.get("created_at"),
                current_zone_id=(mapping.get("zones") or [None])[0],
                current_sub_zone_id=(mapping.get("subzones") or [None])[0],
                metadata={
                    "confidence": obj.get("confidence"),
                    "bbox": obj.get("bbox"),
                    "attributes": obj.get("attributes") or {},
                    "observationId": observation.get("id"),
                },
            )
            _publish(
                topics.TRACK_UPDATED,
                {
                    "track": track,
                    "isNew": is_new,
                    "previousTrack": previous,
                    "observation": observation,
                    "zoneMapping": mapping,
                },
            )

        _evaluate_zone_rules(db, observation, zones, mappings, track_store)
    except Exception:
        logger.exception("TrackStore subscriber failed")
    finally:
        db.close()


def handle_track_updated(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    track = payload.get("track")
    observation = payload.get("observation")
    zone_mapping = payload.get("zoneMapping")
    if not track or not observation:
        return

    db = SessionLocal()
    try:
        hits = _evaluate_track_rules(db, track, observation, zone_mapping)
        for hit in hits:
            _publish(topics.RULE_EVALUATED, hit)
            create_event_from_evaluation(db, EventEngineCreate(**hit["eventPayload"]))
    except Exception:
        logger.exception("Evaluator subscriber failed for track=%s", track.get("trackId"))
    finally:
        db.close()


def handle_event_created(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    event = payload.get("event")
    if not event:
        return

    _publish(
        topics.NOTIFICATION_CREATED,
        {
            "notification": {
                "type": "event_created",
                "eventId": event.get("id"),
                "cameraId": event.get("camera_id"),
                "severity": event.get("severity"),
                "eventType": event.get("event_type"),
                "message": f"[{event.get('severity')}] {event.get('event_type')} — {event.get('zone_name') or event.get('zone_id')}",
            }
        },
    )


def _evaluate_track_rules(
    db: Session,
    track: dict[str, Any],
    observation: dict[str, Any],
    zone_mapping: Optional[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not zone_mapping:
        return []

    hits: list[dict[str, Any]] = []
    rules = list_rules_for_camera(db, track["cameraId"])
    obj = next(
        (
            item
            for item in observation.get("objects") or []
            if (item.get("trackId") or item.get("track_id")) == track["trackId"]
        ),
        None,
    )
    if not obj:
        return hits

    presence_tracker = get_zone_presence_tracker()
    transitions_by_zone: dict[str, str | None] = {}

    for rule in rules:
        if not rule.enabled:
            continue

        is_inside = object_in_zone(zone_mapping, rule.zone_id)

        if rule.rule_type in ("PERSON_ENTER", "PERSON_EXIT") and track.get("class") == "person":
            if rule.zone_id not in transitions_by_zone:
                transitions_by_zone[rule.zone_id] = presence_tracker.update(
                    track["cameraId"],
                    track["trackId"],
                    rule.zone_id,
                    is_inside,
                )
            transition = transitions_by_zone[rule.zone_id]

            if rule.rule_type == "PERSON_ENTER" and transition == PRESENCE_ENTER:
                hits.append(
                    _build_hit(
                        rule,
                        track,
                        observation,
                        obj,
                        confidence=obj.get("confidence", 0.9),
                        extra={"transition": "OUTSIDE->INSIDE"},
                    )
                )
            elif rule.rule_type == "PERSON_EXIT" and transition == PRESENCE_EXIT:
                hits.append(
                    _build_hit(
                        rule,
                        track,
                        observation,
                        obj,
                        confidence=obj.get("confidence", 0.9),
                        extra={"transition": "INSIDE->OUTSIDE"},
                    )
                )
            continue

        if not is_inside:
            continue

        if rule.rule_type == "ANIMAL_ENTER" and track.get("class") == "animal":
            hits.append(_build_hit(rule, track, observation, obj, confidence=obj.get("confidence", 0.9)))
        elif rule.rule_type == "PPE_REQUIRED" and track.get("class") == "person":
            required = (rule.config or {}).get("requiredPPE") or (rule.config or {}).get("required_ppe") or []
            attrs = obj.get("attributes") or {}
            missing = [item for item in required if not attrs.get(item)]
            if missing:
                hits.append(
                    _build_hit(
                        rule,
                        track,
                        observation,
                        obj,
                        confidence=obj.get("confidence", 0.9),
                        extra={"missingPPE": missing},
                    )
                )

    return hits


def _evaluate_zone_rules(
    db: Session,
    observation: dict[str, Any],
    zones: list[dict[str, Any]],
    mappings: list[dict[str, Any]],
    track_store,
) -> None:
    camera_id = observation["camera_id"]
    rules = list_rules_for_camera(db, camera_id)
    zone_level = [rule for rule in rules if rule.enabled and rule.rule_type == "PERSON_COUNT"]

    for rule in zone_level:
        zone = next((item for item in zones if item["id"] == rule.zone_id), None)
        if not zone:
            continue

        max_persons = (rule.config or {}).get("maxPersons") or (rule.config or {}).get("max_persons")
        if max_persons is None:
            continue

        persons_in_zone = [
            track
            for track in track_store.get_tracks_by_camera(camera_id)
            if track.get("class") == "person"
            and (
                track.get("currentZoneId") == rule.zone_id
                or track.get("currentSubZoneId") == rule.zone_id
            )
        ]
        if len(persons_in_zone) <= max_persons:
            continue

        confidence = max((track.get("metadata") or {}).get("confidence") or 0 for track in persons_in_zone)
        hit = {
            "ruleId": rule.id,
            "zoneId": rule.zone_id,
            "eventType": rule.rule_type,
            "evaluator": "PERSON_COUNT",
            "eventPayload": {
                "camera_id": camera_id,
                "zone_id": rule.zone_id,
                "rule_id": rule.id,
                "event_type": rule.rule_type,
                "severity": rule.severity,
                "confidence_score": confidence,
                "observation_id": observation.get("id"),
                "event_metadata": {
                    "evaluator": "PERSON_COUNT",
                    "personCount": len(persons_in_zone),
                    "maxPersons": max_persons,
                    "trackIds": [track["trackId"] for track in persons_in_zone],
                },
            },
        }
        _publish(topics.RULE_EVALUATED, hit)
        create_event_from_evaluation(db, EventEngineCreate(**hit["eventPayload"]))


def _build_hit(rule, track, observation, obj, confidence: float, extra: Optional[dict] = None) -> dict[str, Any]:
    metadata = {
        "evaluator": rule.rule_type,
        "trackId": track["trackId"],
        **(extra or {}),
    }
    return {
        "ruleId": rule.id,
        "zoneId": rule.zone_id,
        "eventType": rule.rule_type,
        "evaluator": rule.rule_type,
        "eventPayload": {
            "camera_id": track["cameraId"],
            "zone_id": rule.zone_id,
            "rule_id": rule.id,
            "event_type": rule.rule_type,
            "severity": rule.severity,
            "confidence_score": confidence,
            "observation_id": observation.get("id"),
            "event_metadata": metadata,
        },
    }


def register_pipeline_subscribers() -> None:
    bus = get_event_bus()
    bus.subscribe(topics.OBSERVATION_CREATED, handle_observation_created)
    bus.subscribe(topics.TRACK_UPDATED, handle_track_updated)
    bus.subscribe(topics.EVENT_CREATED, handle_event_created)
    logger.info("Pipeline subscribers registered on EventBus")
