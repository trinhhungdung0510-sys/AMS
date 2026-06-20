"""Event bus topic constants — AMS v1.5."""

OBSERVATION_CREATED = "observation.created"
TRACK_UPDATED = "track.updated"
RULE_EVALUATED = "rule.evaluated"
EVENT_CREATED = "event.created"
NOTIFICATION_CREATED = "notification.created"
CAMERA_STATUS_CHANGED = "camera.status"

ALL_TOPICS = {
    OBSERVATION_CREATED,
    TRACK_UPDATED,
    RULE_EVALUATED,
    EVENT_CREATED,
    NOTIFICATION_CREATED,
    CAMERA_STATUS_CHANGED,
}
