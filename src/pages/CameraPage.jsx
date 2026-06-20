import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getCameras, getCameraIp } from '../services/cameraService'

function CameraPage() {
  const [cameras, setCameras] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCameras()
  }, [])

  async function loadCameras() {
    try {
      const data = await getCameras()
      setCameras(data)
    } catch (error) {
      console.error('Load cameras failed', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <section className="panel">Đang tải camera...</section>
  }

  return (
    <section className="panel">
      <div className="panel__header">
        <div>
          <h2>Danh sách camera</h2>
          <p>{cameras.length} camera đang được AMS quản lý</p>
        </div>

        <Link className="btn btn--primary" to="/monitoring">
          Mở giám sát
        </Link>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tên camera</th>
              <th>Khu vực</th>
              <th>IP</th>
              <th>Trạng thái</th>
              <th>Độ phân giải</th>
              <th>Uptime</th>
              <th>FPS</th>
              <th>Active</th>
            </tr>
          </thead>

          <tbody>
            {cameras.map((camera) => (
              <tr key={camera.id}>
                <td className="data-table__mono">{camera.id}</td>
                <td className="data-table__desc">{camera.name}</td>
                <td>{camera.zone}</td>
                <td className="data-table__mono">{getCameraIp(camera)}</td>

                <td>
                  <span
                    className={`status-pill status-pill--${camera.status}`}
                  >
                    {camera.status}
                  </span>
                </td>

                <td>{camera.resolution}</td>
                <td>{camera.uptime}%</td>
                <td>{camera.fps}</td>

                <td>
                  {camera.is_active ? '✅' : '❌'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default CameraPage
