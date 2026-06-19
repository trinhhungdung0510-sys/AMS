import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import CameraFeed from '../components/CameraFeed'
import { getCameras } from '../services/cameraService'

function MonitoringPage() {
  const [cameras, setCameras] = useState([])
  const [zoneFilter, setZoneFilter] = useState('Tất cả khu vực')

  useEffect(() => {
    loadCameras()

    const timer = setInterval(loadCameras, 10000)

    return () => clearInterval(timer)
  }, [])

  async function loadCameras() {
    try {
      const data = await getCameras()
      setCameras(data)
    } catch (error) {
      console.error(error)
    }
  }

  const zones = useMemo(() => {
    return [
      'Tất cả khu vực',
      ...new Set(cameras.map((camera) => camera.zone)),
    ]
  }, [cameras])

  const filteredCameras = useMemo(() => {
    if (zoneFilter === 'Tất cả khu vực') {
      return cameras
    }

    return cameras.filter(
      (camera) => camera.zone === zoneFilter
    )
  }, [cameras, zoneFilter])

  return (
    <div className="monitoring-page">

      <div className="panel">
        <div className="panel__header">
          <h2>Giám sát Camera</h2>

          <select
            value={zoneFilter}
            onChange={(e) => setZoneFilter(e.target.value)}
          >
            {zones.map((zone) => (
              <option key={zone} value={zone}>
                {zone}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="monitoring-grid">
        {filteredCameras.map((camera) => (
          <Link
            key={camera.id}
            to={`/monitoring/${camera.id}`}
            className="monitor-card"
          >
            <CameraFeed camera={camera} />

            <div className="monitor-card__body">
              <h3>{camera.name}</h3>

              <p>{camera.zone}</p>

              <div>
                {camera.status}
                {' | '}
                {camera.resolution}
                {' | '}
                {camera.fps} FPS
              </div>

              <div>
                Uptime: {camera.uptime}%
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default MonitoringPage
