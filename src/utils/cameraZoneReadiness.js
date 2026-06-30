import { loadCameraZones } from '../services/cameraZoneOverlayService'

export const MONITORING_STATUS = {
  NOT_CONFIGURED: 'not_configured',
  READY: 'ready',
}

export const MONITORING_STATUS_LABELS = {
  [MONITORING_STATUS.NOT_CONFIGURED]: 'Chưa cấu hình vùng ATSH',
  [MONITORING_STATUS.READY]: 'Sẵn sàng giám sát',
}

export function hasValidMonitoringZones(zones = []) {
  return (zones || []).some((zone) => (zone.points?.length ?? 0) >= 3 && zone.active !== false)
}

export function getMonitoringStatus(zones = []) {
  return hasValidMonitoringZones(zones)
    ? MONITORING_STATUS.READY
    : MONITORING_STATUS.NOT_CONFIGURED
}

export function getMonitoringStatusLabel(zones = []) {
  return MONITORING_STATUS_LABELS[getMonitoringStatus(zones)]
}

/** Normalize overlay zone for Rule Engine / Zone Mapper (single data shape). */
export function mapOverlayZoneToEngineRecord(zone) {
  return {
    id: zone.id,
    camera_id: zone.camera_id,
    name: zone.name,
    type: zone.type,
    color: zone.color,
    points: zone.points || [],
    reference_width: zone.reference_width,
    reference_height: zone.reference_height,
    points_format: zone.points_format || 'normalized',
    parent_zone_id: zone.parent_zone_id ?? null,
  }
}

export async function loadEngineZones(cameraId) {
  const zones = await loadCameraZones(cameraId)
  return zones.map(mapOverlayZoneToEngineRecord)
}

export const NEW_CAMERA_ZONE_MESSAGE =
  'Camera chưa được thiết kế vùng an toàn sinh học. Vui lòng hoàn tất cấu hình trước khi đưa vào giám sát.'

export const UNSAVED_ZONE_CHANGES_MESSAGE =
  'Bạn có thay đổi chưa được lưu. Bạn có muốn lưu trước khi thoát không?'
