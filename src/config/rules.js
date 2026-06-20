export const RULE_TYPES = [
  { value: 'PERSON_ENTER', label: 'Người vào vùng' },
  { value: 'PERSON_DWELL', label: 'Người lưu lại vùng' },
  { value: 'PERSON_COUNT', label: 'Đếm số người' },
  { value: 'ANIMAL_ENTER', label: 'Động vật xâm nhập' },
  { value: 'PPE_REQUIRED', label: 'Bắt buộc PPE' },
  { value: 'HANDWASH_REQUIRED', label: 'Bắt buộc rửa tay' },
  { value: 'DISINFECTION_REQUIRED', label: 'Bắt buộc sát trùng' },
  { value: 'CROSS_LINE', label: 'Vượt đường giới hạn' },
]

export const RULE_SEVERITIES = [
  { value: 'LOW', label: 'Thấp', tone: 'info' },
  { value: 'MEDIUM', label: 'Trung bình', tone: 'warning' },
  { value: 'HIGH', label: 'Cao', tone: 'critical' },
  { value: 'CRITICAL', label: 'Nghiêm trọng', tone: 'critical' },
]

export const EVENT_STATUSES = [
  { value: 'OPEN', label: 'Mở' },
  { value: 'ACKNOWLEDGED', label: 'Đã xác nhận' },
  { value: 'RESOLVED', label: 'Đã xử lý' },
]

export const DEFAULT_RULE_FORM = {
  name: '',
  description: '',
  zone_id: '',
  rule_type: 'PERSON_ENTER',
  severity: 'MEDIUM',
  enabled: true,
  cooldown_seconds: 60,
  config: {},
}

export function getRuleTypeLabel(type) {
  return RULE_TYPES.find((item) => item.value === type)?.label || type
}

export function getSeverityLabel(severity) {
  return RULE_SEVERITIES.find((item) => item.value === severity)?.label || severity
}

export function getSeverityTone(severity) {
  return RULE_SEVERITIES.find((item) => item.value === severity)?.tone || 'warning'
}

export function getEventStatusLabel(status) {
  return EVENT_STATUSES.find((item) => item.value === status)?.label || status
}
