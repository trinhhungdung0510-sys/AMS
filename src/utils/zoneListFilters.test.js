import { describe, expect, it } from 'vitest'
import {
  filterAndSortZoneItems,
  flattenZoneTree,
} from './zoneListFilters'

const MODES = { VIEW: 'view', EDIT: 'edit', ADD: 'add' }

const zoneTree = [
  {
    id: 'Z-1',
    name: 'Vùng sạch',
    type: 'clean',
    color: '#16a34a',
    points: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }],
    created_at: '2026-06-01T08:00:00+07:00',
    subzones: [
      {
        id: 'Z-1A',
        name: 'Khu rửa tay',
        type: 'clean',
        color: '#22c55e',
        points: [{ x: 0, y: 0 }, { x: 0.2, y: 0 }, { x: 0.2, y: 0.2 }],
        created_at: '2026-06-02T08:00:00+07:00',
      },
    ],
  },
  {
    id: 'Z-2',
    name: 'Kho cám',
    type: 'restricted',
    color: '#dc2626',
    points: [{ x: 0, y: 0 }, { x: 0.5, y: 0 }, { x: 0.5, y: 0.5 }],
    created_at: '2026-06-03T08:00:00+07:00',
    subzones: [],
  },
]

describe('flattenZoneTree', () => {
  it('flattens root zones and subzones', () => {
    const flat = flattenZoneTree(zoneTree)
    expect(flat).toHaveLength(3)
    expect(flat[1].zone.name).toBe('Khu rửa tay')
    expect(flat[1].isSubzone).toBe(true)
    expect(flat[1].parentName).toBe('Vùng sạch')
  })
})

describe('filterAndSortZoneItems', () => {
  const flat = flattenZoneTree(zoneTree)
  const statusContext = { selectedZoneId: null, mode: MODES.VIEW, modes: MODES }

  it('filters by search query', () => {
    const result = filterAndSortZoneItems(flat, { query: 'kho' }, statusContext)
    expect(result.map((item) => item.zone.name)).toEqual(['Kho cám'])
  })

  it('filters by type and level', () => {
    const result = filterAndSortZoneItems(
      flat,
      { typeFilter: 'clean', levelFilter: 'subzone' },
      statusContext,
    )
    expect(result.map((item) => item.zone.name)).toEqual(['Khu rửa tay'])
  })

  it('sorts by name descending', () => {
    const result = filterAndSortZoneItems(flat, { sortBy: 'name-desc' }, statusContext)
    expect(result.map((item) => item.zone.name)).toEqual([
      'Vùng sạch',
      'Khu rửa tay',
      'Kho cám',
    ])
  })
})
