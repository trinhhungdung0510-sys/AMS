const STATUS_VI_TO_CODE = {
  Mới: 'new',
  'Đang xử lý': 'processing',
  'Đã xử lý': 'resolved',
}

const OPEN_STATUS = new Set(['OPEN', 'open', 'new', 'Mới'])

export function parseOccurredParts(value) {
  if (!value) {
    return { date: '', time: '00:00', occurredAt: '' }
  }
  const normalized = String(value)
  const [datePart, timePart = ''] = normalized.includes('T')
    ? normalized.split('T')
    : normalized.split(' ')
  return {
    date: datePart || '',
    time: timePart.slice(0, 5) || '00:00',
    occurredAt: normalized,
  }
}

export function normalizeSeverity(raw) {
  const value = String(raw || '').toUpperCase()
  if (value === 'CRITICAL' || value.includes('NGHIÊM')) {
    return { severityRaw: 'CRITICAL', severity: 'critical' }
  }
  if (value === 'HIGH' || value.includes('CAO')) {
    return { severityRaw: 'HIGH', severity: 'danger' }
  }
  if (value === 'MEDIUM' || value.includes('CẢNH') || value === 'WARNING') {
    return { severityRaw: 'MEDIUM', severity: 'warning' }
  }
  if (value === 'LOW' || value.includes('THẤP')) {
    return { severityRaw: 'LOW', severity: 'low' }
  }
  return { severityRaw: value || 'MEDIUM', severity: 'medium' }
}

export function normalizeStatus(raw) {
  const value = String(raw || '')
  if (OPEN_STATUS.has(value)) {
    return { statusRaw: 'OPEN', status: 'new' }
  }
  if (value === 'ACKNOWLEDGED' || value === 'processing' || value === 'Đang xử lý') {
    return { statusRaw: value, status: 'processing' }
  }
  if (value === 'RESOLVED' || value === 'resolved' || value === 'Đã xử lý') {
    return { statusRaw: value, status: 'resolved' }
  }
  return {
    statusRaw: value || 'OPEN',
    status: STATUS_VI_TO_CODE[value] || 'new',
  }
}

export function normalizeApiEvent(event) {
  const { date, time, occurredAt } = parseOccurredParts(event.thoi_gian)
  const { severityRaw, severity } = normalizeSeverity(event.muc_do)
  const { statusRaw, status } = normalizeStatus(event.trang_thai)

  return {
    id: event.id,
    eventType: event.ten_vi_pham,
    typeLabel: event.ten_vi_pham,
    cameraId: '',
    cameraName: event.ten_camera,
    zoneId: '',
    zoneName: event.ten_vung,
    farmName: event.ten_trang_trai,
    severityRaw,
    severity,
    statusRaw,
    status,
    handler: event.nguoi_xu_ly || 'Chưa phân công',
    confidence: event.do_tin_cay ?? 0,
    date,
    time,
    occurredAt,
    source: 'api',
  }
}

export function normalizeEngineEvent(event) {
  const occurred = event.started_at || event.created_at || event.occurred_at
  const { date, time, occurredAt } = parseOccurredParts(occurred)
  const { severityRaw, severity } = normalizeSeverity(event.severity)
  const { statusRaw, status } = normalizeStatus(event.status)
  const confidence = event.confidence != null
    ? Math.round(Number(event.confidence) * (Number(event.confidence) <= 1 ? 100 : 1))
    : 0

  return {
    id: event.id,
    eventType: event.event_type || event.alert_type,
    typeLabel: event.event_type || event.rule_name || event.alert_type || 'Sự kiện',
    cameraId: event.camera_id,
    cameraName: event.camera_name || event.camera_id,
    zoneId: event.zone_id,
    zoneName: event.zone_name || event.zone_id,
    farmName: '',
    severityRaw,
    severity,
    statusRaw,
    status,
    handler: 'Chưa phân công',
    confidence,
    date,
    time,
    occurredAt,
    source: 'engine',
    metadata: event.metadata || {},
  }
}

export function normalizeWsPayload(payload) {
  const data = payload?.payload || payload
  const event = data?.event
  if (!event?.id) return null
  return normalizeEngineEvent(event)
}

export function upsertEvent(events, incoming) {
  if (!incoming?.id) return events
  const without = events.filter((item) => item.id !== incoming.id)
  return [incoming, ...without]
}

export function isToday(isoDate, today = new Date().toISOString().slice(0, 10)) {
  if (!isoDate) return false
  return String(isoDate).slice(0, 10) === today
}

export function computeEventMetrics(events, cameras = [], today = new Date().toISOString().slice(0, 10)) {
  return {
    totalEvents: events.length,
    openEvents: events.filter((item) => item.statusRaw === 'OPEN' || item.status === 'new').length,
    criticalEvents: events.filter((item) => item.severityRaw === 'CRITICAL').length,
    totalEventsToday: events.filter((item) => isToday(item.occurredAt || item.date, today)).length,
    totalCameras: cameras.length,
    onlineCameras: cameras.filter((item) => String(item.status).toLowerCase() === 'online').length,
  }
}
