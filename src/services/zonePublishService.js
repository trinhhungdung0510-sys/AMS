import { notifyCameraZonesUpdated } from './cameraZoneOverlayService'

export const ZONE_PUBLISHED_EVENT = 'ams:zone-published'
export const ZONE_PUBLISH_SUCCESS_MESSAGE =
  'Đồng bộ thành công. Camera đang sử dụng vùng ATSH mới.'

const ZONE_PUBLISH_STORAGE_KEY = 'ams:zone-published'

function countValidZones(zones = []) {
  return zones.filter((zone) => {
    const points = zone.points || zone.polygon_points || []
    return points.length >= 3 && zone.active !== false
  }).length
}

/** Validate before publish — throws if no valid saved zone. */
export function validateZonesForPublish(zones = []) {
  const validCount = countValidZones(zones)
  if (validCount < 1) {
    throw new Error('Cần ít nhất 01 vùng ATSH hợp lệ trước khi publish')
  }
  return validCount
}

/**
 * Publish flow (after successful API save):
 * Validate → Notify Live/AI/Rule reload → success event.
 * Does NOT restart AI or reload page — only zone data for this camera.
 */
export function publishCameraZones(cameraId, { zones = null, message = ZONE_PUBLISH_SUCCESS_MESSAGE } = {}) {
  if (!cameraId) {
    throw new Error('Thiếu cameraId để publish vùng ATSH')
  }

  if (zones && zones.length > 0) {
    validateZonesForPublish(zones)
  }

  const detail = {
    cameraId,
    at: Date.now(),
    message,
  }

  notifyCameraZonesUpdated(cameraId)

  window.dispatchEvent(new CustomEvent(ZONE_PUBLISHED_EVENT, { detail }))

  try {
    localStorage.setItem(ZONE_PUBLISH_STORAGE_KEY, JSON.stringify(detail))
  } catch {
    // ignore
  }

  return detail
}

export function readLastZonePublishMessage(cameraId) {
  try {
    const raw = localStorage.getItem(ZONE_PUBLISH_STORAGE_KEY)
    if (!raw) return null
    const detail = JSON.parse(raw)
    if (detail?.cameraId && detail.cameraId !== cameraId) return null
    return detail?.message || null
  } catch {
    return null
  }
}
