import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import CameraFeed from '../components/CameraFeed'
import { cameras } from '../data/mockData'

const zoneFilters = ['Tất cả khu vực', 'Cổng trại', 'Khu nái', 'Khu đực giống', 'Khu cách ly']

function MonitoringPage() {
  const [zoneFilter, setZoneFilter] = useState('Tất cả khu vực')

  const filteredCameras = useMemo(() => {
    if (zoneFilter === 'Tất cả khu vực') return cameras
    return cameras.filter((camera) => camera.zone === zoneFilter)
  }, [zoneFilter])

  return (
    <div className="monitoring-page">
      <div className="toolbar">
        <div className="toolbar__left">
          <span className="toolbar__count">Lưới camera 3x3</span>
          <span className="toolbar__divider" />
          <span className="toolbar__meta">{filteredCameras.length} camera hiển thị</span>
        </div>
        <div className="toolbar__right">
          <select
            className="toolbar__select"
            value={zoneFilter}
            onChange={(event) => setZoneFilter(event.target.value)}
          >
            {zoneFilters.map((zone) => (
              <option key={zone} value={zone}>
                {zone}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="monitoring-grid">
        {filteredCameras.map((camera) => (
          <Link key={camera.id} to={`/monitoring/${camera.id}`} className="monitor-card">
            <CameraFeed camera={camera} />
            <div className="monitor-card__body">
              <div>
                <h3>{camera.name}</h3>
                <p>{camera.zone}</p>
              </div>
              <span className={`status-pill status-pill--${camera.status}`}>
                {camera.status === 'online' ? 'LIVE' : 'OFFLINE'}
              </span>
            </div>
            <div className="monitor-card__meta">
              <span>{camera.resolution}</span>
              <span>Uptime {camera.uptime}%</span>
              <span>{camera.alertsToday} cảnh báo</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default MonitoringPage
