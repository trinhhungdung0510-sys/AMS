import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { useAuth } from './AuthContext'
import { getEvents } from '../services/eventService'
import { apiFetch } from '../services/apiClient'
import { subscribeWsEvents } from '../services/wsClient'
import {
  computeEventMetrics,
  mergeEventLists,
  normalizeApiEvent,
  normalizeWsPayload,
  sortEventsByTime,
  upsertEvent,
} from '../utils/eventNormalizer'

const EventStoreContext = createContext(null)
const MAX_EVENTS = 500
const FEED_LIMIT = 50

function logWs(label, payload) {
  if (import.meta.env.DEV) {
    console.info(label, payload)
  }
}

export function EventStoreProvider({ children }) {
  const { user, loading: authLoading } = useAuth()
  const [events, setEvents] = useState([])
  const [cameras, setCameras] = useState([])
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastWsEvent, setLastWsEvent] = useState(null)
  const [lastNotification, setLastNotification] = useState(null)
  const reloadVersionRef = useRef(0)

  const applyEvent = useCallback((incoming, { fromWs = false } = {}) => {
    if (!incoming?.id) return

    setEvents((current) => sortEventsByTime(upsertEvent(current, incoming)).slice(0, MAX_EVENTS))

    if (fromWs) {
      setLastWsEvent(incoming)
    }
  }, [])

  const reload = useCallback(async () => {
    const reloadVersion = reloadVersionRef.current + 1
    reloadVersionRef.current = reloadVersion
    setLoading(true)
    setError(null)

    try {
      const [eventsData, cameraRes] = await Promise.all([
        getEvents(),
        apiFetch('/cameras'),
      ])

      if (!cameraRes.ok) {
        throw new Error(`Không tải được camera (${cameraRes.status})`)
      }

      const cameraData = await cameraRes.json()
      const normalizedEvents = (Array.isArray(eventsData) ? eventsData : []).map(normalizeApiEvent)

      if (reloadVersionRef.current !== reloadVersion) {
        return
      }

      setEvents((current) => mergeEventLists(normalizedEvents, current).slice(0, MAX_EVENTS))
      setCameras(Array.isArray(cameraData) ? cameraData : [])
    } catch (err) {
      if (reloadVersionRef.current === reloadVersion) {
        setError(err instanceof Error ? err.message : 'Không tải được sự kiện')
      }
    } finally {
      if (reloadVersionRef.current === reloadVersion) {
        setLoading(false)
      }
    }
  }, [])

  useEffect(() => {
    if (authLoading) return
    if (!user) {
      setEvents([])
      setCameras([])
      setLoading(false)
      setError(null)
      setLastWsEvent(null)
      setLastNotification(null)
      return
    }
    reload()
  }, [authLoading, user, reload])

  useEffect(() => {
    if (!user) return undefined

    return subscribeWsEvents({
      onConnect: () => setConnected(true),
      onDisconnect: () => setConnected(false),
      onMessage: (payload) => {
        logWs('[WS RAW]', payload)
        logWs('[WS TYPE]', payload?.type)

        if (payload?.type === 'event.created' || payload?.type === 'event.updated') {
          const normalized = normalizeWsPayload(payload)
          logWs('[WS PAYLOAD]', normalized)

          if (normalized) {
            applyEvent(normalized, { fromWs: true })
            return
          }

          if (import.meta.env.DEV) {
            console.warn('[WS PAYLOAD] normalizeWsPayload returned null', payload)
          }
          return
        }

        if (payload?.type === 'notification.created') {
          const notification = payload.payload?.notification ?? payload.payload
          if (notification) {
            setLastNotification(notification)
          }
        }
      },
    })
  }, [user, applyEvent])

  const metrics = useMemo(
    () => computeEventMetrics(events, cameras),
    [events, cameras],
  )

  const feedEvents = useMemo(() => events.slice(0, FEED_LIMIT), [events])

  const value = useMemo(
    () => ({
      events,
      feedEvents,
      cameras,
      metrics,
      connected,
      loading,
      error,
      reload,
      applyEvent,
      lastWsEvent,
      lastNotification,
    }),
    [events, feedEvents, cameras, metrics, connected, loading, error, reload, applyEvent, lastWsEvent, lastNotification],
  )

  return (
    <EventStoreContext.Provider value={value}>
      {children}
    </EventStoreContext.Provider>
  )
}

export function useEventStore() {
  const context = useContext(EventStoreContext)
  if (!context) {
    throw new Error('useEventStore must be used within EventStoreProvider')
  }
  return context
}
