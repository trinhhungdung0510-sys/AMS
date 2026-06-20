import { cameras } from '../data/mockData'
import { Link } from 'react-router-dom'

function CameraPage() {
  return (
    <section className="panel">
      <div className="panel__header">
        <div>
          <h2>Danh sách camera</h2>
          <p>9 camera mẫu đang được AMS quản lý</p>
        </div>
        <Link className="btn btn--primary" to="/monitoring">Mở giám sát</Link>
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
              <th>Cảnh báo hôm nay</th>
            </tr>
          </thead>
          <tbody>
            {cameras.map((camera) => (
              <tr key={camera.id}>
                <td className="data-table__mono">{camera.id}</td>
                <td className="data-table__desc">{camera.name}</td>
                <td>{camera.zone}</td>
                <td className="data-table__mono">{camera.ip}</td>
                <td>
                  <span className={`status-pill status-pill--${camera.status}`}>
                    {camera.status === 'online' ? 'Online' : 'Offline'}
                  </span>
                </td>
                <td>{camera.resolution}</td>
                <td>{camera.uptime}%</td>
                <td>{camera.fps}</td>
                <td>{camera.alertsToday}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default CameraPage
