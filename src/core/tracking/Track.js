/**
 * Runtime track model — continuity layer between observations.
 */

export function createTrack({
  trackId,
  cameraId,
  objectClass,
  timestamp,
  currentZoneId = null,
  currentSubZoneId = null,
  metadata = {},
}) {
  if (!trackId) throw new Error('trackId is required')
  if (!cameraId) throw new Error('cameraId is required')

  return {
    trackId,
    cameraId,
    class: objectClass,
    firstSeenAt: timestamp,
    lastSeenAt: timestamp,
    currentZoneId,
    currentSubZoneId,
    metadata: { ...metadata },
  }
}

export function trackKey(cameraId, trackId) {
  return `${cameraId}:${trackId}`
}

export function resolveTrackId(objectItem) {
  return objectItem.trackId || objectItem.track_id
}

export function resolveObjectClass(objectItem) {
  return objectItem.class || objectItem.object_class
}

export function updateTrackFromObservation(track, {
  timestamp,
  currentZoneId,
  currentSubZoneId,
  metadata,
}) {
  return {
    ...track,
    lastSeenAt: timestamp,
    currentZoneId: currentZoneId ?? track.currentZoneId,
    currentSubZoneId: currentSubZoneId ?? track.currentSubZoneId,
    metadata: {
      ...track.metadata,
      ...metadata,
    },
  }
}
