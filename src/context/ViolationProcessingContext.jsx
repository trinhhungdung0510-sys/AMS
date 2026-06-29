import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from 'react'
import { useAuth } from './AuthContext'
import { useEventStore } from './EventStore'
import { buildViolationDetail, mergeViolationOverrides } from '../utils/violationDetailModel'
import { isOpenViolation, isTodayValue, mapSourceStatusKey } from '../utils/violationStatus'

const ViolationProcessingContext = createContext(null)

export function ViolationProcessingProvider({ children }) {
  const { user } = useAuth()
  const { feedEvents, events } = useEventStore()
  const [selectedSource, setSelectedSource] = useState(null)
  const [overrides, setOverrides] = useState({})

  const getOverride = useCallback((id) => (id ? overrides[id] : null), [overrides])

  const getStatusKey = useCallback(
    (source) => mapSourceStatusKey(source, getOverride(source?.id)),
    [getOverride],
  )

  const isViolationOpen = useCallback(
    (source) => isOpenViolation(source, getOverride(source?.id)),
    [getOverride],
  )

  const openViolation = useCallback((source) => {
    if (!source) return
    setSelectedSource(source)
  }, [])

  const closeViolation = useCallback(() => {
    setSelectedSource(null)
  }, [])

  const updateViolationState = useCallback((id, patch) => {
    if (!id) return
    setOverrides((current) => ({
      ...current,
      [id]: { ...current[id], ...patch },
    }))
  }, [])

  const resolveViolation = useCallback((source, { note = '' } = {}) => {
    const id = source?.id
    if (!id) return

    setOverrides((current) => ({
      ...current,
      [id]: {
        ...current[id],
        statusKey: 'resolved',
        note,
        resolvedAt: new Date().toISOString(),
        handler: user?.full_name || user?.email || 'Quản lý trại',
        snapshot: buildViolationDetail(source),
        source,
      },
    }))
    setSelectedSource(null)
  }, [user])

  const openFeedEvents = useMemo(
    () => (Array.isArray(feedEvents) ? feedEvents : []).filter((event) => isViolationOpen(event)),
    [feedEvents, isViolationOpen],
  )

  const openEvents = useMemo(
    () => (Array.isArray(events) ? events : []).filter((event) => isViolationOpen(event)),
    [events, isViolationOpen],
  )

  const resolvedRecords = useMemo(
    () => Object.entries(overrides)
      .filter(([, value]) => value.statusKey === 'resolved')
      .map(([id, value]) => ({
        id,
        ...(value.source || value.snapshot?.raw || {}),
        typeLabel: value.snapshot?.typeLabel,
        cameraName: value.snapshot?.cameraName,
        zoneName: value.snapshot?.zoneName,
        confidence: value.snapshot?.confidence,
        occurredAt: value.snapshot?.occurredAt,
        snapshotUrl: value.snapshot?.snapshotUrl,
        note: value.note || '',
        handler: value.handler || 'Quản lý trại',
        resolvedAt: value.resolvedAt,
        statusKey: 'resolved',
        raw: value.source || value.snapshot?.raw,
      }))
      .sort((left, right) => String(right.resolvedAt || '').localeCompare(String(left.resolvedAt || ''))),
    [overrides],
  )

  const openMetrics = useMemo(() => {
    const today = new Date().toISOString().slice(0, 10)
    const openToday = openEvents.filter((event) => isTodayValue(event.occurredAt || event.date, today))
    return {
      openTotal: openEvents.length,
      openToday: openToday.length,
      openCritical: openEvents.filter((event) => event.severityRaw === 'CRITICAL').length,
      resolvedTotal: resolvedRecords.length,
    }
  }, [openEvents, resolvedRecords.length])

  const detail = useMemo(() => {
    if (!selectedSource) return null
    const base = buildViolationDetail(selectedSource)
    const id = base?.id
    return mergeViolationOverrides(base, id ? overrides[id] : {})
  }, [selectedSource, overrides])

  const value = useMemo(
    () => ({
      detail,
      selectedSource,
      isDrawerOpen: Boolean(selectedSource),
      overrides,
      openViolation,
      closeViolation,
      updateViolationState,
      resolveViolation,
      getStatusKey,
      isViolationOpen,
      getOverride,
      openFeedEvents,
      openEvents,
      resolvedRecords,
      openMetrics,
    }),
    [
      detail,
      selectedSource,
      overrides,
      openViolation,
      closeViolation,
      updateViolationState,
      resolveViolation,
      getStatusKey,
      isViolationOpen,
      getOverride,
      openFeedEvents,
      openEvents,
      resolvedRecords,
      openMetrics,
    ],
  )

  return (
    <ViolationProcessingContext.Provider value={value}>
      {children}
    </ViolationProcessingContext.Provider>
  )
}

export function useViolationProcessing() {
  const context = useContext(ViolationProcessingContext)
  if (!context) {
    throw new Error('useViolationProcessing must be used within ViolationProcessingProvider')
  }
  return context
}
