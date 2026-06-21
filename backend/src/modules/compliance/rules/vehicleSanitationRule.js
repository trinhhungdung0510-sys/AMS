import { COMPLIANCE_RULE_IDS } from '../complianceRules.js'

/** @type {import('../complianceRules.js').ComplianceRule} */
export const vehicleSanitationRule = {
  id: COMPLIANCE_RULE_IDS.VEHICLE_INTRUSION,
  name: 'Xe xâm nhập / chưa sát trùng',
  eventType: 'VEHICLE_INTRUSION',
  enabled: true,
  evaluate() {
    return { violated: false, score: 0, evidence: {} }
  },
}
