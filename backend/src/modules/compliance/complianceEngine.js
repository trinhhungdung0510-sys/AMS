/** @typedef {import('../modules/compliance/complianceRules.js').ComplianceRule} ComplianceRule */
/** @typedef {import('../modules/compliance/complianceRules.js').ComplianceEvaluationResult} ComplianceEvaluationResult */
/** @typedef {import('../modules/compliance/complianceRules.js').ComplianceViolationEvent} ComplianceViolationEvent */

export class ComplianceEngine {
  constructor() {
    /** @type {ComplianceRule[]} */
    this.rules = []
  }

  /** @param {ComplianceRule} rule */
  registerRule(rule) {
    this.rules.push(rule)
  }

  /**
   * @param {Record<string, unknown>} context
   * @returns {Promise<ComplianceViolationEvent[]>}
   */
  async evaluate(context) {
    const violations = []

    for (const rule of this.rules) {
      if (!rule.enabled) continue

      const result = await rule.evaluate(context)
      this._logResult(rule, context, result)

      if (!result.violated) continue

      const violation = this._buildViolation(rule, context, result)
      violations.push(violation)
      await this.emitViolation(context, violation)
    }

    return violations
  }

  /**
   * @param {Record<string, unknown>} context
   * @param {ComplianceViolationEvent} violation
   */
  async emitViolation(context, violation) {
    return violation
  }

  /** @param {ComplianceRule} rule @param {Record<string, unknown>} context @param {ComplianceEvaluationResult} result */
  _logResult(rule, context, result) {
    const zone = context.zoneName || context.zoneId || '-'
    const track = context.trackId ?? '-'
    const status = result.violated ? 'VIOLATED' : 'PASSED'
    console.info(
      `[Compliance] Rule: ${rule.name} Track: ${track} Zone: ${zone} Score: ${Number(result.score).toFixed(2)} Result: ${status}`,
    )
  }

  /** @param {ComplianceRule} rule @param {Record<string, unknown>} context @param {ComplianceEvaluationResult} result */
  _buildViolation(rule, context, result) {
    return {
      eventType: rule.eventType || rule.id,
      ruleId: rule.id,
      ruleName: rule.name,
      cameraId: context.cameraId || '',
      zoneId: context.zoneId || '',
      trackId: context.trackId ?? null,
      score: result.score,
      snapshotPath: context.snapshotPath || null,
      timestamp: context.timestamp || '',
      evidence: result.evidence || {},
    }
  }
}

export function createComplianceEngine() {
  return new ComplianceEngine()
}
