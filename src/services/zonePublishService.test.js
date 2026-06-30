import { describe, expect, it, vi, afterEach } from 'vitest'
import {
  publishCameraZones,
  validateZonesForPublish,
  ZONE_PUBLISH_SUCCESS_MESSAGE,
} from './zonePublishService'

vi.mock('./cameraZoneOverlayService', () => ({
  notifyCameraZonesUpdated: vi.fn(),
}))

import { notifyCameraZonesUpdated } from './cameraZoneOverlayService'

describe('zonePublishService', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('validates at least one zone before publish', () => {
    expect(() => validateZonesForPublish([])).toThrow(/01 vùng/)
  })

  it('publishes and notifies consumers', () => {
    vi.stubGlobal('window', { dispatchEvent: vi.fn() })
    vi.stubGlobal('localStorage', { setItem: vi.fn() })

    const detail = publishCameraZones('CAM-001', {
      zones: [{ polygon_points: [[0, 0], [1, 0], [1, 1]] }],
    })

    expect(notifyCameraZonesUpdated).toHaveBeenCalledWith('CAM-001')
    expect(detail.message).toBe(ZONE_PUBLISH_SUCCESS_MESSAGE)
    expect(window.dispatchEvent).toHaveBeenCalled()
  })
})
