import { FARM_MAP_ZONES } from './farmControlDashboard'
import { DESIGNER_STORAGE_KEY, loadDesignerState } from './smartFarmDesigner'

export const FARM_MAP_UPDATED_EVENT = 'ams-farm-map-updated'

const PCT_SCALE = 0.00018

export function atshLevelToRisk(level) {
  if (level === 'red') return 'risk'
  if (level === 'yellow' || level === 'orange') return 'attention'
  return 'safe'
}

export function gisObjectToDashboardZone(obj, centerLat, centerLng) {
  const pctCenterX = 50 + (obj.y - centerLng) / PCT_SCALE
  const pctCenterY = 50 - (obj.x - centerLat) / PCT_SCALE
  const pctW = Math.max(4, obj.height / PCT_SCALE)
  const pctH = Math.max(4, obj.width / PCT_SCALE)

  return {
    id: obj.id,
    name: obj.name,
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
  const data = state || loadDesignerState()
  const { layout, objects } = data

  const zones = objects
    .filter((item) => item.objectType !== 'camera')
    .map((item) => gisObjectToDashboardZone(item, layout.centerLat, layout.centerLng))

  const cameras = objects
    .filter((item) => item.objectType === 'camera')
    .map((item) => {
      const box = gisObjectToDashboardZone(
        { ...item, width: item.width * 0.6, height: item.height * 0.6 },
        layout.centerLat,
        layout.centerLng,
      )
      return { ...box, id: item.id, status: item.status }
    })

  return {
    zones: zones.length ? zones : FARM_MAP_ZONES,
    cameras,
    layout: data.layout,
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
