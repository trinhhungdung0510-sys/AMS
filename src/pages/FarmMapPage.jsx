import { Link } from 'react-router-dom'
import { cameras, farmZones } from '../data/mockData'
import { getRiskLabel } from '../utils/formatters'

function FarmMapPage() {
  return (
    <div className="map-page">
      <section className="panel">
        <div className="panel__header">
          <div>
            <h2>Sơ đồ trang trại</h2>
            <p>Vị trí camera và trạng thái rủi ro theo khu vực</p>
          </div>
          <div className="map-legend">
            <span><i className="risk-dot risk-dot--online" /> Online</span>
            <span><i className="risk-dot risk-dot--warning" /> Cảnh báo</span>
            <span><i className="risk-dot risk-dot--danger" /> Mức cao</span>
            <span><i className="risk-dot risk-dot--offline" /> Offline</span>
          </div>
        </div>

        <div className="farm-map">
          {farmZones.map((zone) => (
            <div
              key={zone.id}
              className={`farm-zone farm-zone--${zone.risk}`}
              style={{
                left: `${zone.x}%`,
                top: `${zone.y}%`,
                width: `${zone.width}%`,
                height: `${zone.height}%`,
              }}
            >
              <strong>{zone.name}</strong>
            </div>
          ))}

          {cameras.map((camera) => (
            <Link
              key={camera.id}
              to={`/monitoring/${camera.id}`}
              className={`map-camera map-camera--${camera.risk}`}
              style={{ left: `${camera.mapX}%`, top: `${camera.mapY}%` }}
              title={`${camera.name} - ${getRiskLabel(camera.risk)}`}
            >
              <span>{camera.id.replace('CAM-', '')}</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}

export default FarmMapPage
