export const PRESENCE_UNKNOWN = 'UNKNOWN'
export const PRESENCE_OUTSIDE = 'OUTSIDE'
export const PRESENCE_INSIDE = 'INSIDE'

export const PRESENCE_ENTER = 'enter'
export const PRESENCE_EXIT = 'exit'

function presenceKey(cameraId, trackId, zoneId) {
  return `${cameraId}:${trackId}:${zoneId}`
}

export class ZonePresenceTracker {
  constructor() {
    /** @type {Map<string, string>} */
    this.states = new Map()
  }

  getState(cameraId, trackId, zoneId) {
    return this.states.get(presenceKey(cameraId, trackId, zoneId)) || PRESENCE_UNKNOWN
  }

  /**
   * Update zone presence for a track.
   * @returns {'enter'|'exit'|null}
   */
  update(cameraId, trackId, zoneId, isInside) {
    const key = presenceKey(cameraId, trackId, zoneId)
    const current = this.getState(cameraId, trackId, zoneId)
    const next = isInside ? PRESENCE_INSIDE : PRESENCE_OUTSIDE

    if (current === next) {
      return null
    }

    this.states.set(key, next)

    if (next === PRESENCE_INSIDE && (current === PRESENCE_UNKNOWN || current === PRESENCE_OUTSIDE)) {
      return PRESENCE_ENTER
    }

    if (next === PRESENCE_OUTSIDE && current === PRESENCE_INSIDE) {
      return PRESENCE_EXIT
    }

    return null
  }

  clearCamera(cameraId) {
    const prefix = `${cameraId}:`
    for (const key of [...this.states.keys()]) {
      if (key.startsWith(prefix)) {
        this.states.delete(key)
      }
    }
  }

  clear() {
    this.states.clear()
  }
}

export const defaultZonePresenceTracker = new ZonePresenceTracker()
