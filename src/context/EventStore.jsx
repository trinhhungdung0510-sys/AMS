import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'
import { useAuth } from './AuthContext'
import { useDashboardBootstrap } from './DashboardBootstrapStore'
import { subscribeWsEvents } from '../services/wsClient'
import {
  computeEventMetrics,
  normalizeEngineEvent,
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

function normalizeBootstrapEvents(items = []) {
  return items.map((event) => normalizeEngineEvent(event)).filter(Boolean)
}

export function EventStoreProvider({ children }) {
  const { user, loading: authLoading } = useAuth()
  const { data: bootstrap, loading: bootstrapLoading, error: bootstrapError } = useDashboardBootstrap()
  const [events, setEvents] = useState([])
  const [cameras, setCameras] = useState([])
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastWsEvent, setLastWsEvent] = useState(null)
  const [lastNotification, setLastNotification] = useState(null)
  const [lastGmailFailure, setLastGmailFailure] = useState(null)

  const applyEvent = useCallback((incoming, { fromWs = false } = {}) => {
    if (!incoming?.id) return

    setEvents((current) => sortEventsByTime(upsertEvent(current, incoming)).slice(0, MAX_EVENTS))

    if (fromWs) {
      setLastWsEvent(incoming)
    }
  }, [])

  const removeEvent = useCallback((eventId) => {
    if (!eventId) return
    setEvents((current) => current.filter((item) => item.id !== eventId))
  }, [])

  useEffect(() => {
    if (authLoading || bootstrapLoading) {
      return
    }

    if (!user) {
      setEvents([])
      setCameras([])
      setLoading(false)
      setError(null)
      setLastWsEvent(null)
      setLastNotification(null)
      setLastGmailFailure(null)
      return
    }

    if (bootstrap?.recentEvents && bootstrap?.cameraSummary) {
      setEvents(normalizeBootstrapEvents(bootstrap.recentEvents.items))
      setCameras(Array.isArray(bootstrap.cameraSummary.cameras) ? bootstrap.cameraSummary.cameras : [])
      setLoading(false)
      setError(null)
      return
    }

    setLoading(false)
    setError(bootstrapError || 'Không tải được sự kiện')
  }, [authLoading, bootstrapLoading, user, bootstrap, bootstrapError])

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

        if (payload?.type === 'event.removed') {
          const eventId = payload.payload?.event?.id || payload.payload?.id
          removeEvent(eventId)
          return
        }

        if (payload?.type === 'notification.created') {
          const notification = payload.payload?.notification ?? payload.payload
          if (notification) {
            setLastNotification(notification)
          }
          return
        }

        if (payload?.type === 'notification.gmail_failed') {
          const alert = payload.payload?.alert ?? payload.payload
          if (alert) {
            setLastGmailFailure({
              message: alert.message || alert.title || 'Gửi Email thất bại',
              eventId: alert.eventId,
              sentAt: payload.timestamp,
            })
          }
        }
      },
    })
  }, [user, applyEvent, removeEvent])

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
      lastWsEvent,
      lastNotification,
      lastGmailFailure,
    }),
    [events, feedEvents, cameras, metrics, connected, loading, error, lastWsEvent, lastNotification, lastGmailFailure],
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
