/**
 * @typedef {Object} ComplianceEvaluationResult
 * @property {boolean} violated
 * @property {number} score
 * @property {Record<string, unknown>} evidence
 */

/**
 * @typedef {Object} ComplianceRule
 * @property {string} id
 * @property {string} name
 * @property {boolean} enabled
 * @property {(context: Record<string, unknown>) => ComplianceEvaluationResult} evaluate
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

export const COMPLIANCE_RULE_IDS = {
  ZONE_INTRUSION: 'ZONE_INTRUSION',
  NO_HAND_SANITIZATION: 'NO_HAND_SANITIZATION',
  NO_BOOT_SANITIZATION: 'NO_BOOT_SANITIZATION',
  ANIMAL_INTRUSION: 'ANIMAL_INTRUSION',
  VEHICLE_INTRUSION: 'VEHICLE_INTRUSION',
  UNIFORM_VIOLATION: 'UNIFORM_VIOLATION',
}

export const COMPLIANCE_RULE_DEFINITIONS = [
  { id: 'ZONE_INTRUSION', name: 'Xâm nhập vùng cấm', eventType: 'ZONE_INTRUSION' },
  { id: 'NO_HAND_SANITIZATION', name: 'Không rửa tay sát trùng', eventType: 'NO_HAND_SANITIZATION' },
  { id: 'NO_BOOT_SANITIZATION', name: 'Không sát trùng ủng', eventType: 'NO_BOOT_SANITIZATION' },
  { id: 'ANIMAL_INTRUSION', name: 'Động vật xâm nhập', eventType: 'ANIMAL_INTRUSION' },
  { id: 'VEHICLE_INTRUSION', name: 'Xe xâm nhập / chưa sát trùng', eventType: 'VEHICLE_INTRUSION' },
  { id: 'UNIFORM_VIOLATION', name: 'Sai đồng phục bảo hộ', eventType: 'UNIFORM_VIOLATION' },
]
