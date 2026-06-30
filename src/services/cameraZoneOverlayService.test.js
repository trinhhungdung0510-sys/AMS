import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import {
  CAMERA_ZONES_UPDATED_EVENT,
  getZoneUpdatedCameraId,
  isZoneUpdatedWsPayload,
  loadCameraZones,
  mapDesignerZoneToOverlay,
  notifyCameraZonesUpdated,
} from './cameraZoneOverlayService'

vi.mock('./farmZoneService', () => ({
  listZones: vi.fn(),
}))

vi.mock('./zoneService', () => ({
  getZones: vi.fn(),
}))

import { listZones } from './farmZoneService'
import { getZones } from './zoneService'

describe('mapDesignerZoneToOverlay', () => {
  it('normalizes ATSH designer polygon to overlay model', () => {
    const zone = mapDesignerZoneToOverlay({
      id: 'ZP-001',
      camera_id: 'CAM-001',
      ten_vung: 'Vùng sạch',
      ten_loai_vung: 'Cổng trại',
      ma_vung: 'farm_gate',
      mau_sac: '#16a34a',
      diem_polygon: [[0, 0], [640, 0], [640, 360], [0, 360]],
      dang_hoat_dong: true,
    })

    expect(zone.name).toBe('Vùng sạch')
    expect(zone.typeLabel).toBe('Cổng trại')
    expect(zone.points[1]).toEqual({ x: 0.5, y: 0 })
    expect(zone.reference_width).toBe(1280)
    expect(zone.source).toBe('atsh_designer')
  })
})

describe('loadCameraZones', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('loads persisted zones from server APIs and deduplicates by id', async () => {
    listZones.mockResolvedValue([
      {
        id: 'ZP-001',
        camera_id: 'CAM-001',
        ten_vung: 'ATSH',
        ten_loai_vung: 'Cổng',
        ma_vung: 'farm_gate',
        mau_sac: '#16a34a',
        diem_polygon: [[0, 0], [1280, 0], [1280, 720], [0, 720]],
        dang_hoat_dong: true,
      },
    ])

    getZones.mockResolvedValue([
      {
        id: 'ZP-001',
        camera_id: 'CAM-001',
        name: 'Editor override',
        type: 'monitoring',
        color: '#ff0000',
        points: [{ x: 0.1, y: 0.1 }, { x: 0.9, y: 0.1 }, { x: 0.9, y: 0.9 }],
        reference_width: 1920,
        reference_height: 1080,
        points_format: 'normalized',
      },
      {
        id: 'CZ-002',
        camera_id: 'CAM-001',
        name: 'Sub zone',
        type: 'clean',
        color: '#22c55e',
        points: [{ x: 0.2, y: 0.2 }, { x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
        reference_width: 1920,
        reference_height: 1080,
        points_format: 'normalized',
      },
    ])

    const zones = await loadCameraZones('CAM-001')

    expect(zones).toHaveLength(2)
    expect(zones.find((zone) => zone.id === 'ZP-001')?.name).toBe('Editor override')
    expect(zones.find((zone) => zone.id === 'CZ-002')?.name).toBe('Sub zone')
  })
})

describe('zone sync helpers', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('dispatches ZoneUpdated custom event with camera id', () => {
    const handler = vi.fn()
    const listeners = new Map()

    vi.stubGlobal('window', {
      dispatchEvent: (event) => {
        listeners.get(event.type)?.(event)
        return true
      },
      addEventListener: (type, fn) => {
        listeners.set(type, fn)
      },
      removeEventListener: (type) => {
        listeners.delete(type)
      },
    })

    vi.stubGlobal('localStorage', {
      setItem: vi.fn(),
    })

    window.addEventListener(CAMERA_ZONES_UPDATED_EVENT, handler)
    notifyCameraZonesUpdated('CAM-001')

    expect(handler).toHaveBeenCalledTimes(1)
    expect(handler.mock.calls[0][0].detail).toEqual(
      expect.objectContaining({ cameraId: 'CAM-001' }),
    )
  })

  it('detects websocket zone update payloads', () => {
    expect(isZoneUpdatedWsPayload({ type: 'zone.updated', camera_id: 'CAM-001' })).toBe(true)
    expect(isZoneUpdatedWsPayload({ event_type: 'ZoneUpdated', cameraId: 'CAM-002' })).toBe(true)
    expect(isZoneUpdatedWsPayload({ type: 'event.created' })).toBe(false)
    expect(getZoneUpdatedCameraId({ type: 'zone.updated', camera_id: 'CAM-003' })).toBe('CAM-003')
  })
})
