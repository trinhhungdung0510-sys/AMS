import { BaseRule, COMPLIANCE_RULE_IDS } from '../BaseRule.js'
import { getComplianceConfig } from '../../../config/compliance.js'
import { matchUniform } from '../uniformMatcher.js'

export class UniformRule extends BaseRule {
  constructor() {
    super({
      id: COMPLIANCE_RULE_IDS.UNIFORM_VIOLATION,
      name: 'Sai đồng phục bảo hộ',
      eventType: 'UNIFORM_VIOLATION',
    })
  }

  async evaluate(context) {
    if (context.triggerEvent !== 'PERSON_ENTER') {
      return { violated: false, score: 0, evidence: {} }
    }

    const requiredUniformId = context.requiredUniformId
    if (!requiredUniformId) {
      return { violated: false, score: 1, evidence: { reason: 'no_required_uniform' } }
    }

    const templateImages = context.templateImages || []
    const match = await matchUniform(context.personSnapshot || null, templateImages, {
      trackId: context.trackId,
      templateId: requiredUniformId,
    })

    const config = getComplianceConfig()
    if (match.score >= config.uniformThreshold) {
      return { violated: false, score: match.score, evidence: { matched: match.matched } }
    }

    return {
      violated: true,
      score: match.score,
      evidence: { eventType: 'UNIFORM_VIOLATION', matched: match.matched },
    }
  }
}
