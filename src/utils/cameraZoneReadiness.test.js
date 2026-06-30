import { describe, expect, it } from 'vitest'
import {
  canManageAtshZones,
  canViewAtshZones,
  FARM_ADMIN,
  normalizeRole,
  roleHasPermission,
  VIEWER,
} from './permissions'
import {
  getMonitoringStatus,
  hasValidMonitoringZones,
  MONITORING_STATUS,
} from './cameraZoneReadiness'

describe('permissions', () => {
  it('grants zone.manage to farm owner role', () => {
    expect(roleHasPermission(FARM_ADMIN, 'zone.manage')).toBe(true)
    expect(canManageAtshZones({ role: FARM_ADMIN })).toBe(true)
  })

  it('allows viewers to read zones only', () => {
    expect(roleHasPermission(VIEWER, 'zone.read')).toBe(true)
    expect(roleHasPermission(VIEWER, 'zone.manage')).toBe(false)
    expect(canViewAtshZones({ role: VIEWER })).toBe(true)
    expect(canManageAtshZones({ role: VIEWER })).toBe(false)
  })

  it('normalizes role aliases', () => {
    expect(normalizeRole('Farm Owner')).toBe(FARM_ADMIN)
  })
})

describe('cameraZoneReadiness', () => {
  it('detects monitoring readiness from valid polygons', () => {
    const zones = [{ points: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }] }]
    expect(hasValidMonitoringZones(zones)).toBe(true)
    expect(getMonitoringStatus(zones)).toBe(MONITORING_STATUS.READY)
  })

  it('marks camera as not configured without zones', () => {
    expect(getMonitoringStatus([])).toBe(MONITORING_STATUS.NOT_CONFIGURED)
  })
})
