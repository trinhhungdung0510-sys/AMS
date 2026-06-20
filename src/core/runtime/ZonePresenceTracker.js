export const PRESENCE_UNKNOWN = 'UNKNOWN'
export const PRESENCE_OUTSIDE = 'OUTSIDE'
export const PRESENCE_INSIDE = 'INSIDE'

export const PRESENCE_ENTER = 'enter'
export const PRESENCE_EXIT = 'exit'

function presenceKey(cameraId, trackId, zoneId) {
  return `${cameraId}:${trackId}:${zoneId}`
}

function createEmptyZoneState(cameraId, trackId, zoneId) {
  return {
    trackId,
    cameraId,
    zoneId,
    currentZoneId: null,
    previousZoneId: null,
    state: PRESENCE_UNKNOWN,
    enteredAt: null,
    exitedAt: null,
  }
}

export class ZonePresenceTracker {
  constructor() {
    /** @type {Map<string, string>} */
    this.states = new Map()
    /** @type {Map<string, object>} */
    this.records = new Map()
  }

  getState(cameraId, trackId, zoneId) {
    return this.states.get(presenceKey(cameraId, trackId, zoneId)) || PRESENCE_UNKNOWN
  }

  getZoneState(cameraId, trackId, zoneId) {
    const key = presenceKey(cameraId, trackId, zoneId)
    return this.records.get(key) || createEmptyZoneState(cameraId, trackId, zoneId)
  }

  update(cameraId, trackId, zoneId, isInside, timestamp = null) {
    const key = presenceKey(cameraId, trackId, zoneId)
    const current = this.getState(cameraId, trackId, zoneId)
    const previousRecord = this.getZoneState(cameraId, trackId, zoneId)
    const next = isInside ? PRESENCE_INSIDE : PRESENCE_OUTSIDE
    let transition = null

    if (current === next) {
      const record = { ...previousRecord, state: current }
      this.records.set(key, record)
      return {
        transition: null,
        previousState: current,
        nextState: current,
        zoneState: record,
      }
    }

    if (next === PRESENCE_INSIDE && current === PRESENCE_OUTSIDE) {
      transition = PRESENCE_ENTER
    } else if (next === PRESENCE_OUTSIDE && current === PRESENCE_INSIDE) {
      transition = PRESENCE_EXIT
    }

    const record = {
      trackId,
      cameraId,
      zoneId,
      currentZoneId: isInside ? zoneId : null,
      previousZoneId: isInside ? previousRecord.currentZoneId : zoneId,
      state: next,
      enteredAt: isInside ? timestamp : previousRecord.enteredAt,
      exitedAt: isInside ? null : timestamp,
    }

    if (isInside && transition === PRESENCE_ENTER) {
      record.enteredAt = timestamp
      record.exitedAt = null
    } else if (!isInside && transition === PRESENCE_EXIT) {
      record.exitedAt = timestamp
    }

    this.states.set(key, next)
    this.records.set(key, record)

    return {
      transition,
      previousState: current,
      nextState: next,
      zoneState: record,
    }
  }

  applyZones(cameraId, trackId, activeZoneIds, timestamp, monitoredZoneIds = null) {
    const prefix = `${cameraId}:${trackId}:`
    const knownZoneIds = [...this.states.keys()]
      .filter((key) => key.startsWith(prefix))
      .map((key) => key.split(':').slice(2).join(':'))

    const zoneIds = new Set([
      ...activeZoneIds,
      ...knownZoneIds,
      ...(monitoredZoneIds || []),
    ])

    const results = {}
    zoneIds.forEach((zoneId) => {
      results[zoneId] = this.update(
        cameraId,
        trackId,
        zoneId,
        activeZoneIds.has(zoneId),
        timestamp,
      )
    })
    return results
  }

  clearCamera(cameraId) {
    const prefix = `${cameraId}:`
    for (const key of [...this.states.keys()]) {
      if (key.startsWith(prefix)) {
        this.states.delete(key)
      }
    }
    for (const key of [...this.records.keys()]) {
      if (key.startsWith(prefix)) {
        this.records.delete(key)
      }
    }
  }

  clear() {
    this.states.clear()
    this.records.clear()
  }
}

export const defaultZonePresenceTracker = new ZonePresenceTracker()
