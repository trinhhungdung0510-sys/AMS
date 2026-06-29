import { ATSH_SEVERITY, ATSH_STATUS } from '../data/atshViolations'
import { severityLabels } from '../data/mockData'
import { resolveSnapshotUrl } from './complianceEventNormalizer'

const EMPTY = 'Chưa có dữ liệu'

const STATUS_LABELS = {
  new: 'Chưa xử lý',
  confirmed: 'Đang xử lý',
  processing: 'Đang xử lý',
  resolved: 'Đã xử lý',
  dismissed: 'Báo động giả',
}

function parseDateTime(source) {
  const raw = source.occurredAt || source.datetime || `${source.date || ''}T${source.time || '00:00'}`
  if (!raw) return { display: EMPTY, date: '', time: '' }
  const parsed = new Date(raw.includes('T') ? raw : `${source.date}T${source.time || '00:00'}`)
  if (Number.isNaN(parsed.getTime())) {
    return { display: raw, date: source.date || '', time: source.time || '' }
  }
  return {
    display: parsed.toLocaleString('vi-VN'),
    date: source.date || raw.slice(0, 10),
    time: source.time || parsed.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
    timestamp: parsed,
  }
}

function resolveObjectKind(source) {
  const eventType = String(source.eventType || source.type || '').toUpperCase()
  const group = source.typeGroup || source.metadata?.object_type

  if (group === 'animal' || eventType.includes('ANIMAL')) return 'animal'
  if (group === 'vehicle' || eventType.includes('VEHICLE') || eventType.includes('TRUCK')) return 'vehicle'
  return 'person'
}

function formatTimelineTime(timestamp, offsetSeconds = 0) {
  if (!timestamp) return '--:--:--'
  const next = new Date(timestamp.getTime() + offsetSeconds * 1000)
  return next.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

function buildPilotTimeline(source, timestamp) {
  const kind = resolveObjectKind(source)
  const label = source.typeLabel || source.eventType || 'Vi phạm ATSH'

  if (!timestamp) {
    return [{ time: EMPTY, label: EMPTY, tone: 'info' }]
  }

  if (kind === 'vehicle') {
    return [
      { time: formatTimelineTime(timestamp, -18), label: 'Xe tiếp cận cổng kiểm soát', tone: 'info' },
      { time: formatTimelineTime(timestamp, -8), label: 'Chưa hoàn tất sát trùng xe', tone: 'warning' },
      { time: formatTimelineTime(timestamp, 0), label, tone: 'critical' },
      { time: formatTimelineTime(timestamp, 1), label: 'Thông báo gửi quản lý', tone: 'info' },
    ]
  }

  if (kind === 'animal') {
    return [
      { time: formatTimelineTime(timestamp, -12), label: 'Phát hiện động vật lạ trong khung hình', tone: 'warning' },
      { time: formatTimelineTime(timestamp, -4), label: 'Xác nhận xâm nhập khu vực sạch', tone: 'warning' },
      { time: formatTimelineTime(timestamp, 0), label, tone: 'critical' },
      { time: formatTimelineTime(timestamp, 1), label: 'Thông báo gửi quản lý', tone: 'info' },
    ]
  }

  return [
    { time: formatTimelineTime(timestamp, -10), label: 'Người đi vào vùng sạch', tone: 'info' },
    { time: formatTimelineTime(timestamp, -7), label: 'Không phát hiện sát trùng tay', tone: 'warning' },
    { time: formatTimelineTime(timestamp, 0), label, tone: 'critical' },
    { time: formatTimelineTime(timestamp, 1), label: 'Thông báo gửi quản lý', tone: 'info' },
  ]
}

export function buildViolationDetail(source) {
  if (!source) return null

  const metadata = source.metadata || {}
  const { display, date, time, timestamp } = parseDateTime(source)
  const severityKey = source.severityRaw
    || (['CRITICAL', 'WARNING', 'INFO'].includes(source.severity) ? source.severity : null)
    || (source.severity === 'critical' || source.severity === 'danger' ? 'CRITICAL'
      : source.severity === 'warning' || source.severity === 'medium' ? 'WARNING'
        : 'INFO')
  const severity = ATSH_SEVERITY[severityKey] || ATSH_SEVERITY.WARNING
  const statusKey = source.status || 'new'
  const snapshotUrl = resolveSnapshotUrl(source.snapshotPath || source.snapshotUrl || metadata.snapshot_url)
  const videoUrl = resolveSnapshotUrl(metadata.videoUrl || metadata.video_url)
  const objectKind = resolveObjectKind(source)
  const confidence = source.confidence ?? metadata.confidence ?? null

  return {
    id: source.id || EMPTY,
    code: source.id || EMPTY,
    occurredAt: display,
    date,
    time,
    severityLabel: severity.label,
    severityTone: severity.tone,
    statusKey,
    statusLabel: STATUS_LABELS[statusKey] || ATSH_STATUS[statusKey] || STATUS_LABELS.new,
    cameraId: source.cameraId || source.camera_id || '',
    cameraName: source.cameraName || source.camera_name || metadata.camera_name || EMPTY,
    zoneName: source.zoneName || source.zone || source.zone_name || metadata.zone_name || EMPTY,
    ruleName: source.ruleName || source.rule_name || source.typeLabel || source.eventType || EMPTY,
    typeLabel: source.typeLabel || source.eventType || source.type || EMPTY,
    confidence: confidence != null ? Number(confidence) : null,
    confidenceLabel: confidence != null ? `${Math.round(Number(confidence))}%` : EMPTY,
    snapshotUrl,
    videoUrl,
    hasSnapshot: Boolean(snapshotUrl),
    hasVideo: Boolean(videoUrl),
    objectKind,
    person: {
      trackId: metadata.track_id || metadata.trackId || source.trackId || EMPTY,
      uniform: metadata.uniform || metadata.uniform_name || source.uniform || EMPTY,
      currentZone: source.zoneName || source.zone || EMPTY,
      allowedZone: metadata.allowed_zone || metadata.allowedZone || EMPTY,
    },
    vehicle: {
      vehicleType: metadata.vehicle_type || metadata.vehicleType || source.typeLabel || EMPTY,
      zone: source.zoneName || source.zone || EMPTY,
    },
    animal: {
      animalType: metadata.animal_type || source.animal || source.typeLabel || EMPTY,
    },
    timeline: metadata.timeline?.length
      ? metadata.timeline.map((step) => ({
        time: step.time || step.thoi_gian || EMPTY,
        label: step.label || step.mo_ta || EMPTY,
        tone: step.tone || 'info',
      }))
      : buildPilotTimeline(source, timestamp),
    description: source.description || metadata.description || EMPTY,
    raw: source,
  }
}

export function mergeViolationOverrides(detail, overrides = {}) {
  if (!detail) return null
  return {
    ...detail,
    statusKey: overrides.statusKey ?? detail.statusKey,
    statusLabel: STATUS_LABELS[overrides.statusKey] || detail.statusLabel,
    note: overrides.note ?? '',
  }
}

export { EMPTY as VIOLATION_EMPTY_LABEL, STATUS_LABELS as VIOLATION_STATUS_LABELS }
