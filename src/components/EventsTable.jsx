import { events, severityLabels } from '../data/mockData'

function EventsTable({ compact = false, onViewAll }) {
  const displayEvents = compact ? events.slice(0, 3) : events

  return (
    <section className="panel">
      <div className="panel__header">
        <h2 className="panel__title">
          {compact ? 'Sự kiện gần nhất' : 'Danh sách sự kiện'}
        </h2>
        {compact && onViewAll && (
          <button type="button" className="panel__link" onClick={onViewAll}>
            Xem tất cả
          </button>
        )}
      </div>

      <div className="table-wrapper">
        <table className="events-table">
          <thead>
            <tr>
              <th>Thời gian</th>
              <th>Sự kiện</th>
              <th>Vị trí</th>
              <th>Mức độ</th>
            </tr>
          </thead>
          <tbody>
            {displayEvents.map((event) => (
              <tr key={event.id}>
                <td className="events-table__time">{event.time}</td>
                <td>{event.description}</td>
                <td className="events-table__location">{event.location}</td>
                <td>
                  <span className={`badge badge--${event.severity}`}>
                    {severityLabels[event.severity]}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default EventsTable
