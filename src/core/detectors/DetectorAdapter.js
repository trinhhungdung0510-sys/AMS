/**
 * Base detector adapter — normalizes external AI output to Observation payload.
 */
export class DetectorAdapter {
  /** @returns {string} */
  get id() {
    throw new Error('DetectorAdapter.id must be implemented')
  }

  /** @returns {string} MOCK | YOLO | OPENVINO | MANUAL */
  get source() {
    throw new Error('DetectorAdapter.source must be implemented')
  }

  /**
   * @param {object} context
   * @param {string} context.cameraId
   * @param {number} [context.frameWidth=1920]
   * @param {number} [context.frameHeight=1080]
   * @returns {Promise<object>|object} Observation create payload
   */
  detect(context) {
    throw new Error('DetectorAdapter.detect() must be implemented')
  }
}
