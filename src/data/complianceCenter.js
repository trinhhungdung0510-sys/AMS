export const COMPLIANCE_EVENT_TYPES = {
  ZONE_INTRUSION: 'ZONE_INTRUSION',
  UNIFORM_VIOLATION: 'UNIFORM_VIOLATION',
  NO_HAND_SANITIZATION: 'NO_HAND_SANITIZATION',
  NO_BOOT_SANITIZATION: 'NO_BOOT_SANITIZATION',
  VEHICLE_INTRUSION: 'VEHICLE_INTRUSION',
  ANIMAL_INTRUSION: 'ANIMAL_INTRUSION',
  BIOSECURITY_PROCESS_VIOLATION: 'BIOSECURITY_PROCESS_VIOLATION',
}

export const COMPLIANCE_EVENT_LABELS = {
  ZONE_INTRUSION: 'Xâm nhập vùng cấm',
  UNIFORM_VIOLATION: '⚠ Sai đồng phục',
  NO_HAND_SANITIZATION: 'Không rửa tay sát trùng',
  NO_BOOT_SANITIZATION: 'Không sát trùng ủng',
  VEHICLE_INTRUSION: 'Xe vi phạm sát trùng',
  ANIMAL_INTRUSION: 'Động vật xâm nhập',
  BIOSECURITY_PROCESS_VIOLATION: 'Vi phạm quy trình ATSH',
}

export const COMPLIANCE_EVENT_TYPE_OPTIONS = [
  { value: 'all', label: 'Tất cả loại vi phạm' },
  ...Object.entries(COMPLIANCE_EVENT_LABELS).map(([value, label]) => ({ value, label })),
]

export const COMPLIANCE_DATE_OPTIONS = [
  { value: 'all', label: 'Tất cả ngày' },
  { value: 'today', label: 'Hôm nay' },
  { value: 'week', label: '7 ngày qua' },
  { value: 'month', label: 'Tháng này' },
]

export function isComplianceEventType(eventType) {
  if (!eventType) return false
  return Object.values(COMPLIANCE_EVENT_TYPES).includes(String(eventType).toUpperCase())
}

export function resolveComplianceLabel(eventType, ruleName) {
  const key = String(eventType || '').toUpperCase()
  return COMPLIANCE_EVENT_LABELS[key] || ruleName || eventType || 'Vi phạm tuân thủ'
}

export function formatComplianceTimestamp(value) {
  if (!value) return '—'
  const normalized = String(value)
  const [datePart, timePart = ''] = normalized.includes('T') ? normalized.split('T') : normalized.split(' ')
  const time = timePart.replace(/\.\d+.*$/, '').replace(/\+.*$/, '').slice(0, 8)
  return `${datePart} ${time || '00:00:00'}`
}

export function resolveScorePercent(event) {
  const raw = event.score ?? event.confidence ?? event.confidence_score
  if (raw == null) return 0
  const numeric = Number(raw)
  if (Number.isNaN(numeric)) return 0
  return Math.round(numeric * (numeric <= 1 ? 100 : 1))
}
