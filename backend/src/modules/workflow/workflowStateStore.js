export class WorkflowStateStore {
  constructor() {
    /** @type {Map<string, { workflowId: string, completedSteps: string[], lastZone: string, updatedAt: string }>} */
    this._states = new Map()
  }

  /** @param {string} cameraId @param {number} trackId @param {string} workflowId */
  _key(cameraId, trackId, workflowId) {
    return `${cameraId}:${trackId}:${workflowId}`
  }

  /** @param {string} cameraId @param {number} trackId @param {string} workflowId */
  getState(cameraId, trackId, workflowId) {
    const key = this._key(cameraId, trackId, workflowId)
    let state = this._states.get(key)
    if (!state) {
      state = { workflowId, completedSteps: [], lastZone: '', updatedAt: '' }
      this._states.set(key, state)
    }
    return state
  }

  /**
   * @param {object} params
   * @param {string} params.cameraId
   * @param {number} params.trackId
   * @param {string} params.workflowId
   * @param {string} params.stepCode
   * @param {string} params.zoneCode
   * @param {string} params.timestamp
   */
  markStepCompleted({ cameraId, trackId, workflowId, stepCode, zoneCode, timestamp }) {
    const state = this.getState(cameraId, trackId, workflowId)
    if (!state.completedSteps.includes(stepCode)) {
      state.completedSteps.push(stepCode)
    }
    state.lastZone = zoneCode
    state.updatedAt = timestamp
    return state
  }

  /** @param {string} cameraId @param {number} trackId @param {string} workflowId */
  reset(cameraId, trackId, workflowId) {
    this._states.delete(this._key(cameraId, trackId, workflowId))
  }
}

let _store = null

export function getWorkflowStateStore() {
  if (!_store) {
    _store = new WorkflowStateStore()
  }
  return _store
}

export function resetWorkflowStateStore() {
  _store = new WorkflowStateStore()
}
