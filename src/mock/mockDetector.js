/**
 * @deprecated Use src/core/detectors/MockDetectorAdapter.js
 */
export {
  listMockScenarios,
  MockDetectorAdapter,
  defaultMockDetectorAdapter,
} from '../core/detectors/MockDetectorAdapter'

import { defaultMockDetectorAdapter } from '../core/detectors/MockDetectorAdapter'

export function generateMockObservation(cameraId, scenarioKey, frameSize = { width: 1920, height: 1080 }) {
  return defaultMockDetectorAdapter.detect({
    cameraId,
    scenarioKey,
    frameWidth: frameSize.width,
    frameHeight: frameSize.height,
  })
}
