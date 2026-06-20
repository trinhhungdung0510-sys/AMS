import { getEventStatusLabel, getRuleTypeLabel, getSeverityLabel, getSeverityTone } from '../../config/rules'
import { formatDateTime } from '../../utils/formatters'

function formatEventTime(isoString) {
  if (!isoString) return '—'
  const normalized = isoString.includes('T') ? isoString : isoString.replace(' ', 'T')
  const datePart = normalized.slice(0, 10)
  const timePart = normalized.slice(11, 16)
  return formatDateTime(datePart, timePart)
}

function EventTimeline({ events, loading, emptyMessage }) {
  if (loading) {
    return <div className="event-timeline__loading">Đang tải timeline...</div>
  }

  if (!events.length) {
    return <p className="event-timeline__empty">{emptyMessage || 'Chưa có sự kiện nào.'}</p>
  }

  return (
    <div className="event-timeline">
      <table className="event-timeline__table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Camera</th>
            <th>Zone</th>
            <th>Rule</th>
            <th>Severity</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => (
            <tr key={event.id}>
              <td>{formatEventTime(event.started_at || event.created_at)}</td>
              <td>{event.camera_name || event.camera_id}</td>
              <td>{event.zone_name || event.zone_id || '—'}</td>
              <td>
                <div className="event-timeline__rule">
                  <strong>{event.rule_name || event.rule_id || '—'}</strong>
                  <small>{getRuleTypeLabel(event.event_type)}</small>
                </div>
              </td>
              <td>
                <span className={`badge badge--${getSeverityTone(event.severity)}`}>
                  {getSeverityLabel(event.severity)}
                </span>
              </td>
              <td>{getEventStatusLabel(event.status)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default EventTimeline
