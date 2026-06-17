import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ChevronLeft } from 'lucide-react'
import CameraFeed from '../components/CameraFeed'
import ViolationCard from '../components/ViolationCard'
import {
  alertTypeOptions,
  getCameraById,
  getEventsByCamera,
  getViolationImagesByCamera,
  severityLabels,
  statusLabels,
} from '../data/mockData'
import { formatDateTime } from '../utils/formatters'

const timeFilters = [
  { value: 'all', label: 'Tất cả' },
  { value: 'today', label: 'Hôm nay' },
  { value: 'week', label: '7 ngày' },
  { value: 'month', label: '30 ngày' },
]

function CameraDetailPage() {
  const { cameraId } = useParams()
  const camera = getCameraById(cameraId)
  const alerts = useMemo(() => getEventsByCamera(cameraId), [cameraId])
  const [images, setImages] = useState(() => getViolationImagesByCamera(cameraId))
  const [timeFilter, setTimeFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')

  const filteredAlerts = useMemo(() => {
    let result = alerts
    if (timeFilter === 'today') result = result.filter((alert) => alert.date === '2026-06-17')
    if (timeFilter === 'week') result = result.filter((alert) => Number(alert.date.slice(-2)) >= 11)
    if (timeFilter === 'month') result = result.filter((alert) => alert.date.startsWith('2026-06'))
    if (typeFilter !== 'all') {
      result = result.filter((alert) => alert.type === typeFilter)
    }
    return result
  }, [alerts, timeFilter, typeFilter])

  const filteredImages = images.filter((image) =>
    filteredAlerts.some((alert) => alert.id === image.eventId),
  )

  const toggleResolved = (imageId) => {
    setImages((current) =>
      current.map((image) =>
        image.id === imageId ? { ...image, resolved: !image.resolved } : image,
      ),
    )
  }

  if (!camera) {
    return (
      <div className="camera-detail camera-detail--empty">
        <p>Không tìm thấy camera.</p>
        <Link className="btn btn--primary" to="/monitoring">Quay lại</Link>
      </div>
    )
  }

  return (
    <div className="camera-detail">
      <div className="camera-detail__topbar">
        <Link className="btn btn--outline" to="/monitoring">
          <ChevronLeft size={16} />
          Quay lại giám sát
        </Link>
        <div className="camera-detail__camera-info">
          <span className="camera-detail__id">{camera.id}</span>
          <span className={`status-pill status-pill--${camera.status}`}>
            {camera.status === 'online' ? 'Online' : 'Offline'}
          </span>
          <span className="camera-detail__ip">{camera.ip}</span>
        </div>
      </div>

      <div className="camera-detail__layout">
        <section className="camera-detail__video-section">
          <CameraFeed camera={camera} size="large" showActions />
          <div className="info-grid">
            <div><span>ID camera</span><strong>{camera.id}</strong></div>
            <div><span>IP camera</span><strong>{camera.ip}</strong></div>
            <div><span>Khu vực</span><strong>{camera.zone}</strong></div>
            <div><span>Trạng thái</span><strong>{camera.status === 'online' ? 'Online' : 'Offline'}</strong></div>
            <div><span>Uptime</span><strong>{camera.uptime}%</strong></div>
            <div><span>FPS</span><strong>{camera.fps}</strong></div>
          </div>
        </section>

        <aside className="camera-detail__sidebar">
          <section className="panel panel--compact">
            <div className="panel__header">
              <h2 className="panel__title">Bộ lọc</h2>
            </div>
            <div className="filter-panel">
              <div className="filter-panel__group">
                <span className="filter-panel__label">Thời gian</span>
                <div className="filter-chips">
                  {timeFilters.map((filter) => (
                    <button
                      key={filter.value}
                      type="button"
                      className={`filter-chip${timeFilter === filter.value ? ' filter-chip--active' : ''}`}
                      onClick={() => setTimeFilter(filter.value)}
                    >
                      {filter.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="filter-panel__group">
                <span className="filter-panel__label">Loại cảnh báo</span>
                <select
                  className="toolbar__select toolbar__select--full"
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                >
                  <option value="all">Tất cả loại</option>
                  {alertTypeOptions.map((item) => (
                    <option key={item.value} value={item.value}>{item.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </section>

          <section className="panel panel--compact">
            <div className="panel__header">
              <h2 className="panel__title">Danh sách cảnh báo</h2>
              <span className="panel__meta">{filteredAlerts.length} kết quả</span>
            </div>
            <ul className="alert-list">
              {filteredAlerts.length === 0 ? (
                <li className="alert-list__empty">Không có cảnh báo trong khoảng thời gian này.</li>
              ) : (
                filteredAlerts.map((alert) => (
                  <li key={alert.id} className="alert-list__item">
                    <div className="alert-list__time">
                      <span>{alert.time}</span>
                      <span>{alert.date.slice(5)}</span>
                    </div>
                    <div className="alert-list__body">
                      <span className="alert-list__type">{alert.typeLabel}</span>
                      <div className="alert-list__tags">
                        <span className={`badge badge--${alert.severity}`}>
                          {severityLabels[alert.severity]}
                        </span>
                        <span className={`status-tag status-tag--${alert.status}`}>
                          {statusLabels[alert.status]}
                        </span>
                        <span className="confidence-pill">{alert.confidence}% AI</span>
                      </div>
                    </div>
                  </li>
                ))
              )}
            </ul>
          </section>
        </aside>
      </div>

      <section className="panel">
        <div className="panel__header">
          <h2 className="panel__title">Ảnh vi phạm</h2>
          <span className="panel__meta">{filteredImages.length} ảnh</span>
        </div>
        {filteredImages.length === 0 ? (
          <div className="violation-empty">Chưa có ảnh vi phạm trong khoảng thời gian đã chọn.</div>
        ) : (
          <div className="violation-grid">
            {filteredImages.map((image) => (
              <ViolationCard
                key={image.id}
                image={{ ...image, time: formatDateTime(image.time.slice(0, 10), image.time.slice(11)) }}
                onResolve={toggleResolved}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default CameraDetailPage
