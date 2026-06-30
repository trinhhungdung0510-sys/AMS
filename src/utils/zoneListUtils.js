export function getZonePointCount(zone) {
  return zone?.points?.length ?? 0
}

export function getZoneStatusLabel(zone, { selectedZoneId, mode, modes }) {
  if (zone.id === selectedZoneId && mode === modes.EDIT) return 'Đang chỉnh sửa'
  if (zone.id === selectedZoneId && mode === modes.VIEW) return 'Đang chọn'
  if (getZonePointCount(zone) < 3) return 'Thiếu điểm'
  return 'Hoạt động'
}

export function getZoneStatusKey(zone, { selectedZoneId, mode, modes }) {
  if (zone.id === selectedZoneId && mode === modes.EDIT) return 'editing'
  if (zone.id === selectedZoneId && mode === modes.VIEW) return 'selected'
  if (getZonePointCount(zone) < 3) return 'incomplete'
  return 'active'
}

export function getLiveZoneStatus(zone, rules = []) {
  if (getZonePointCount(zone) < 3) return 'Thiếu điểm'

  const zoneRules = rules.filter((rule) => rule.zone_id === zone.id)
  if (zoneRules.length === 0) return 'Chưa gắn rule'

  const enabledCount = zoneRules.filter((rule) => rule.enabled !== false).length
  if (enabledCount === 0) return 'Rule tắt'
  if (enabledCount === zoneRules.length) return 'Hoạt động'
  return 'Một phần'
}

export function countZoneRules(zoneId, rules = []) {
  return rules.filter((rule) => rule.zone_id === zoneId).length
}
