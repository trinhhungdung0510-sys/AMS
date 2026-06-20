import { Activity, AlertTriangle, Camera, Radio, ShieldAlert } from 'lucide-react'
import { useEventStore } from '../../context/EventStore'

function RealtimeDashboardWidgets() {
  const { metrics, feedEvents, connected, loading, error, reload } = useEventStore()

  const cards = [
    { label: 'Event đang mở', value: metrics.openEvents, icon: ShieldAlert, tone: 'orange' },
    { label: 'Event nghiêm trọng', value: metrics.criticalEvents, icon: AlertTriangle, tone: 'red' },
    { label: 'Sự kiện hôm nay', value: metrics.totalEventsToday, icon: Activity, tone: 'green' },
    { label: 'Camera online', value: `${metrics.onlineCameras}/${metrics.totalCameras}`, icon: Radio, tone: 'green' },
  ]

  return (
    <section className="realtime-dashboard">
      <div className="realtime-dashboard__header">
        <h2>Realtime Dashboard</h2>
        <span className={`realtime-feed__status${connected ? ' realtime-feed__status--online' : ''}`}>
          {connected ? 'WS connected' : 'WS reconnecting'}
        </span>
      </div>

      {error ? (
        <div className="realtime-feed__error">
          <p>{error}</p>
          <button type="button" className="btn btn--outline btn--sm" onClick={reload}>
            Tải lại
          </button>
        </div>
      ) : null}

      <div className="stat-grid">
        {cards.map((card) => (
          <article key={card.label} className={`metric-card metric-card--${card.tone}`}>
            <div>
              <span className="metric-card__label">{card.label}</span>
              <strong>{loading && card.value === 0 ? '…' : card.value}</strong>
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
          <Camera size={16} />
        </div>
        {feedEvents.length === 0 && !loading ? (
          <p className="realtime-feed__empty">Chưa có sự kiện.</p>
        ) : (
          <ul className="realtime-feed__list">
            {feedEvents.slice(0, 5).map((event) => (
              <li key={event.id} className="realtime-feed__item">
                <strong>{event.typeLabel || event.eventType}</strong>
                <span>{event.zoneName || event.cameraName || event.cameraId}</span>
              </li>
            ))}
          </ul>
        )}
      </article>
    </section>
  )
}

export default RealtimeDashboardWidgets
