import { useEventStore } from '../../context/EventStore'

function formatEventTime(event) {
  const value = event.occurredAt || `${event.date}T${event.time || '00:00'}`
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return value || '--'
  return parsed.toLocaleString('vi-VN')
}

function RealtimeEventFeed({ limit = 50, filterCameraId = null }) {
  const { feedEvents, connected, loading, error, reload } = useEventStore()

  const items = (filterCameraId
    ? feedEvents.filter((item) => item.cameraId === filterCameraId)
    : feedEvents
  ).slice(0, limit)

  return (
    <aside className="realtime-feed panel panel--compact">
      <div className="panel__header">
        <h3 className="panel__title">Sự kiện realtime</h3>
        <span className={`realtime-feed__status${connected ? ' realtime-feed__status--online' : ''}`}>
          {connected ? 'Live' : 'Reconnecting...'}
        </span>
      </div>

      {error ? (
        <div className="realtime-feed__error">
          <p>{error}</p>
          <button type="button" className="btn btn--outline btn--sm" onClick={reload}>
            Thử lại
          </button>
        </div>
      ) : null}

      {loading && items.length === 0 ? (
        <p className="realtime-feed__empty">Đang tải sự kiện...</p>
      ) : null}

      {!loading && !error && items.length === 0 ? (
        <p className="realtime-feed__empty">Chưa có sự kiện realtime.</p>
      ) : null}

      {items.length > 0 ? (
        <ul className="realtime-feed__list">
          {items.map((event) => (
            <li key={event.id} className="realtime-feed__item">
              <strong>{event.typeLabel || event.eventType}</strong>
              <span>{event.zoneName || event.zoneId || event.cameraName}</span>
              <small>{formatEventTime(event)}</small>
            </li>
          ))}
        </ul>
      ) : null}
    </aside>
  )
}

export default RealtimeEventFeed
