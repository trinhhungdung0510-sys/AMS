import { trackKey } from '../tracking/Track'

function stateKey(cameraId, trackId) {
  return trackKey(cameraId, trackId)
}

function createEmptyState() {
  return {
    zoneEnteredAt: {},
    dwellTriggered: {},
    transitions: [],
    ruleStates: {},
  }
}

export class StateEngine {
  constructor() {
    /** @type {Map<string, object>} */
    this.states = new Map()
  }

  getState(cameraId, trackId) {
    const key = stateKey(cameraId, trackId)
    if (!this.states.has(key)) {
      this.states.set(key, createEmptyState())
    }
    return this.states.get(key)
  }

  setState(cameraId, trackId, patch) {
    const current = this.getState(cameraId, trackId)
    const next = {
      ...current,
      ...patch,
    }

    if ('zoneEnteredAt' in patch) {
      next.zoneEnteredAt = { ...patch.zoneEnteredAt }
    } else {
      next.zoneEnteredAt = { ...current.zoneEnteredAt }
    }

    if ('dwellTriggered' in patch) {
      next.dwellTriggered = { ...current.dwellTriggered, ...patch.dwellTriggered }
    } else {
      next.dwellTriggered = { ...current.dwellTriggered }
    }

    if ('ruleStates' in patch) {
      next.ruleStates = { ...current.ruleStates }
      Object.entries(patch.ruleStates).forEach(([ruleId, ruleState]) => {
        next.ruleStates[ruleId] = {
          ...(current.ruleStates[ruleId] || {}),
          ...ruleState,
        }
      })
    } else {
      next.ruleStates = { ...current.ruleStates }
    }

    if ('transitions' in patch) {
      next.transitions = [...patch.transitions]
    } else {
      next.transitions = [...current.transitions]
    }

    this.states.set(stateKey(cameraId, trackId), next)
    return next
  }

  getRuleState(cameraId, trackId, ruleId) {
    const state = this.getState(cameraId, trackId)
    return state.ruleStates[ruleId] || {}
  }

  setRuleState(cameraId, trackId, ruleId, patch) {
    const state = this.getState(cameraId, trackId)
    return this.setState(cameraId, trackId, {
      ruleStates: {
        ...state.ruleStates,
        [ruleId]: {
          ...(state.ruleStates[ruleId] || {}),
          ...patch,
        },
      },
    })
  }

  /**
   * Update dwell + zone transition state after a track move.
   */
  processTrackUpdate({ track, previousTrack, timestamp, zones = [] }) {
    if (!track) return createEmptyState()

    const state = this.getState(track.cameraId, track.trackId)
    const zoneEnteredAt = { ...state.zoneEnteredAt }
    const transitions = [...state.transitions]

    const activeZoneIds = [
      track.currentZoneId,
      track.currentSubZoneId,
    ].filter(Boolean)

    activeZoneIds.forEach((zoneId) => {
      if (!zoneEnteredAt[zoneId]) {
        zoneEnteredAt[zoneId] = timestamp
      }
    })

    const previousZoneIds = [
      previousTrack?.currentZoneId,
      previousTrack?.currentSubZoneId,
    ].filter(Boolean)

    const entered = activeZoneIds.filter((zoneId) => !previousZoneIds.includes(zoneId))
    const exited = previousZoneIds.filter((zoneId) => !activeZoneIds.includes(zoneId))

    entered.forEach((zoneId) => {
      const zone = zones.find((item) => item.id === zoneId)
      transitions.push({
        type: 'enter',
        zoneId,
        zoneName: zone?.name || zoneId,
        at: timestamp,
      })
    })

    exited.forEach((zoneId) => {
      const zone = zones.find((item) => item.id === zoneId)
      transitions.push({
        type: 'exit',
        zoneId,
        zoneName: zone?.name || zoneId,
        at: timestamp,
      })
      delete zoneEnteredAt[zoneId]

      Object.keys(state.dwellTriggered).forEach((ruleId) => {
        const triggeredZoneId = state.ruleStates[ruleId]?.zoneId
        if (triggeredZoneId === zoneId) {
          state.dwellTriggered[ruleId] = false
        }
      })
    })

    if (
      previousTrack &&
      track.currentZoneId &&
      previousTrack.currentZoneId &&
      track.currentZoneId !== previousTrack.currentZoneId
    ) {
      transitions.push({
        type: 'transition',
        fromZoneId: previousTrack.currentZoneId,
        toZoneId: track.currentZoneId,
        at: timestamp,
      })
    }

    return this.setState(track.cameraId, track.trackId, {
      zoneEnteredAt,
      transitions,
    })
  }

  getDwellSeconds(cameraId, trackId, zoneId, timestamp) {
    const enteredAt = this.getState(cameraId, trackId).zoneEnteredAt[zoneId]
    if (!enteredAt) return 0

    const enteredMs = Date.parse(enteredAt)
    const currentMs = Date.parse(timestamp)
    if (Number.isNaN(enteredMs) || Number.isNaN(currentMs)) return 0

    return Math.max(0, (currentMs - enteredMs) / 1000)
  }

  markDwellTriggered(cameraId, trackId, ruleId, zoneId) {
    const state = this.getState(cameraId, trackId)
    return this.setState(cameraId, trackId, {
      dwellTriggered: {
        ...state.dwellTriggered,
        [ruleId]: true,
      },
      ruleStates: {
        ...state.ruleStates,
        [ruleId]: {
          ...(state.ruleStates[ruleId] || {}),
          zoneId,
          triggeredAt: new Date().toISOString(),
        },
      },
    })
  }

  hasDwellTriggered(cameraId, trackId, ruleId) {
    return Boolean(this.getState(cameraId, trackId).dwellTriggered[ruleId])
  }

  removeState(cameraId, trackId) {
    this.states.delete(stateKey(cameraId, trackId))
  }

  clearCamera(cameraId) {
    for (const key of [...this.states.keys()]) {
      if (key.startsWith(`${cameraId}:`)) {
        this.states.delete(key)
      }
    }
  }

  clear() {
    this.states.clear()
  }
}

export const defaultStateEngine = new StateEngine()
