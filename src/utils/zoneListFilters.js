import { getZoneTypeLabel } from '../config/cameraZones'
import { getZonePointCount, getZoneStatusKey } from './zoneListUtils'

export function flattenZoneTree(zoneTree) {
  const items = []

  zoneTree.forEach((root) => {
    items.push({
      zone: root,
      isSubzone: false,
      parentName: null,
    })

    ;(root.subzones || []).forEach((subzone) => {
      items.push({
        zone: subzone,
        isSubzone: true,
        parentName: root.name,
      })
    })
  })

  return items
}

function matchesQuery(item, query) {
  if (!query) return true

  const { zone } = item
  const typeLabel = getZoneTypeLabel(zone.type)
  const haystack = [
    zone.name,
    zone.description,
    zone.id,
    zone.type,
    typeLabel,
    item.parentName,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()

  return haystack.includes(query)
}

function matchesType(item, typeFilter) {
  if (!typeFilter || typeFilter === 'all') return true
  return item.zone.type === typeFilter
}

function matchesLevel(item, levelFilter) {
  if (!levelFilter || levelFilter === 'all') return true
  if (levelFilter === 'root') return !item.isSubzone
  if (levelFilter === 'subzone') return item.isSubzone
  return true
}

function matchesStatus(item, statusFilter, statusContext) {
  if (!statusFilter || statusFilter === 'all') return true
  const statusKey = getZoneStatusKey(item.zone, statusContext)
  return statusKey === statusFilter
}

function compareStrings(a, b) {
  return a.localeCompare(b, 'vi', { sensitivity: 'base' })
}

function sortZoneItems(items, sortBy) {
  const sorted = [...items]

  sorted.sort((left, right) => {
    const leftZone = left.zone
    const rightZone = right.zone

    switch (sortBy) {
      case 'name-desc':
        return compareStrings(rightZone.name, leftZone.name)
      case 'type-asc':
        return compareStrings(getZoneTypeLabel(leftZone.type), getZoneTypeLabel(rightZone.type))
      case 'type-desc':
        return compareStrings(getZoneTypeLabel(rightZone.type), getZoneTypeLabel(leftZone.type))
      case 'points-asc':
        return getZonePointCount(leftZone) - getZonePointCount(rightZone)
      case 'points-desc':
        return getZonePointCount(rightZone) - getZonePointCount(leftZone)
      case 'created-asc':
        return compareStrings(leftZone.created_at || '', rightZone.created_at || '')
      case 'created-desc':
        return compareStrings(rightZone.created_at || '', leftZone.created_at || '')
      case 'name-asc':
      default:
        return compareStrings(leftZone.name, rightZone.name)
    }
  })

  return sorted
}

export function filterAndSortZoneItems(items, options, statusContext) {
  const query = (options.query || '').trim().toLowerCase()
  const {
    typeFilter = 'all',
    levelFilter = 'all',
    statusFilter = 'all',
    sortBy = 'name-asc',
  } = options

  const filtered = items.filter(
    (item) =>
      matchesQuery(item, query)
      && matchesType(item, typeFilter)
      && matchesLevel(item, levelFilter)
      && matchesStatus(item, statusFilter, statusContext),
  )

  return sortZoneItems(filtered, sortBy)
}
