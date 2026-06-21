import { BaseRule, COMPLIANCE_RULE_IDS } from '../BaseRule.js'

function skeletonRule(id, name, eventType) {
  return class extends BaseRule {
    constructor() {
      super({ id, name, eventType })
    }

    async evaluate() {
      return { violated: false, score: 0, evidence: {} }
    }
  }
}

export const HandSanitationRule = skeletonRule(
  COMPLIANCE_RULE_IDS.NO_HAND_SANITIZATION,
  'Không rửa tay sát trùng',
  'NO_HAND_SANITIZATION',
)

export const BootSanitationRule = skeletonRule(
  COMPLIANCE_RULE_IDS.NO_BOOT_SANITIZATION,
  'Không sát trùng ủng',
  'NO_BOOT_SANITIZATION',
)

export const VehicleSanitationRule = skeletonRule(
  COMPLIANCE_RULE_IDS.VEHICLE_INTRUSION,
  'Xe xâm nhập / chưa sát trùng',
  'VEHICLE_INTRUSION',
)

export const AnimalIntrusionRule = skeletonRule(
  COMPLIANCE_RULE_IDS.ANIMAL_INTRUSION,
  'Động vật xâm nhập',
  'ANIMAL_INTRUSION',
)
