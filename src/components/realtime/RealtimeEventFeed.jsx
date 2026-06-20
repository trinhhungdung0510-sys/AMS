import { useEffect, useState } from 'react'
import { useRealtimeEvents } from '../../hooks/useRealtimeEvents'
import { formatDateTime } from '../../utils/formatters'

function extractEvent(payload) {
  const data = payload?.payload || payload
  return data?.event || null
}

function RealtimeEventFeed({ limit = 8, filterCameraId = null }) {
  const [items, setItems] = useState([])
  const { connected } = useRealtimeEvents({
    filterCameraId,
    eventTypes: ['event.created', 'event.updated'],
    onMessage: (payload) => {
      const event = extractEvent(payload)
      if (!event) return
      setItems((current) => [event, ...current.filter((item) => item.id !== event.id)].slice(0, limit))
    },
  })

  return (
    <aside className="realtime-feed panel panel--compact">
      <div className="panel__header">
        <h3 className="panel__title">Sự kiện realtime</h3>
        <span className={`realtime-feed__status${connected ? ' realtime-feed__status--online' : ''}`}>
          {connected ? 'Live' : 'Reconnecting...'}
        </span>
      </div>
      {items.length === 0 ? (
        <p className="realtime-feed__empty">Chưa có sự kiện realtime.</p>
      ) : (
        <ul className="realtime-feed__list">
          {items.map((event) => (
            <li key={event.id} className="realtime-feed__item">
              <strong>{event.event_type || event.alert_type}</strong>
              <span>{event.zone_name || event.zone_id}</span>
              <small>
                {formatDateTime(
                  (event.occurred_at || event.started_at || '').slice(0, 10),
                  (event.occurred_at || event.started_at || '').slice(11, 19),
                )}
              </small>
            </li>
          ))}
        </ul>
      )}
    </aside>
  )
}

export default RealtimeEventFeed
