import { API_BASE_URL } from '../config/api'
import {
  formatComplianceTimestamp,
  isComplianceEventType,
  resolveComplianceLabel,
  resolveScorePercent,
} from '../data/complianceCenter'
import { enrichEventFields } from '../data/eventCatalog'

export function resolveSnapshotUrl(path) {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  return `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
}

export function normalizeComplianceEvent(raw) {
  if (!raw?.id) return null

  const eventType = raw.event_type || raw.eventType
  const occurredAt = raw.started_at || raw.created_at || raw.occurred_at || raw.thoi_gian
  const snapshotPath = raw.snapshotPath || raw.snapshot_url || raw.snapshot_path
  const enriched = enrichEventFields({
    eventType,
    severity: raw.severity,
    ruleName: raw.ruleName || raw.rule_name,
    zoneName: raw.zone_name || raw.zoneName || raw.ten_vung || raw.zone,
    title: raw.title,
    description: raw.description,
    recommendedAction: raw.recommendedAction,
    explanation: raw.explanation,
  })

  return {
    id: raw.id,
    eventType: enriched.eventType,
    typeLabel: enriched.title || resolveComplianceLabel(eventType, raw.ruleName || raw.rule_name),
    classification: enriched.classification,
    classificationLabel: enriched.classificationLabel,
    severity: enriched.severity,
    severityLabel: enriched.severityLabel,
    title: enriched.title,
    description: enriched.description,
    recommendedAction: enriched.recommendedAction,
    explanation: enriched.explanation,
    cameraId: raw.camera_id || raw.cameraId || '',
    cameraName: raw.camera_name || raw.cameraName || raw.ten_camera || raw.camera_id || '—',
    zoneId: raw.zone_id || raw.zoneId || '',
    zoneName: raw.zone_name || raw.zoneName || raw.ten_vung || raw.zone || '—',
    ruleId: raw.ruleId || raw.rule_id || '',
    ruleName: raw.ruleName || raw.rule_name || '',
    score: resolveScorePercent(raw),
    snapshotPath,
    snapshotUrl: resolveSnapshotUrl(snapshotPath),
    timestamp: formatComplianceTimestamp(occurredAt),
    occurredAt,
    severity: enriched.severity,
    status: raw.status,
    metadata: raw.metadata || {},
  }
}

export function isComplianceWsEvent(normalized) {
  if (!normalized) return false
  return isComplianceEventType(normalized.eventType)
}

export function upsertComplianceEvent(events, incoming) {
  if (!incoming?.id) return events
  const without = events.filter((item) => item.id !== incoming.id)
  return [incoming, ...without]
}

export function matchesClientFilters(event, filters) {
  if (filters.eventType !== 'all' && event.eventType !== filters.eventType) return false
  if (filters.cameraId !== 'all' && event.cameraId !== filters.cameraId) return false
  if (filters.zoneId !== 'all' && event.zoneId !== filters.zoneId && event.zoneName !== filters.zoneId) {
    return false
  }
  if (filters.date === 'today') {
    const today = new Date().toISOString().slice(0, 10)
    if (!String(event.occurredAt || '').startsWith(today)) return false
  }
  return true
}
