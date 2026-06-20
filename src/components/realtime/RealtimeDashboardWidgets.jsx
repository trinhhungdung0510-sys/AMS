import { useEffect, useState } from 'react'
import { Activity, AlertTriangle, Camera, Radio, ShieldAlert } from 'lucide-react'
import { useRealtimeEvents } from '../../hooks/useRealtimeEvents'
import { apiFetch } from '../../services/apiClient'

const initialStats = {
  activeCameras: 0,
  onlineCameras: 0,
  openEvents: 0,
  criticalEvents: 0,
}

function RealtimeDashboardWidgets() {
  const [stats, setStats] = useState(initialStats)
  const [recentEvents, setRecentEvents] = useState([])
  const { connected } = useRealtimeEvents({
    onMessage: (payload) => {
      if (payload.type === 'event.created') {
        const event = payload.payload?.event
        if (!event) return
        setRecentEvents((current) => [event, ...current].slice(0, 5))
        setStats((current) => ({
          ...current,
          openEvents: current.openEvents + (event.status === 'OPEN' ? 1 : 0),
          criticalEvents: current.criticalEvents + (event.severity === 'CRITICAL' ? 1 : 0),
        }))
      }

      if (payload.type === 'camera.status') {
        const data = payload.payload || {}
        setStats((current) => ({
          ...current,
          onlineCameras: data.status === 'ONLINE'
            ? current.onlineCameras + 1
            : Math.max(0, current.onlineCameras - 1),
        }))
      }
    },
  })

  useEffect(() => {
    const loadBaseline = async () => {
      try {
        const [cameraRes, healthRes, eventsRes] = await Promise.all([
          apiFetch('/cameras'),
          apiFetch('/camera-health'),
          apiFetch('/events/engine'),
        ])

        const cameras = cameraRes.ok ? await cameraRes.json() : []
        const health = healthRes.ok ? await healthRes.json() : []
        const events = eventsRes.ok ? await eventsRes.json() : []

        setStats({
          activeCameras: cameras.length,
          onlineCameras: health.filter((item) => item.status === 'ONLINE').length,
          openEvents: events.filter((item) => item.status === 'OPEN').length,
          criticalEvents: events.filter((item) => item.severity === 'CRITICAL').length,
        })
        setRecentEvents(events.slice(0, 5))
      } catch {
        // keep defaults
      }
    }

    loadBaseline()
  }, [])

  const cards = [
    { label: 'Camera hoạt động', value: stats.activeCameras, icon: Camera, tone: 'green' },
    { label: 'Camera online', value: stats.onlineCameras, icon: Radio, tone: 'green' },
    { label: 'Event đang mở', value: stats.openEvents, icon: ShieldAlert, tone: 'orange' },
    { label: 'Event nghiêm trọng', value: stats.criticalEvents, icon: AlertTriangle, tone: 'red' },
  ]

  return (
    <section className="realtime-dashboard">
      <div className="realtime-dashboard__header">
        <h2>Realtime Dashboard</h2>
        <span className={`realtime-feed__status${connected ? ' realtime-feed__status--online' : ''}`}>
          {connected ? 'WS connected' : 'WS reconnecting'}
        </span>
      </div>

      <div className="stat-grid">
        {cards.map((card) => (
          <article key={card.label} className={`metric-card metric-card--${card.tone}`}>
            <div>
              <span className="metric-card__label">{card.label}</span>
              <strong>{card.value}</strong>
            </div>
            <span className="metric-card__icon">
              <card.icon size={22} />
            </span>
          </article>
        ))}
      </div>

      <article className="panel panel--compact">
        <div className="panel__header">
          <h3 className="panel__title">Recent Events</h3>
          <Activity size={16} />
        </div>
        {recentEvents.length === 0 ? (
          <p className="realtime-feed__empty">Chưa có sự kiện.</p>
        ) : (
          <ul className="realtime-feed__list">
            {recentEvents.map((event) => (
              <li key={event.id} className="realtime-feed__item">
                <strong>{event.event_type}</strong>
                <span>{event.zone_name || event.camera_id}</span>
              </li>
            ))}
          </ul>
        )}
      </article>
    </section>
  )
}

export default RealtimeDashboardWidgets
