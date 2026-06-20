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

  beforeEach(() => {
    tracker = new ZonePresenceTracker()
  })

  it('starts in UNKNOWN for unseen track/zone pairs', () => {
    expect(tracker.getState('CAM-1', 'T-1', 'CZ-1')).toBe(PRESENCE_UNKNOWN)
  })

  it('emits enter on OUTSIDE -> INSIDE', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', false)
    expect(tracker.getState('CAM-1', 'T-1', 'CZ-1')).toBe(PRESENCE_OUTSIDE)

    const transition = tracker.update('CAM-1', 'T-1', 'CZ-1', true)
    expect(transition).toBe(PRESENCE_ENTER)
    expect(tracker.getState('CAM-1', 'T-1', 'CZ-1')).toBe(PRESENCE_INSIDE)
  })

  it('emits enter on UNKNOWN -> INSIDE (first detection)', () => {
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', true)).toBe(PRESENCE_ENTER)
  })

  it('prevents duplicate enter while INSIDE', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', true)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', true)).toBeNull()
  })

  it('emits exit on INSIDE -> OUTSIDE', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', true)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', false)).toBe(PRESENCE_EXIT)
    expect(tracker.getState('CAM-1', 'T-1', 'CZ-1')).toBe(PRESENCE_OUTSIDE)
  })

  it('allows re-enter after exit', () => {
    tracker.update('CAM-1', 'T-1', 'CZ-1', true)
    tracker.update('CAM-1', 'T-1', 'CZ-1', false)
    expect(tracker.update('CAM-1', 'T-1', 'CZ-1', true)).toBe(PRESENCE_ENTER)
  })
})
