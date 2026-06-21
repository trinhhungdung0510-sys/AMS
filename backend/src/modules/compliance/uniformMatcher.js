import { getComplianceConfig } from '../../config/compliance.js'

/**
 * @param {Buffer|string|null} personImage
 * @param {string[]} templateImages
 * @param {{ trackId?: number|null, templateId?: string|null }} [options]
 */
export async function matchUniform(personImage, templateImages, options = {}) {
  const config = getComplianceConfig()
  const seed = `${options.trackId}:${options.templateId}:${templateImages.length}:${(personImage || '').length || 0}`
  let hash = 0
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) >>> 0
  }
  const score = Math.round((0.75 + (hash % 25) / 100) * 100) / 100
  const matched = score >= config.uniformThreshold
  return { score, matched }
}
