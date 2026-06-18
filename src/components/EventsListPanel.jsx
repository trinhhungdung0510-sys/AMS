import { useState } from 'react'
import { Download, Search } from 'lucide-react'
import { alertTypeOptions, events, severityLabels, statusLabels } from '../data/mockData'
import { exportRowsAsExcel, formatDateTime } from '../utils/formatters'

const pageSize = 10
const timeOptions = [
  { value: 'all', label: 'Tất cả thời gian' },
  { value: 'today', label: 'Hôm nay' },
  { value: 'week', label: '7 ngày' },
  { value: 'month', label: '30 ngày' },
]

function EventsListPanel() {
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('all')
  const [timeFilter, setTimeFilter] = useState('all')
  const [page, setPage] = useState(1)

  const filtered = events.filter((event) => {
    const query = search.trim().toLowerCase()
    const matchSearch =
      query === '' ||
      event.typeLabel.toLowerCase().includes(query) ||
      event.cameraName.toLowerCase().includes(query) ||
      event.zone.toLowerCase().includes(query) ||
      event.handler.toLowerCase().includes(query)

    const matchType = typeFilter === 'all' || event.type === typeFilter
    const matchTime =
      timeFilter === 'all' ||
      (timeFilter === 'today' && event.date === '2026-06-17') ||
      (timeFilter === 'week' && Number(event.date.slice(-2)) >= 11) ||
      (timeFilter === 'month' && event.date.startsWith('2026-06'))

    return matchSearch && matchType && matchTime
  })

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize))
  const currentPage = Math.min(page, totalPages)
  const rows = filtered.slice((currentPage - 1) * pageSize, currentPage * pageSize)

  const exportExcel = () => {
    exportRowsAsExcel(
      'ams-events-v0.4.xls',
      filtered.map((event) => ({
        'Thời gian': formatDateTime(event.date, event.time),
        'Loại cảnh báo': event.typeLabel,
        Camera: event.cameraName,
        'Khu vực': event.zone,
        'Mức độ': severityLabels[event.severity],
        'Trạng thái': statusLabels[event.status],
        'Người xử lý': event.handler,
        'AI (%)': event.confidence,
      })),
    )
  }

  return (
    <div className="events-page events-page--embedded">
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
            value={typeFilter}
            onChange={(event) => {
              setTypeFilter(event.target.value)
              setPage(1)
            }}
          >
            <option value="all">Tất cả loại</option>
            {alertTypeOptions.map((item) => (
              <option key={item.value} value={item.value}>{item.label}</option>
            ))}
          </select>
          <select
            className="toolbar__select"
            value={timeFilter}
            onChange={(event) => {
              setTimeFilter(event.target.value)
              setPage(1)
            }}
          >
            {timeOptions.map((item) => (
              <option key={item.value} value={item.value}>{item.label}</option>
            ))}
          </select>
          <button type="button" className="btn btn--outline" onClick={exportExcel}>
            <Download size={16} />
            Xuất Excel
          </button>
        </div>
      </div>

      <section className="panel panel--flush">
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
                <tr key={event.id}>
                  <td className="data-table__time">{formatDateTime(event.date, event.time)}</td>
                  <td className="data-table__desc">{event.typeLabel}</td>
                  <td>{event.cameraName}</td>
                  <td>{event.zone}</td>
                  <td>
                    <span className={`badge badge--${event.severity}`}>
                      {severityLabels[event.severity]}
                    </span>
                  </td>
                  <td>
                    <span className={`status-tag status-tag--${event.status}`}>
                      {statusLabels[event.status]}
                    </span>
                  </td>
                  <td>{event.handler}</td>
                  <td><span className="confidence-pill">{event.confidence}%</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

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
