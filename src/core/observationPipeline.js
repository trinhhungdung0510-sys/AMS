import { defaultEvaluatorEngine } from './evaluator/EvaluatorEngine'
import { mapObservationToZones } from './zoneMapper'
import { defaultMockDetectorAdapter } from './detectors/MockDetectorAdapter'
import { defaultStateEngine } from './runtime/StateEngine'
import { syncRuntimeFromObservation } from './runtime/syncRuntime'
import { defaultTrackStore } from './tracking/TrackStore'
import { createEngineEvent } from '../services/eventService'
import { createObservation } from '../services/observationService'
import { notifyEventCreated } from '../providers/NotificationProvider'

/**
 * Full v1.4.1 pipeline:
 * Detector → Observation → TrackStore → StateEngine → Evaluator → Event
 */
export async function runObservationPipeline({
  observationPayload,
  zones,
  rules,
  trackStore = defaultTrackStore,
  stateEngine = defaultStateEngine,
  evaluatorEngine = defaultEvaluatorEngine,
}) {
  const observation = await createObservation(observationPayload)
  const zoneMappings = mapObservationToZones(observation, zones)

  syncRuntimeFromObservation({
    observation,
    zones,
    zoneMappings,
    trackStore,
    stateEngine,
  })

  const hits = evaluatorEngine.evaluate({
    observation,
    rules,
    zones,
    zoneMappings,
    trackStore,
    stateEngine,
  })

  const events = []
  for (const hit of hits) {
    const event = await createEngineEvent({
      camera_id: hit.cameraId,
      zone_id: hit.zoneId,
      rule_id: hit.ruleId,
      event_type: hit.eventType,
      severity: hit.severity,
      confidence_score: hit.confidenceScore,
      observation_id: hit.observationId,
      event_metadata: hit.metadata,
    })
    notifyEventCreated(event)
    events.push(event)
  }

  return {
    observation,
    zoneMappings,
    hits,
    events,
    tracks: trackStore.getTracksByCamera(observation.camera_id || observation.cameraId),
  }
}

/**
 * Run pipeline using a DetectorAdapter instance.
 */
export async function runDetectorPipeline({
  cameraId,
  zones,
  rules,
  detector = defaultMockDetectorAdapter,
  detectorContext = {},
  trackStore = defaultTrackStore,
  stateEngine = defaultStateEngine,
  evaluatorEngine = defaultEvaluatorEngine,
}) {
  const observationPayload = await detector.detect({
    cameraId,
    ...detectorContext,
  })

  return runObservationPipeline({
    observationPayload,
    zones,
    rules,
    trackStore,
    stateEngine,
    evaluatorEngine,
  })
}

export { mapObservationToZones }
