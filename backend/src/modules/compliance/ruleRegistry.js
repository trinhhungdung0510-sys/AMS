import {
  AnimalIntrusionRule,
  BootSanitationRule,
  HandSanitationRule,
  VehicleSanitationRule,
} from './rules/index.js'
import { ComplianceEngine } from './complianceEngine.js'
import { UniformRule } from './rules/uniformRule.js'
import { ZoneIntrusionRule } from './rules/zoneIntrusionRule.js'

export const RULE_REGISTRY = [
  ZoneIntrusionRule,
  UniformRule,
  AnimalIntrusionRule,
  HandSanitationRule,
  BootSanitationRule,
  VehicleSanitationRule,
]

export function loadComplianceRules() {
  return RULE_REGISTRY.map((RuleClass) => new RuleClass())
}

export function createEngineFromRegistry() {
  const engine = new ComplianceEngine()
  for (const rule of loadComplianceRules()) {
    engine.registerRule(rule)
  }
  return engine
}
