import { COMPLIANCE_RULE_IDS } from '../complianceRules.js'

/** @type {import('../complianceRules.js').ComplianceRule} */
export const bootSanitationRule = {
  id: COMPLIANCE_RULE_IDS.NO_BOOT_SANITIZATION,
  name: 'Không sát trùng ủng',
  eventType: 'NO_BOOT_SANITIZATION',
  enabled: true,
  evaluate() {
    return { violated: false, score: 0, evidence: {} }
  },
}
