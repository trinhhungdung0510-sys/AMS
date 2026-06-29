"""Event bus topic constants — AMS v1.5."""

OBSERVATION_CREATED = "observation.created"
TRACK_UPDATED = "track.updated"
RULE_EVALUATED = "rule.evaluated"
EVENT_CREATED = "event.created"
EVENT_UPDATED = "event.updated"
EVENT_REMOVED = "event.removed"
NOTIFICATION_CREATED = "notification.created"
NOTIFICATION_GMAIL_FAILED = "notification.gmail_failed"
CAMERA_STATUS_CHANGED = "camera.status"

DETECTOR_STARTED = "detector.started"
DETECTOR_STOPPED = "detector.stopped"
DETECTOR_FAILED = "detector.failed"
DETECTOR_RECOVERED = "detector.recovered"

ALL_TOPICS = {
    OBSERVATION_CREATED,
    TRACK_UPDATED,
    RULE_EVALUATED,
    EVENT_CREATED,
    EVENT_UPDATED,
    EVENT_REMOVED,
    NOTIFICATION_CREATED,
    NOTIFICATION_GMAIL_FAILED,
    CAMERA_STATUS_CHANGED,
    DETECTOR_STARTED,
    DETECTOR_STOPPED,
    DETECTOR_FAILED,
    DETECTOR_RECOVERED,
}
