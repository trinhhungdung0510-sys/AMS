import { getWorkflowManager, stepForZone } from './workflowManager.js'
import { getWorkflowStateStore } from './workflowStateStore.js'

export const BIOSECURITY_PROCESS_VIOLATION = 'BIOSECURITY_PROCESS_VIOLATION'

export const STEP_LABELS_VI = {
  ENTER_SHOWER: 'Vào khu tắm',
  HAND_SANITIZATION: 'Sát trùng tay',
  BOOT_SANITIZATION: 'Sát trùng ủng',
  ENTER_CLEAN_ZONE: 'Vào vùng sạch',
}

/**
 * @typedef {object} WorkflowEvaluationContext
 * @property {string} cameraId
 * @property {number} trackId
 * @property {string} zoneCode
 * @property {string} timestamp
 * @property {string} [objectType]
 * @property {string} [workflowId]
 */

export class WorkflowEngine {
  constructor() {
    this._manager = getWorkflowManager()
    this._store = getWorkflowStateStore()
  }

  /** @param {WorkflowEvaluationContext} context */
  evaluate(context) {
    if ((context.objectType || 'person').toLowerCase() !== 'person') {
      return []
    }

    const definitions = context.workflowId
      ? [this._manager.getDefinition(context.workflowId)].filter(Boolean)
      : this._manager.listDefinitions()

    return definitions
      .map((definition) => this._evaluateDefinition(context, definition))
      .filter(Boolean)
  }

  /** @param {WorkflowEvaluationContext} context @param {import('./workflowManager.js').WorkflowDefinition} definition */
  _evaluateDefinition(context, definition) {
    const stepCode = stepForZone(definition, context.zoneCode)
    if (!stepCode) {
      return null
    }

    const state = this._store.getState(context.cameraId, context.trackId, definition.id)
    const completed = [...state.completedSteps]

    if (completed.includes(stepCode)) {
      return {
        workflowId: definition.id,
        workflowName: definition.name,
        compliant: true,
        violated: false,
        currentStep: stepCode,
        completedSteps: completed,
        evidence: { status: 'step_already_completed', step: stepCode },
      }
    }

    const expectedIndex = completed.length
    const actualIndex = definition.steps.indexOf(stepCode)
    const skipped = definition.steps.slice(expectedIndex, actualIndex)

    if (skipped.length > 0) {
      const skippedLabels = skipped.map((code) => STEP_LABELS_VI[code] || code)
      console.warn(
        `[Workflow] VIOLATION workflow=${definition.id} track=${context.trackId} skipped=${skipped.join(',')} attempted=${stepCode}`,
      )
      return {
        workflowId: definition.id,
        workflowName: definition.name,
        compliant: false,
        violated: true,
        eventType: BIOSECURITY_PROCESS_VIOLATION,
        score: 0.35,
        currentStep: stepCode,
        skippedSteps: skipped,
        completedSteps: completed,
        evidence: {
          workflowId: definition.id,
          workflowName: definition.name,
          attemptedStep: stepCode,
          skippedSteps: skipped,
          skippedStepLabels: skippedLabels,
          zoneCode: context.zoneCode,
        },
      }
    }

    const updated = this._store.markStepCompleted({
      cameraId: context.cameraId,
      trackId: context.trackId,
      workflowId: definition.id,
      stepCode,
      zoneCode: context.zoneCode,
      timestamp: context.timestamp,
    })

    console.info(
      `[Workflow] PASSED workflow=${definition.id} track=${context.trackId} step=${stepCode} zone=${context.zoneCode}`,
    )

    return {
      workflowId: definition.id,
      workflowName: definition.name,
      compliant: true,
      violated: false,
      score: 1.0,
      currentStep: stepCode,
      completedSteps: [...updated.completedSteps],
      evidence: { status: 'step_completed', step: stepCode },
    }
  }
}

let _engine = null

export function getWorkflowEngine() {
  if (!_engine) {
    _engine = new WorkflowEngine()
  }
  return _engine
}

export function resetWorkflowEngine() {
  _engine = null
}
