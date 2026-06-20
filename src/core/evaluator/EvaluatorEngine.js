import { findMappingForObject } from '../zoneMapper'
import { resolveTrackId } from '../tracking/Track'
import {
  AnimalEnterEvaluator,
  applyEvaluationStatePatches,
  HandwashRequiredEvaluator,
  PersonCountEvaluator,
  PersonDwellEvaluator,
  PersonEnterEvaluator,
  PersonExitEvaluator,
  PpeRequiredEvaluator,
} from './RuleEvaluator'
import { defaultZonePresenceTracker } from '../runtime/ZonePresenceTracker'

const EVALUATORS = [
  new PersonEnterEvaluator(),
  new PersonExitEvaluator(),
  new PersonDwellEvaluator(),
  new PersonCountEvaluator(),
  new AnimalEnterEvaluator(),
  new PpeRequiredEvaluator(),
  new HandwashRequiredEvaluator(),
]

export class EvaluatorEngine {
  constructor(evaluators = EVALUATORS, zonePresenceTracker = defaultZonePresenceTracker) {
    this.evaluators = evaluators
    this.zonePresenceTracker = zonePresenceTracker
    this.evaluatorByType = Object.fromEntries(
      evaluators.map((evaluator) => [evaluator.ruleType, evaluator]),
    )
  }

  resolveTrackInZone(track, zoneMapping, zoneId) {
    if (!track || !zoneMapping) return false
    return (
      zoneMapping.zones.includes(zoneId) ||
      zoneMapping.subzones.includes(zoneId) ||
      track.currentZoneId === zoneId ||
      track.currentSubZoneId === zoneId
    )
  }

  evaluate({
    observation,
    rules,
    zones,
    zoneMappings,
    trackStore,
    stateEngine,
  }) {
    const zoneById = Object.fromEntries((zones || []).map((zone) => [zone.id, zone]))
    const cameraId = observation.camera_id || observation.cameraId
    const results = []
    const transitionByTrackZone = new Map()

    const resolveTransition = (trackId, zoneId, isInside) => {
      const cacheKey = `${trackId}:${zoneId}`
      if (!transitionByTrackZone.has(cacheKey)) {
        transitionByTrackZone.set(
          cacheKey,
          this.zonePresenceTracker.update(cameraId, trackId, zoneId, isInside),
        )
      }
      return transitionByTrackZone.get(cacheKey)
    }

    ;(rules || [])
      .filter((rule) => rule.enabled)
      .forEach((rule) => {
        const evaluator = this.evaluatorByType[rule.rule_type]
        if (!evaluator) return

        const zone = zoneById[rule.zone_id]
        if (!zone) return

        if (evaluator.evaluationMode === 'zone') {
          const tracksInZone = (trackStore?.getTracksByCamera(cameraId) || []).filter(
            (track) => track.currentZoneId === zone.id || track.currentSubZoneId === zone.id,
          )

          const hits = evaluator.evaluate({
            track: null,
            state: {},
            observation,
            rule,
            zone,
            zoneMapping: null,
            object: null,
            tracksInZone,
            stateEngine,
          })

          hits.forEach((hit) => {
            results.push({
              ...hit,
              cameraId,
              observationId: observation.id,
            })
          })
          return
        }

        ;(observation.objects || []).forEach((objectItem) => {
          const trackId = resolveTrackId(objectItem)
          const track = trackStore?.getTrack(cameraId, trackId)
          if (!track) return

          const zoneMapping = findMappingForObject(zoneMappings, trackId)
          const state = stateEngine?.getState(cameraId, trackId) || {}
          const isInside = this.resolveTrackInZone(track, zoneMapping, rule.zone_id)
          const transition = resolveTransition(trackId, rule.zone_id, isInside)

          const hits = evaluator.evaluate({
            track,
            state,
            observation,
            rule,
            zone,
            zoneMapping,
            object: objectItem,
            tracksInZone: [],
            stateEngine,
            transition,
          })

          applyEvaluationStatePatches(stateEngine, track, hits)

          hits.forEach((hit) => {
            const { statePatch, markDwellTriggered, ...result } = hit
            results.push({
              ...result,
              cameraId,
              observationId: observation.id,
            })
          })
        })
      })

    return results
  }
}

export const defaultEvaluatorEngine = new EvaluatorEngine()
