import { FARM_MAP_ZONES } from './farmControlDashboard'
import { DESIGNER_STORAGE_KEY, getDefaultDesignerState, loadDesignerState } from './smartFarmDesigner'

export const FARM_MAP_UPDATED_EVENT = 'ams-farm-map-updated'

const PCT_SCALE = 0.00018

function normalizeDesignerPayload(state) {
  const fallback = getDefaultDesignerState()
  const data = state && typeof state === 'object' ? state : fallback

  return {
    layout: data.layout || fallback.layout,
    objects: Array.isArray(data.objects) ? data.objects : fallback.objects,
  }
}

export function atshLevelToRisk(level) {
  if (level === 'red') return 'risk'
  if (level === 'yellow' || level === 'orange') return 'attention'
  return 'safe'
}

export function gisObjectToDashboardZone(obj, centerLat, centerLng) {
  if (!obj || centerLat == null || centerLng == null) return null

  const pctCenterX = 50 + (obj.y - centerLng) / PCT_SCALE
  const pctCenterY = 50 - (obj.x - centerLat) / PCT_SCALE
  const pctW = Math.max(4, (obj.height || 0) / PCT_SCALE)
  const pctH = Math.max(4, (obj.width || 0) / PCT_SCALE)

  return {
    id: obj.id || `zone-${Math.random().toString(36).slice(2, 8)}`,
    name: obj.name || 'Khu vực',
    x: Math.max(0, Math.min(90, pctCenterX - pctW / 2)),
    y: Math.max(0, Math.min(90, pctCenterY - pctH / 2)),
    width: Math.min(40, pctW),
    height: Math.min(40, pctH),
    risk: atshLevelToRisk(obj.atshLevel),
    objectType: obj.objectType,
    rotation: obj.rotation || 0,
  }
}

export function getDashboardMapFromDesigner(state) {
  let data
  try {
    data = normalizeDesignerPayload(state || loadDesignerState())
  } catch {
    data = normalizeDesignerPayload(getDefaultDesignerState())
  }

  const { layout, objects } = data

  const zones = objects
    .filter((item) => item?.objectType !== 'camera')
    .map((item) => gisObjectToDashboardZone(item, layout.centerLat, layout.centerLng))
    .filter(Boolean)

  const cameras = objects
    .filter((item) => item?.objectType === 'camera')
    .map((item) => {
      const box = gisObjectToDashboardZone(
        { ...item, width: (item.width || 0) * 0.6, height: (item.height || 0) * 0.6 },
        layout.centerLat,
        layout.centerLng,
      )
      if (!box) return null
      return { ...box, id: item.id, name: item.name, status: item.status || 'online' }
    })
    .filter(Boolean)

  return {
    zones: zones.length ? zones : FARM_MAP_ZONES,
    cameras,
    layout,
  }
}

export function subscribeFarmMapUpdates(callback) {
  const onCustom = (event) => {
    callback(getDashboardMapFromDesigner(event.detail))
  }
  const onStorage = (event) => {
    if (event.key === DESIGNER_STORAGE_KEY) {
      callback(getDashboardMapFromDesigner())
    }
  }

  if (typeof window === 'undefined') {
    return () => {}
  }

  window.addEventListener(FARM_MAP_UPDATED_EVENT, onCustom)
  window.addEventListener('storage', onStorage)
  return () => {
    window.removeEventListener(FARM_MAP_UPDATED_EVENT, onCustom)
    window.removeEventListener('storage', onStorage)
  }
}
