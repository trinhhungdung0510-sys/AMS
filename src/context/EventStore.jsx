import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'
import { useAuth } from './AuthContext'
import { getEvents } from '../services/eventService'
import { apiFetch } from '../services/apiClient'
import { subscribeWsEvents } from '../services/wsClient'
import {
  computeEventMetrics,
  normalizeApiEvent,
  normalizeWsPayload,
  upsertEvent,
} from '../utils/eventNormalizer'

const EventStoreContext = createContext(null)
const MAX_EVENTS = 500
const FEED_LIMIT = 50

export function EventStoreProvider({ children }) {
  const { user, loading: authLoading } = useAuth()
  const [events, setEvents] = useState([])
  const [cameras, setCameras] = useState([])
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const applyEvent = useCallback((incoming) => {
    if (!incoming?.id) return
    setEvents((current) => upsertEvent(current, incoming).slice(0, MAX_EVENTS))
  }, [])

  const reload = useCallback(async () => {
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
      const normalizedEvents = eventsData.map(normalizeApiEvent)
      setEvents(normalizedEvents.slice(0, MAX_EVENTS))
      setCameras(cameraData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không tải được sự kiện')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (authLoading) return
    if (!user) {
      setEvents([])
      setCameras([])
      setLoading(false)
      setError(null)
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
        if (payload.type === 'event.created' || payload.type === 'event.updated') {
          const normalized = normalizeWsPayload(payload)
          if (normalized) applyEvent(normalized)
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
    }),
    [events, feedEvents, cameras, metrics, connected, loading, error, reload, applyEvent],
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
