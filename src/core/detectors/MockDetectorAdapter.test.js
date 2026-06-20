import { describe, expect, it } from 'vitest'
import { MockDetectorAdapter, listMockScenarios } from './MockDetectorAdapter'
import { DetectorAdapter } from './DetectorAdapter'

describe('MockDetectorAdapter', () => {
  it('extends DetectorAdapter', () => {
    const adapter = new MockDetectorAdapter()
    expect(adapter).toBeInstanceOf(DetectorAdapter)
    expect(adapter.id).toBe('mock-detector-v1')
    expect(adapter.source).toBe('MOCK')
  })

  it('detects observation payload for scenario', () => {
    const adapter = new MockDetectorAdapter('one_person')
    const payload = adapter.detect({
      cameraId: 'CAM-1',
      frameWidth: 1280,
      frameHeight: 720,
      timestamp: '2026-06-22T10:00:00Z',
    })

    expect(payload.cameraId).toBe('CAM-1')
    expect(payload.source).toBe('MOCK')
    expect(payload.objects).toHaveLength(1)
    expect(payload.objects[0].trackId).toBe('T-001')
  })

  it('lists available scenarios', () => {
    const scenarios = listMockScenarios()
    expect(scenarios.some((item) => item.key === 'ppe_violation')).toBe(true)
  })
})
