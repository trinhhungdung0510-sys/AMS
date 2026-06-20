import { findMappingForObject } from '../zoneMapper'
import { resolveTrackId } from '../tracking/Track'
import {
  AnimalEnterEvaluator,
  applyEvaluationStatePatches,
  HandwashRequiredEvaluator,
  PersonCountEvaluator,
  PersonDwellEvaluator,
  PersonEnterEvaluator,
  PpeRequiredEvaluator,
} from './RuleEvaluator'

const EVALUATORS = [
  new PersonEnterEvaluator(),
  new PersonDwellEvaluator(),
  new PersonCountEvaluator(),
  new AnimalEnterEvaluator(),
  new PpeRequiredEvaluator(),
  new HandwashRequiredEvaluator(),
]

export class EvaluatorEngine {
  constructor(evaluators = EVALUATORS) {
    this.evaluators = evaluators
    this.evaluatorByType = Object.fromEntries(
      evaluators.map((evaluator) => [evaluator.ruleType, evaluator]),
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
