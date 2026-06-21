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
  const typeLabel = event.ten_vi_pham || event.event_type || 'Sự kiện'

  return {
    id: event.id,
    eventType: typeLabel,
    typeLabel,
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

export function resolveEventId(event) {
  if (!event) return null
  return event.id || event.event_id || event.eventId || null
}

export function normalizeEngineEvent(event) {
  const id = resolveEventId(event)
  if (!id) return null

  const occurred = event.started_at || event.created_at || event.occurred_at || event.thoi_gian
  const { date, time, occurredAt } = parseOccurredParts(occurred)
  const { severityRaw, severity } = normalizeSeverity(event.severity || event.muc_do)
  const { statusRaw, status } = normalizeStatus(event.status || event.trang_thai)
  const rawConfidence = event.confidence ?? event.confidence_score ?? event.do_tin_cay
  const scoreRaw = event.score ?? event.confidence_score ?? (rawConfidence != null && Number(rawConfidence) <= 1 ? rawConfidence : null)
  const confidence = rawConfidence != null
    ? Math.round(Number(rawConfidence) * (Number(rawConfidence) <= 1 ? 100 : 1))
    : scoreRaw != null
      ? Math.round(Number(scoreRaw) * (Number(scoreRaw) <= 1 ? 100 : 1))
      : 0

  const eventType = event.event_type || event.eventType || event.alert_type || event.ten_vi_pham
  const ruleName = event.ruleName || event.rule_name
  const typeLabels = {
    UNIFORM_VIOLATION: '⚠ Sai đồng phục',
    ZONE_INTRUSION: 'Xâm nhập vùng cấm',
    ANIMAL_INTRUSION: 'Động vật xâm nhập',
    VEHICLE_INTRUSION: 'Xe vi phạm',
    NO_HAND_SANITIZATION: 'Không rửa tay sát trùng',
    NO_BOOT_SANITIZATION: 'Không sát trùng ủng',
  }

  return {
    id,
    eventType,
    typeLabel: typeLabels[eventType] || ruleName || eventType || 'Sự kiện',
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
    score: scoreRaw ?? confidence / 100,
    snapshotPath: event.snapshotPath || event.snapshot_url || event.snapshot_path,
    snapshotUrl: null,
    ruleId: event.ruleId || event.rule_id,
    ruleName,
    date,
    time,
    occurredAt,
    source: 'engine',
    metadata: event.metadata || {},
  }
}

export function normalizeWsPayload(payload) {
  if (!payload) return null

  const data = payload.payload ?? payload.data ?? payload
  const rawEvent = data?.event ?? (resolveEventId(data) ? data : null)
  if (!rawEvent) return null

  return normalizeEngineEvent(rawEvent)
}

export function sortEventsByTime(events) {
  return [...events].sort((left, right) => {
    const leftTs = Date.parse(left.occurredAt || `${left.date}T${left.time || '00:00'}`) || 0
    const rightTs = Date.parse(right.occurredAt || `${right.date}T${right.time || '00:00'}`) || 0
    return rightTs - leftTs
  })
}

export function upsertEvent(events, incoming) {
  if (!incoming?.id) return events
  const without = events.filter((item) => item.id !== incoming.id)
  return sortEventsByTime([incoming, ...without])
}

export function mergeEventLists(primary = [], secondary = []) {
  const merged = new Map()
  ;[...secondary, ...primary].forEach((event) => {
    if (event?.id) merged.set(event.id, event)
  })
  return sortEventsByTime([...merged.values()])
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
