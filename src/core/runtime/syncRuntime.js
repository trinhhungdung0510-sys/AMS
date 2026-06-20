import { mapObservationToZones } from '../zoneMapper'
import { defaultStateEngine } from './StateEngine'
import { defaultTrackStore } from '../tracking/TrackStore'

/**
 * Sync TrackStore + StateEngine from a persisted observation.
 */
export function syncRuntimeFromObservation({
  observation,
  zones,
  zoneMappings,
  trackStore = defaultTrackStore,
  stateEngine = defaultStateEngine,
}) {
  const cameraId = observation.camera_id || observation.cameraId
  const timestamp = observation.timestamp || observation.created_at
  const mappingsByObjectId = Object.fromEntries(
    (zoneMappings || []).map((mapping) => [mapping.objectId, mapping]),
  )

  const tracks = []

  ;(observation.objects || []).forEach((objectItem) => {
    const trackId = objectItem.trackId || objectItem.track_id
    const { track, previousTrack } = trackStore.upsertFromObservationObject({
      cameraId,
      timestamp,
      objectItem,
      zoneMapping: mappingsByObjectId[trackId] || null,
      observationId: observation.id,
    })

    stateEngine.processTrackUpdate({
      track,
      previousTrack,
      timestamp,
      zones,
    })

    tracks.push(track)
  })

  return tracks
}
