import { describe, expect, it, beforeEach } from 'vitest'
import {
  PRESENCE_ENTER,
  PRESENCE_EXIT,
  PRESENCE_INSIDE,
  PRESENCE_OUTSIDE,
  PRESENCE_UNKNOWN,
  ZonePresenceTracker,
} from './ZonePresenceTracker'

describe('ZonePresenceTracker', () => {
  let tracker
  const timestamp = '2026-06-20T10:00:00+00:00'

  beforeEach(() => {
    tracker = new ZonePresenceTracker()
  })

  it('starts in UNKNOWN for unseen track/zone pairs', () => {
    expect(tracker.getState('CAM-1', 'T-1', 'CZ-1')).toBe(PRESENCE_UNKNOWN)
  })

  it('is silent on UNKNOWN -> OUTSIDE', () => {
    const result = tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp)
    expect(result.transition).toBeNull()
    expect(result.nextState).toBe(PRESENCE_OUTSIDE)
  })

  it('emits enter on OUTSIDE -> INSIDE', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp)
    const result = tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp)
    expect(result.transition).toBe(PRESENCE_ENTER)
    expect(result.nextState).toBe(PRESENCE_INSIDE)
  })

  it('is silent on UNKNOWN -> INSIDE', () => {
    const result = tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp)
    expect(result.transition).toBeNull()
    expect(result.nextState).toBe(PRESENCE_INSIDE)
  })

  it('prevents duplicate enter while INSIDE', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp)
    tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp).transition).toBeNull()
  })

  it('emits exit on INSIDE -> OUTSIDE', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp).transition).toBe(PRESENCE_EXIT)
  })
})

describe('Transition scenarios v1.6.1', () => {
  let tracker
  const timestamp = '2026-06-20T10:00:00+00:00'

  beforeEach(() => {
    tracker = new ZonePresenceTracker()
  })

  it('Test 1: OUTSIDE -> INSIDE emits one PERSON_ENTER transition', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp).transition).toBe(PRESENCE_ENTER)
  })

  it('Test 2: INSIDE -> INSIDE -> INSIDE emits no transitions', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp)
    const transitions = [true, true, true].map(() =>
      tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp).transition,
    )
    expect(transitions.filter(Boolean)).toEqual([])
  })

  it('Test 3: INSIDE -> OUTSIDE emits one PERSON_EXIT transition', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp).transition).toBe(PRESENCE_EXIT)
  })

  it('Test 4: OUTSIDE -> INSIDE -> OUTSIDE -> INSIDE emits 2 enter and 1 exit', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp)
    const transitions = [
      tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp).transition,
      tracker.update('CAM-1', 'T-1', 'CZ-1', false, timestamp).transition,
      tracker.update('CAM-1', 'T-1', 'CZ-1', true, timestamp).transition,
    ]
    expect(transitions.filter((item) => item === PRESENCE_ENTER)).toHaveLength(2)
    expect(transitions.filter((item) => item === PRESENCE_EXIT)).toHaveLength(1)
  })

  it('Test 5: ZONE-A -> ZONE-B emits exit A and enter B', () => {
    tracker.applyZones('CAM-1', 'T-1', new Set(), timestamp, ['ZONE-A', 'ZONE-B'])
    tracker.applyZones('CAM-1', 'T-1', new Set(['ZONE-A']), timestamp, ['ZONE-A', 'ZONE-B'])
    const results = tracker.applyZones(
      'CAM-1',
      'T-1',
      new Set(['ZONE-B']),
      timestamp,
      ['ZONE-A', 'ZONE-B'],
    )
    expect(results['ZONE-A'].transition).toBe(PRESENCE_EXIT)
    expect(results['ZONE-B'].transition).toBe(PRESENCE_ENTER)
  })
})
