import { COMPLIANCE_RULE_IDS } from '../complianceRules.js'

/** @type {import('../complianceRules.js').ComplianceRule} */
export const handSanitationRule = {
  id: COMPLIANCE_RULE_IDS.NO_HAND_SANITIZATION,
  name: 'Không rửa tay sát trùng',
  eventType: 'NO_HAND_SANITIZATION',
  enabled: true,
  evaluate() {
    return { violated: false, score: 0, evidence: {} }
  },
}
