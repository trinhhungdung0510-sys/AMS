import { describe, expect, it } from 'vitest'
import { getDashboardMapFromDesigner } from '../data/farmMapSync.js'
import { FARM_MAP_ZONES } from '../data/farmControlDashboard.js'

describe('getDashboardMapFromDesigner', () => {
  it('returns fallback zones when objects are missing', () => {
    const result = getDashboardMapFromDesigner({ layout: { centerLat: 10.9, centerLng: 106.9 } })
    expect(Array.isArray(result.zones)).toBe(true)
    expect(result.zones.length).toBeGreaterThan(0)
    expect(Array.isArray(result.cameras)).toBe(true)
  })

  it('uses default farm zones when no designer objects exist', () => {
    const result = getDashboardMapFromDesigner({ layout: { centerLat: 10.9, centerLng: 106.9 }, objects: [] })
    expect(result.zones).toEqual(FARM_MAP_ZONES)
  })
})
