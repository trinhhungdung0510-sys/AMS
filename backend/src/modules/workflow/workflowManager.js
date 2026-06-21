export const WORKFLOW_STEP_CODES = {
  ENTER_SHOWER: 'ENTER_SHOWER',
  HAND_SANITIZATION: 'HAND_SANITIZATION',
  BOOT_SANITIZATION: 'BOOT_SANITIZATION',
  ENTER_CLEAN_ZONE: 'ENTER_CLEAN_ZONE',
}

export const STEP_ZONE_CODES = {
  [WORKFLOW_STEP_CODES.ENTER_SHOWER]: 'shower_room',
  [WORKFLOW_STEP_CODES.HAND_SANITIZATION]: 'handwash_zone',
  [WORKFLOW_STEP_CODES.BOOT_SANITIZATION]: 'boot_disinfection_tray',
}

export const CLEAN_PRODUCTION_ZONES = new Set([
  'gestation_barn',
  'farrowing_barn',
  'weaning_barn',
  'nursery_barn',
  'boar_barn',
  'quarantine_barn',
])

export const ENTRY_CLEAN_ZONE_WORKFLOW = {
  id: 'entry_clean_zone',
  name: 'Quy trình vào vùng sạch',
  steps: [
    WORKFLOW_STEP_CODES.ENTER_SHOWER,
    WORKFLOW_STEP_CODES.HAND_SANITIZATION,
    WORKFLOW_STEP_CODES.BOOT_SANITIZATION,
    WORKFLOW_STEP_CODES.ENTER_CLEAN_ZONE,
  ],
}

export const DEFAULT_WORKFLOW_DEFINITIONS = [ENTRY_CLEAN_ZONE_WORKFLOW]

/** @typedef {{ id: string, name: string, steps: string[], stepZones?: Record<string, string> }} WorkflowDefinition */

/** @param {WorkflowDefinition} definition @param {string} stepCode */
export function zoneForStep(definition, stepCode) {
  if (definition.stepZones?.[stepCode]) {
    return definition.stepZones[stepCode]
  }
  if (stepCode === WORKFLOW_STEP_CODES.ENTER_CLEAN_ZONE) {
    return null
  }
  return STEP_ZONE_CODES[stepCode] || null
}

/** @param {WorkflowDefinition} definition @param {string} zoneCode */
export function stepForZone(definition, zoneCode) {
  for (const stepCode of definition.steps) {
    const mapped = zoneForStep(definition, stepCode)
    if (mapped && mapped === zoneCode) {
      return stepCode
    }
  }
  if (
    CLEAN_PRODUCTION_ZONES.has(zoneCode) &&
    definition.steps.includes(WORKFLOW_STEP_CODES.ENTER_CLEAN_ZONE)
  ) {
    return WORKFLOW_STEP_CODES.ENTER_CLEAN_ZONE
  }
  return null
}

export class WorkflowManager {
  constructor() {
    /** @type {Map<string, WorkflowDefinition>} */
    this._definitions = new Map()
  }

  /** @param {WorkflowDefinition} definition */
  registerDefinition(definition) {
    this._definitions.set(definition.id, definition)
  }

  /** @param {string} workflowId */
  getDefinition(workflowId) {
    return this._definitions.get(workflowId) || null
  }

  listDefinitions() {
    return Array.from(this._definitions.values())
  }

  loadDefaults() {
    for (const definition of DEFAULT_WORKFLOW_DEFINITIONS) {
      this.registerDefinition(definition)
    }
  }
}

let _manager = null

export function initWorkflowManager() {
  _manager = new WorkflowManager()
  _manager.loadDefaults()
  return _manager
}

export function getWorkflowManager() {
  if (!_manager) {
    return initWorkflowManager()
  }
  return _manager
}
