import {
  createTrack,
  resolveObjectClass,
  resolveTrackId,
  trackKey,
  updateTrackFromObservation,
} from './Track'

export class TrackStore {
  constructor() {
    /** @type {Map<string, object>} */
    this.tracks = new Map()
  }

  upsertTrack({
    cameraId,
    trackId,
    objectClass,
    timestamp,
    currentZoneId = null,
    currentSubZoneId = null,
    metadata = {},
  }) {
    const key = trackKey(cameraId, trackId)
    const existing = this.tracks.get(key)

    if (!existing) {
      const track = createTrack({
        trackId,
        cameraId,
        objectClass,
        timestamp,
        currentZoneId,
        currentSubZoneId,
        metadata,
      })
      this.tracks.set(key, track)
      return { track, isNew: true, previousTrack: null }
    }

    const previousTrack = { ...existing }
    const track = updateTrackFromObservation(existing, {
      timestamp,
      currentZoneId,
      currentSubZoneId,
      metadata,
    })
    if (objectClass) track.class = objectClass

    this.tracks.set(key, track)
    return { track, isNew: false, previousTrack }
  }

  upsertFromObservationObject({
    cameraId,
    timestamp,
    objectItem,
    zoneMapping = null,
    observationId = null,
  }) {
    const trackId = resolveTrackId(objectItem)
    const zones = zoneMapping?.zones || []
    const subzones = zoneMapping?.subzones || []

    return this.upsertTrack({
      cameraId,
      trackId,
      objectClass: resolveObjectClass(objectItem),
      timestamp,
      currentZoneId: zones[0] || null,
      currentSubZoneId: subzones[0] || null,
      metadata: {
        confidence: objectItem.confidence,
        bbox: objectItem.bbox,
        attributes: objectItem.attributes || {},
        lastObservationId: observationId,
      },
    })
  }

  getTrack(cameraId, trackId) {
    return this.tracks.get(trackKey(cameraId, trackId)) || null
  }

  removeTrack(cameraId, trackId) {
    return this.tracks.delete(trackKey(cameraId, trackId))
  }

  getTracksByCamera(cameraId) {
    return [...this.tracks.values()].filter((track) => track.cameraId === cameraId)
  }

  clearCamera(cameraId) {
    for (const key of [...this.tracks.keys()]) {
      if (key.startsWith(`${cameraId}:`)) {
        this.tracks.delete(key)
      }
    }
  }

  clear() {
    this.tracks.clear()
  }
}

export const defaultTrackStore = new TrackStore()
