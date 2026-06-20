import { describe, expect, it, beforeEach } from 'vitest'
import { StateEngine } from './StateEngine'
import { createTrack } from '../tracking/Track'

describe('StateEngine', () => {
  let engine

  beforeEach(() => {
    engine = new StateEngine()
  })

  it('records zone enter transitions', () => {
    const track = createTrack({
      trackId: 'T-1',
      cameraId: 'CAM-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:00Z',
      currentZoneId: 'CZ-1',
    })

    const state = engine.processTrackUpdate({
      track,
      previousTrack: null,
      timestamp: '2026-06-22T10:00:00Z',
      zones: [{ id: 'CZ-1', name: 'Zone 1' }],
    })

    expect(state.zoneEnteredAt['CZ-1']).toBe('2026-06-22T10:00:00Z')
    expect(state.transitions).toContainEqual({
      type: 'enter',
      zoneId: 'CZ-1',
      zoneName: 'Zone 1',
      at: '2026-06-22T10:00:00Z',
    })
  })

  it('records zone exit and clears dwell entry', () => {
    const previousTrack = createTrack({
      trackId: 'T-1',
      cameraId: 'CAM-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:00Z',
      currentZoneId: 'CZ-1',
    })

    engine.processTrackUpdate({
      track: previousTrack,
      previousTrack: null,
      timestamp: '2026-06-22T10:00:00Z',
      zones: [{ id: 'CZ-1', name: 'Zone 1' }],
    })

    const track = createTrack({
      trackId: 'T-1',
      cameraId: 'CAM-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:10Z',
      currentZoneId: null,
    })

    const state = engine.processTrackUpdate({
      track,
      previousTrack,
      timestamp: '2026-06-22T10:00:10Z',
      zones: [{ id: 'CZ-1', name: 'Zone 1' }],
    })

    expect(state.zoneEnteredAt['CZ-1']).toBeUndefined()
    expect(state.transitions.some((item) => item.type === 'exit')).toBe(true)
  })

  it('computes dwell seconds and marks dwell triggered', () => {
    engine.processTrackUpdate({
      track: createTrack({
        trackId: 'T-1',
        cameraId: 'CAM-1',
        objectClass: 'person',
        timestamp: '2026-06-22T10:00:00Z',
        currentZoneId: 'CZ-1',
      }),
      previousTrack: null,
      timestamp: '2026-06-22T10:00:00Z',
      zones: [{ id: 'CZ-1' }],
    })

    const dwellSeconds = engine.getDwellSeconds(
      'CAM-1',
      'T-1',
      'CZ-1',
      '2026-06-22T10:00:35Z',
    )

    expect(dwellSeconds).toBe(35)
    expect(engine.hasDwellTriggered('CAM-1', 'T-1', 'ZR-1')).toBe(false)

    engine.markDwellTriggered('CAM-1', 'T-1', 'ZR-1', 'CZ-1')
    expect(engine.hasDwellTriggered('CAM-1', 'T-1', 'ZR-1')).toBe(true)
  })
})
