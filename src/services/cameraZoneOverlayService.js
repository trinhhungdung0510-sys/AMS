import { CANVAS_HEIGHT, CANVAS_WIDTH } from '../data/zoneDesignerPro'
import { getZoneTypeLabel } from '../config/cameraZones'
import { resolveZoneTypeLabel } from '../utils/zoneOverlayLabels'
import { normalizePoint } from '../utils/zoneGeometry'
import { listZones } from './farmZoneService'
import { getZones } from './zoneService'

/** Same-tab + cross-tab zone sync (Camera Live refresh after save). */
export const CAMERA_ZONES_UPDATED_EVENT = 'ams:camera-zones-updated'
export const ZONE_UPDATED_EVENT = CAMERA_ZONES_UPDATED_EVENT

const ZONE_SYNC_STORAGE_KEY = 'ams:zone-sync'
const ZONE_WS_TYPES = new Set(['zone.updated', 'zone_updated', 'ZoneUpdated'])

export function isZoneUpdatedWsPayload(payload) {
  const type = payload?.type || payload?.event_type || payload?.eventType
  return ZONE_WS_TYPES.has(type)
}

export function getZoneUpdatedCameraId(payload) {
  return payload?.camera_id || payload?.cameraId || payload?.data?.camera_id || null
}

/**
 * Notify Camera Live (and other listeners) to reload zones from the server.
 * Uses CustomEvent (same tab) + storage pulse (other tabs). No local zone cache.
 */
export function notifyCameraZonesUpdated(cameraId) {
  const detail = { cameraId: cameraId || null, at: Date.now() }

  window.dispatchEvent(new CustomEvent(CAMERA_ZONES_UPDATED_EVENT, { detail }))

  try {
    localStorage.setItem(ZONE_SYNC_STORAGE_KEY, JSON.stringify(detail))
  } catch {
    // ignore private mode / quota errors
  }
}

export const notifyZoneUpdated = notifyCameraZonesUpdated

export function mapDesignerZoneToOverlay(item) {
  const points = (item.diem_polygon || [])
    .filter((pair) => Array.isArray(pair) && pair.length >= 2)
    .map(([x, y]) => normalizePoint({ x, y }, CANVAS_WIDTH, CANVAS_HEIGHT))

  return {
    id: item.id,
    camera_id: item.camera_id,
    name: item.ten_vung,
    type: item.ma_vung,
    typeLabel: resolveZoneTypeLabel({
      typeLabel: item.ten_loai_vung,
      type: item.ma_vung,
    }),
    color: item.mau_sac || '#16a34a',
    opacity: item.do_mo ?? 0.3,
    points,
    reference_width: CANVAS_WIDTH,
    reference_height: CANVAS_HEIGHT,
    points_format: 'normalized',
    active: item.dang_hoat_dong !== false,
    source: 'atsh_designer',
  }
}

export function mapCameraEditorZoneToOverlay(zone) {
  return {
    id: zone.id,
    camera_id: zone.camera_id,
    name: zone.name,
    type: zone.type,
    typeLabel: resolveZoneTypeLabel({
      typeLabel: getZoneTypeLabel(zone.type),
      type: zone.type,
    }),
    color: zone.color,
    opacity: zone.opacity ?? 0.3,
    points: zone.points || [],
    reference_width: zone.reference_width,
    reference_height: zone.reference_height,
    points_format: zone.points_format || 'normalized',
    active: true,
    source: 'camera_editor',
  }
}

/**
 * Single server-backed loader for Camera Live overlay.
 * Reads persisted zones only (ATSH designer + camera editor APIs); no local JSON/cache.
 * Camera editor zones win on duplicate IDs.
 */
export async function loadCameraZones(cameraId) {
  if (!cameraId) return []

  const [designerZones, editorZones] = await Promise.all([
    listZones(cameraId).catch(() => []),
    getZones(cameraId).catch(() => []),
  ])

  const merged = new Map()

  designerZones.forEach((item) => {
    merged.set(item.id, mapDesignerZoneToOverlay(item))
  })

  editorZones.forEach((zone) => {
    merged.set(zone.id, mapCameraEditorZoneToOverlay(zone))
  })

  return Array.from(merged.values()).filter(
    (zone) => zone.active !== false && (zone.points?.length ?? 0) >= 3,
  )
}

/** @deprecated use loadCameraZones */
export const loadUnifiedCameraZones = loadCameraZones
