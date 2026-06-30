import { describe, expect, it } from 'vitest'
import { getZoneOverlayDisplay, resolveZoneTypeLabel } from './zoneOverlayLabels'

describe('zoneOverlayLabels', () => {
  it('prefers Vietnamese type label over technical code', () => {
    expect(resolveZoneTypeLabel({
      typeLabel: 'Nhà tắm',
      type: 'shower_room',
    })).toBe('Nhà tắm')
  })

  it('hides duplicate subtitle when type equals name', () => {
    expect(getZoneOverlayDisplay({
      name: 'Cổng trại',
      typeLabel: 'Cổng trại',
      type: 'farm_gate',
    })).toEqual({
      name: 'Cổng trại',
      typeLabel: '',
    })
  })

  it('keeps subtitle when type differs from name', () => {
    expect(getZoneOverlayDisplay({
      name: 'Vùng sạch A',
      typeLabel: 'Nhà tắm',
      type: 'shower_room',
    })).toEqual({
      name: 'Vùng sạch A',
      typeLabel: 'Nhà tắm',
    })
  })
})
