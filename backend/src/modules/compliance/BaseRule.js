/**
 * @typedef {Object} ComplianceEvaluationResult
 * @property {boolean} violated
 * @property {number} score
 * @property {Record<string, unknown>} [evidence]
 */

/**
 * @typedef {Object} ComplianceRule
 * @property {string} id
 * @property {string} name
 * @property {boolean} enabled
 * @property {string} [eventType]
 * @property {(context: Record<string, unknown>) => ComplianceEvaluationResult | Promise<ComplianceEvaluationResult>} evaluate
 */

/**
 * @typedef {Object} ComplianceViolationEvent
 * @property {string} eventType
 * @property {string} ruleId
 * @property {string} ruleName
 * @property {string} cameraId
 * @property {string} zoneId
 * @property {number|null} trackId
 * @property {number} score
 * @property {string|null} snapshotPath
 * @property {string} timestamp
 */

export class BaseRule {
  constructor({ id, name, eventType, enabled = true }) {
    this.id = id
    this.name = name
    this.eventType = eventType || id
    this.enabled = enabled
  }

  async evaluate(_context) {
    throw new Error('evaluate() must be implemented')
  }
}

export const COMPLIANCE_RULE_IDS = {
  ZONE_INTRUSION: 'ZONE_INTRUSION',
  NO_HAND_SANITIZATION: 'NO_HAND_SANITIZATION',
  NO_BOOT_SANITIZATION: 'NO_BOOT_SANITIZATION',
  ANIMAL_INTRUSION: 'ANIMAL_INTRUSION',
  VEHICLE_INTRUSION: 'VEHICLE_INTRUSION',
  UNIFORM_VIOLATION: 'UNIFORM_VIOLATION',
}
