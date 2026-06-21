import { useCallback, useEffect, useMemo, useState } from 'react'
import { ShieldAlert } from 'lucide-react'
import ComplianceEventCard from '../components/compliance/ComplianceEventCard'
import ComplianceFilters from '../components/compliance/ComplianceFilters'
import ComplianceSummary from '../components/compliance/ComplianceSummary'
import EvidenceSnapshotModal from '../components/compliance/EvidenceSnapshotModal'
import { getComplianceEvents, getComplianceEventsSummary } from '../services/complianceCenterService'
import { apiFetch } from '../services/apiClient'
import { subscribeWsEvents } from '../services/wsClient'
import {
  isComplianceWsEvent,
  matchesClientFilters,
  normalizeComplianceEvent,
  upsertComplianceEvent,
} from '../utils/complianceEventNormalizer'

const DEFAULT_FILTERS = {
  eventType: 'all',
  cameraId: 'all',
  zoneId: 'all',
  date: 'today',
}

function resolveDateParam(dateFilter) {
  if (dateFilter === 'today') {
    return new Date().toISOString().slice(0, 10)
  }
  return undefined
}

function ComplianceCenterPage() {
  const [events, setEvents] = useState([])
  const [summary, setSummary] = useState(null)
  const [filters, setFilters] = useState(DEFAULT_FILTERS)
  const [cameras, setCameras] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [realtimeEnabled, setRealtimeEnabled] = useState(true)
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [total, setTotal] = useState(0)

  const zones = useMemo(() => {
    const map = new Map()
    events.forEach((event) => {
      const key = event.zoneId || event.zoneName
      if (!key) return
      map.set(key, event.zoneName || key)
    })
    return [...map.entries()].map(([value, label]) => ({ value, label }))
  }, [events])

  const visibleEvents = useMemo(
    () => events.filter((event) => matchesClientFilters(event, filters)),
    [events, filters],
  )

  const loadCameras = useCallback(async () => {
    const response = await apiFetch('/cameras')
    if (!response.ok) return
    const data = await response.json()
    setCameras(Array.isArray(data) ? data : [])
  }, [])

  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const date = resolveDateParam(filters.date)
      const [eventsRes, summaryRes] = await Promise.all([
        getComplianceEvents({
          page: 1,
          limit: 50,
          eventType: filters.eventType,
          cameraId: filters.cameraId,
          zoneId: filters.zoneId,
          date,
        }),
        getComplianceEventsSummary(date),
      ])

      const normalized = (eventsRes.items || []).map(normalizeComplianceEvent).filter(Boolean)
      setEvents(normalized)
      setTotal(eventsRes.total ?? normalized.length)
      setSummary(summaryRes)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không tải được dữ liệu')
    } finally {
      setLoading(false)
    }
  }, [filters.cameraId, filters.date, filters.eventType, filters.zoneId])

  useEffect(() => {
    loadCameras().catch(() => {})
  }, [loadCameras])

  useEffect(() => {
    loadData()
  }, [loadData])

  useEffect(() => {
    if (!realtimeEnabled) return undefined

    const unsubscribe = subscribeWsEvents({
      onMessage: (payload) => {
        const data = payload.payload ?? payload.data ?? payload
        const rawEvent = data?.event ?? (data?.id ? data : null)
        const complianceEvent = normalizeComplianceEvent(rawEvent)
        if (!complianceEvent || !isComplianceWsEvent(complianceEvent)) return
        if (!matchesClientFilters(complianceEvent, filters)) return

        setEvents((current) => upsertComplianceEvent(current, complianceEvent))
        setSummary((current) => {
          if (!current) return current
          const keyMap = {
            UNIFORM_VIOLATION: 'uniform_violation',
            ZONE_INTRUSION: 'zone_intrusion',
            ANIMAL_INTRUSION: 'animal_intrusion',
            VEHICLE_INTRUSION: 'vehicle_intrusion',
            NO_HAND_SANITIZATION: 'no_hand_sanitization',
            NO_BOOT_SANITIZATION: 'no_boot_sanitization',
          }
          const summaryKey = keyMap[complianceEvent.eventType]
          return {
            ...current,
            total: (current.total || 0) + 1,
            ...(summaryKey ? { [summaryKey]: (current[summaryKey] || 0) + 1 } : {}),
          }
        })
      },
    })

    return unsubscribe
  }, [filters, realtimeEnabled])

  const handleFilterChange = (patch) => {
    setFilters((current) => ({ ...current, ...patch }))
  }

  return (
    <div className="compliance-center">
      <header className="compliance-center__hero">
        <div>
          <span className="compliance-center__eyebrow">Evidence Center · AMS v1.7.1</span>
          <h1>Trung tâm bằng chứng tuân thủ</h1>
          <p>Vi phạm gì · Ở đâu · Khi nào · Ảnh bằng chứng — không video, không CCTV timeline.</p>
        </div>
      </header>

      <ComplianceSummary summary={summary} loading={loading} />

      <ComplianceFilters
        filters={filters}
        cameras={cameras}
        zones={zones}
        realtimeEnabled={realtimeEnabled}
        onChange={handleFilterChange}
        onRealtimeToggle={setRealtimeEnabled}
      />

      {error && <div className="compliance-center__error">{error}</div>}

      <section className="compliance-center__list panel">
        <div className="panel__header">
          <div>
            <h2 className="panel__title">Bằng chứng vi phạm</h2>
            <p className="panel__desc">
              {loading ? 'Đang tải…' : `${visibleEvents.length} / ${total} sự kiện`}
              {realtimeEnabled ? ' · Realtime bật' : ' · Realtime tắt'}
            </p>
          </div>
        </div>

        {loading ? (
          <div className="compliance-center__empty">Đang tải bằng chứng…</div>
        ) : visibleEvents.length === 0 ? (
          <div className="compliance-center__empty">
            <ShieldAlert size={28} />
            <p>Chưa có vi phạm tuân thủ phù hợp bộ lọc.</p>
          </div>
        ) : (
          <div className="compliance-center__grid">
            {visibleEvents.map((event) => (
              <ComplianceEventCard
                key={event.id}
                event={event}
                onOpenSnapshot={setSelectedEvent}
              />
            ))}
          </div>
        )}
      </section>

      <EvidenceSnapshotModal
        event={selectedEvent}
        open={Boolean(selectedEvent)}
        onClose={() => setSelectedEvent(null)}
      />
    </div>
  )
}

export default ComplianceCenterPage
