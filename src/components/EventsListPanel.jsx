import { useMemo, useState } from 'react'
import { Download, Search } from 'lucide-react'
import { useEventStore } from '../context/EventStore'
import { useDashboardBootstrap } from '../context/DashboardBootstrapStore'
import { useViolationProcessing } from '../context/ViolationProcessingContext'
import { severityLabels, statusLabels } from '../data/mockData'
import { exportRowsAsExcel, formatDateTime } from '../utils/formatters'

const pageSize = 10

function EventsListPanel() {
  const { events, loading, error } = useEventStore()
  const { retry } = useDashboardBootstrap()
  const { openViolation } = useViolationProcessing()
  const [search, setSearch] = useState('')
  const [timeFilter, setTimeFilter] = useState('all')
  const [page, setPage] = useState(1)

  const today = new Date().toISOString().slice(0, 10)

  const filtered = useMemo(() => events.filter((event) => {
    const query = search.trim().toLowerCase()
    const matchSearch =
      query === '' ||
      String(event.typeLabel || event.eventType || '').toLowerCase().includes(query) ||
      String(event.cameraName || '').toLowerCase().includes(query) ||
      String(event.zoneName || '').toLowerCase().includes(query) ||
      String(event.handler || '').toLowerCase().includes(query)

    const matchTime =
      timeFilter === 'all' ||
      (timeFilter === 'today' && (event.date === today || event.occurredAt?.startsWith(today))) ||
      (timeFilter === 'week' && event.date) ||
      (timeFilter === 'month' && event.date?.startsWith(today.slice(0, 7)))

    return matchSearch && matchTime
  }), [events, search, timeFilter, today])

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize))
  const currentPage = Math.min(page, totalPages)
  const rows = filtered.slice((currentPage - 1) * pageSize, currentPage * pageSize)

  const exportExcel = () => {
    exportRowsAsExcel(
      'ams-events.xls',
      filtered.map((event) => ({
        'Thời gian': formatDateTime(event.date, event.time),
        'Loại cảnh báo': event.typeLabel,
        Camera: event.cameraName,
        'Khu vực': event.zoneName,
        'Mức độ': severityLabels[event.severity] || event.severityRaw,
        'Trạng thái': statusLabels[event.status] || event.statusRaw,
        'Người xử lý': event.handler,
        'AI (%)': event.confidence,
      })),
    )
  }

  return (
    <div className="events-page events-page--embedded">
      {error ? (
        <div className="realtime-feed__error">
          <p>{error}</p>
          <button type="button" className="btn btn--outline btn--sm" onClick={retry}>
            Tải lại sự kiện
          </button>
        </div>
      ) : null}

      <div className="toolbar">
        <div className="toolbar__left">
          <div className="search-box">
            <Search size={16} />
            <input
              type="search"
              className="search-box__input"
              placeholder="Tìm loại cảnh báo, camera, khu vực, người xử lý..."
              value={search}
              onChange={(event) => {
                setSearch(event.target.value)
                setPage(1)
              }}
            />
          </div>
        </div>
        <div className="toolbar__right">
          <select
            className="toolbar__select"
            value={timeFilter}
            onChange={(event) => {
              setTimeFilter(event.target.value)
              setPage(1)
            }}
          >
            <option value="all">Tất cả thời gian</option>
            <option value="today">Hôm nay</option>
            <option value="week">7 ngày</option>
            <option value="month">30 ngày</option>
          </select>
          <button type="button" className="btn btn--outline" onClick={exportExcel}>
            <Download size={16} />
            Xuất Excel
          </button>
        </div>
      </div>

      <section className="panel panel--flush">
        {loading && rows.length === 0 ? (
          <p className="realtime-feed__empty">Đang tải sự kiện...</p>
        ) : null}

        {!loading && rows.length === 0 ? (
          <p className="realtime-feed__empty">Không có sự kiện phù hợp bộ lọc.</p>
        ) : (
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Thời gian</th>
                  <th>Loại cảnh báo</th>
                  <th>Camera</th>
                  <th>Khu vực</th>
                  <th>Mức độ</th>
                  <th>Trạng thái</th>
                  <th>Người xử lý</th>
                  <th>AI</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((event) => (
                  <tr key={event.id} className="data-table__row--clickable" onClick={() => openViolation(event)}>
                    <td className="data-table__time">{formatDateTime(event.date, event.time)}</td>
                    <td className="data-table__desc">{event.typeLabel}</td>
                    <td>{event.cameraName}</td>
                    <td>{event.zoneName}</td>
                    <td>
                      <span className={`badge badge--${event.severity}`}>
                        {severityLabels[event.severity] || event.severityRaw}
                      </span>
                    </td>
                    <td>
                      <span className={`status-tag status-tag--${event.status}`}>
                        {statusLabels[event.status] || event.statusRaw}
                      </span>
                    </td>
                    <td>{event.handler}</td>
                    <td><span className="confidence-pill">{event.confidence}%</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="table-footer">
          <span className="table-footer__info">
            Hiển thị {rows.length} / {filtered.length} sự kiện
          </span>
          <div className="pagination">
            <button
              type="button"
              className="pagination__btn"
              disabled={currentPage === 1}
              onClick={() => setPage((value) => Math.max(1, value - 1))}
            >
              Trước
            </button>
            <span className="pagination__label">{currentPage} / {totalPages}</span>
            <button
              type="button"
              className="pagination__btn"
              disabled={currentPage === totalPages}
              onClick={() => setPage((value) => Math.min(totalPages, value + 1))}
            >
              Sau
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}

export default EventsListPanel
