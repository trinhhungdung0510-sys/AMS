import { COMPLIANCE_RULE_IDS } from '../complianceRules.js'

/** @type {import('../complianceRules.js').ComplianceRule} */
export const animalIntrusionRule = {
  id: COMPLIANCE_RULE_IDS.ANIMAL_INTRUSION,
  name: 'Động vật xâm nhập',
  eventType: 'ANIMAL_INTRUSION',
  enabled: true,
  evaluate() {
    return { violated: false, score: 0, evidence: {} }
  },
}
