import { describe, expect, it } from 'vitest'
import {
  CAMERA_LIFECYCLE,
  canRunAiPipeline,
  getLifecycleCapabilities,
  resolveCameraLifecycle,
} from './cameraLifecycle'

const camera = {
  id: 'CAM-001',
  status: 'online',
  is_active: true,
}

describe('resolveCameraLifecycle', () => {
  it('returns NEW when no published zones', () => {
    expect(resolveCameraLifecycle({ camera, publishedZones: [] })).toBe(CAMERA_LIFECYCLE.NEW)
  })

  it('returns CONFIGURING while editing even with published zones', () => {
    const zones = [{ points: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }] }]
    expect(resolveCameraLifecycle({ camera, publishedZones: zones, isZoneEditing: true }))
      .toBe(CAMERA_LIFECYCLE.CONFIGURING)
  })

  it('returns MONITORING when online with published zones', () => {
    const zones = [{ points: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }] }]
    expect(resolveCameraLifecycle({ camera, publishedZones: zones }))
      .toBe(CAMERA_LIFECYCLE.MONITORING)
  })

  it('returns READY when offline with published zones', () => {
    const zones = [{ points: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }] }]
    expect(resolveCameraLifecycle({
      camera: { ...camera, status: 'offline' },
      publishedZones: zones,
    })).toBe(CAMERA_LIFECYCLE.READY)
  })

  it('returns PAUSED when camera inactive', () => {
    expect(resolveCameraLifecycle({
      camera: { ...camera, is_active: false },
      publishedZones: [],
    })).toBe(CAMERA_LIFECYCLE.PAUSED)
  })
})

describe('getLifecycleCapabilities', () => {
  const zones = [{ points: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }] }]

  it('blocks AI on NEW', () => {
    const caps = getLifecycleCapabilities(CAMERA_LIFECYCLE.NEW, [])
    expect(caps.aiDetection).toBe(false)
    expect(caps.liveView).toBe(true)
  })

  it('allows AI on CONFIGURING with published zones', () => {
    expect(canRunAiPipeline(CAMERA_LIFECYCLE.CONFIGURING, zones)).toBe(true)
  })

  it('blocks AI on CONFIGURING without published zones', () => {
    expect(canRunAiPipeline(CAMERA_LIFECYCLE.CONFIGURING, [])).toBe(false)
  })
})
