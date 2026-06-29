export const RESOLVED_STATUS_KEYS = new Set(['resolved', 'dismissed'])

export function mapSourceStatusKey(source, override) {
  if (override?.statusKey) return override.statusKey

  const raw = source?.statusRaw || source?.status || ''
  if (raw === 'resolved' || raw === 'RESOLVED' || raw === 'Đã xử lý') return 'resolved'
  if (raw === 'dismissed') return 'dismissed'
  if (raw === 'confirmed' || raw === 'processing' || raw === 'Đang xử lý') return 'confirmed'
  if (raw === 'new' || raw === 'OPEN' || raw === 'Mới') return 'new'
  return 'new'
}

export function isOpenViolation(source, override) {
  if (!source?.id) return false
  return !RESOLVED_STATUS_KEYS.has(mapSourceStatusKey(source, override))
}

export function isTodayValue(value, today = new Date().toISOString().slice(0, 10)) {
  if (!value) return false
  return String(value).slice(0, 10) === today
}
