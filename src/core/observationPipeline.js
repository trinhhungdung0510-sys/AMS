import { createObservation } from '../services/observationService'

/**
 * v1.5 pipeline entry — persist observation only.
 * Backend EventBus handles TrackStore → Evaluator → Event → Notification.
 * Clients receive updates via /ws/events.
 */
export async function runObservationPipeline({ observationPayload }) {
  const observation = await createObservation(observationPayload)
  return {
    observation,
    zoneMappings: [],
    hits: [],
    events: [],
    tracks: [],
  }
}

export { mapObservationToZones } from './zoneMapper'
