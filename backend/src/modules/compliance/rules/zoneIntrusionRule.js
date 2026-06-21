import { BaseRule, COMPLIANCE_RULE_IDS } from '../BaseRule.js'

export class ZoneIntrusionRule extends BaseRule {
  constructor() {
    super({
      id: COMPLIANCE_RULE_IDS.ZONE_INTRUSION,
      name: 'Xâm nhập vùng cấm',
      eventType: 'ZONE_INTRUSION',
    })
  }

  async evaluate() {
    return { violated: false, score: 0, evidence: {} }
  }
}
