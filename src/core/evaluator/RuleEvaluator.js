import { resolveTrackId } from '../tracking/Track'

const ZONE_LEVEL_RULE_TYPES = new Set(['PERSON_COUNT'])

/**
 * @typedef {object} EvaluationContext
 * @property {object|null} track
 * @property {object} state
 * @property {object} observation
 * @property {object} rule
 * @property {object} zone
 * @property {object|null} zoneMapping
 * @property {object|null} object
 * @property {Array<object>} tracksInZone
 * @property {object|null} stateEngine
 */

export class RuleEvaluator {
  /** @returns {string} */
  get ruleType() {
    throw new Error('ruleType must be implemented')
  }

  get evaluationMode() {
    return ZONE_LEVEL_RULE_TYPES.has(this.ruleType) ? 'zone' : 'track'
  }

  /**
   * @param {EvaluationContext} context
   * @returns {Array<object>}
   */
  evaluate(context) {
    throw new Error('evaluate() must be implemented')
  }

  isTrackInRuleZone(context) {
    const { track, rule, zoneMapping } = context
    if (!track || !zoneMapping) return false
    return (
      zoneMapping.zones.includes(rule.zone_id) ||
      zoneMapping.subzones.includes(rule.zone_id) ||
      track.currentZoneId === rule.zone_id ||
      track.currentSubZoneId === rule.zone_id
    )
  }

  matchesClass(track, objectItem, expectedClass) {
    const value = track?.class || objectItem?.class
    return !expectedClass || value === expectedClass
  }
}

export class PersonEnterEvaluator extends RuleEvaluator {
  get ruleType() {
    return 'PERSON_ENTER'
  }

  evaluate(context) {
    const { track, state, observation, rule, zone, zoneMapping, object } = context
    if (!track || !object || !this.isTrackInRuleZone(context)) return []
    if (!this.matchesClass(track, object, 'person')) return []

    const ruleState = state.ruleStates?.[rule.id] || {}
    if (ruleState.enterTriggered && ruleState.zoneId === zone.id) return []

    return [{
      ruleId: rule.id,
      zoneId: zone.id,
      eventType: rule.rule_type,
      severity: rule.severity,
      confidenceScore: object.confidence,
      metadata: {
        trackId: resolveTrackId(object),
        evaluator: this.ruleType,
        firstSeenAt: track.firstSeenAt,
      },
      statePatch: {
        ruleStates: {
          [rule.id]: {
            enterTriggered: true,
            zoneId: zone.id,
            triggeredAt: observation.timestamp || observation.created_at,
          },
        },
      },
    }]
  }
}

export class PersonDwellEvaluator extends RuleEvaluator {
  get ruleType() {
    return 'PERSON_DWELL'
  }

  evaluate(context) {
    const { track, state, observation, rule, zone, object, stateEngine } = context
    if (!track || !object || !stateEngine || !this.isTrackInRuleZone(context)) return []
    if (!this.matchesClass(track, object, 'person')) return []
    if (stateEngine.hasDwellTriggered(track.cameraId, track.trackId, rule.id)) return []

    const minDwellSeconds = rule.config?.minDwellSeconds ?? rule.config?.min_dwell_seconds ?? 0
    if (!minDwellSeconds) return []

    const dwellSeconds = stateEngine.getDwellSeconds(
      track.cameraId,
      track.trackId,
      zone.id,
      observation.timestamp || observation.created_at,
    )

    if (dwellSeconds < minDwellSeconds) return []

    return [{
      ruleId: rule.id,
      zoneId: zone.id,
      eventType: rule.rule_type,
      severity: rule.severity,
      confidenceScore: object.confidence,
      metadata: {
        trackId: track.trackId,
        evaluator: this.ruleType,
        dwellSeconds,
        minDwellSeconds,
      },
      markDwellTriggered: true,
    }]
  }
}

export class PersonCountEvaluator extends RuleEvaluator {
  get ruleType() {
    return 'PERSON_COUNT'
  }

  evaluate(context) {
    const { rule, zone, tracksInZone = [] } = context
    const maxPersons = rule.config?.maxPersons ?? rule.config?.max_persons
    if (maxPersons == null) return []

    const persons = tracksInZone.filter((track) => track.class === 'person')
    if (persons.length <= maxPersons) return []

    const topConfidence = Math.max(
      ...persons.map((track) => track.metadata?.confidence || 0),
    )

    return [{
      ruleId: rule.id,
      zoneId: zone.id,
      eventType: rule.rule_type,
      severity: rule.severity,
      confidenceScore: topConfidence,
      metadata: {
        evaluator: this.ruleType,
        personCount: persons.length,
        maxPersons,
        trackIds: persons.map((track) => track.trackId),
      },
    }]
  }
}

export class AnimalEnterEvaluator extends RuleEvaluator {
  get ruleType() {
    return 'ANIMAL_ENTER'
  }

  evaluate(context) {
    const { track, state, observation, rule, zone, object } = context
    if (!track || !object || !this.isTrackInRuleZone(context)) return []
    if (!this.matchesClass(track, object, 'animal')) return []

    const ruleState = state.ruleStates?.[rule.id] || {}
    if (ruleState.enterTriggered && ruleState.zoneId === zone.id) return []

    return [{
      ruleId: rule.id,
      zoneId: zone.id,
      eventType: rule.rule_type,
      severity: rule.severity,
      confidenceScore: object.confidence,
      metadata: {
        trackId: track.trackId,
        evaluator: this.ruleType,
      },
      statePatch: {
        ruleStates: {
          [rule.id]: {
            enterTriggered: true,
            zoneId: zone.id,
            triggeredAt: observation.timestamp || observation.created_at,
          },
        },
      },
    }]
  }
}

export class PpeRequiredEvaluator extends RuleEvaluator {
  get ruleType() {
    return 'PPE_REQUIRED'
  }

  evaluate(context) {
    const { track, object, rule, zone } = context
    if (!track || !object || !this.isTrackInRuleZone(context)) return []
    if (!this.matchesClass(track, object, 'person')) return []

    const required = rule.config?.requiredPPE || rule.config?.required_ppe || []
    if (!required.length) return []

    const attributes = object.attributes || track.metadata?.attributes || {}
    const missing = required.filter((item) => !attributes[item])
    if (!missing.length) return []

    return [{
      ruleId: rule.id,
      zoneId: zone.id,
      eventType: rule.rule_type,
      severity: rule.severity,
      confidenceScore: object.confidence,
      metadata: {
        trackId: track.trackId,
        evaluator: this.ruleType,
        missingPPE: missing,
      },
    }]
  }
}

export class HandwashRequiredEvaluator extends RuleEvaluator {
  get ruleType() {
    return 'HANDWASH_REQUIRED'
  }

  evaluate(context) {
    const { track, state, observation, rule, zone, object } = context
    if (!track || !object || !this.isTrackInRuleZone(context)) return []
    if (!this.matchesClass(track, object, 'person')) return []

    const transitions = state.transitions || []
    const sequence = rule.config?.sequence || []

    return [{
      ruleId: rule.id,
      zoneId: zone.id,
      eventType: rule.rule_type,
      severity: rule.severity,
      confidenceScore: object.confidence,
      metadata: {
        trackId: track.trackId,
        evaluator: this.ruleType,
        transitions,
        configuredSteps: sequence.length,
        note: sequence.length
          ? 'Handwash sequence tracking active — full compliance logic in v1.5'
          : 'Configure rule.config.sequence for multi-step handwash',
      },
    }]
  }
}

export function applyEvaluationStatePatches(stateEngine, track, hits) {
  hits.forEach((hit) => {
    if (hit.statePatch) {
      stateEngine.setState(track.cameraId, track.trackId, hit.statePatch)
    }
    if (hit.markDwellTriggered) {
      stateEngine.markDwellTriggered(track.cameraId, track.trackId, hit.ruleId, hit.zoneId)
    }
  })
}
