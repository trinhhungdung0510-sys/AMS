import { cameras, onlineCameraCount } from '../data/mockData'

function CameraStatus() {
  const statusCameras = cameras.slice(0, 4)

  return (
    <section className="panel">
      <div className="panel__header">
        <h2 className="panel__title">Trạng thái camera</h2>
        <span className="panel__meta">
          {onlineCameraCount}/{cameras.length} online
        </span>
      </div>

      <ul className="camera-list">
        {statusCameras.map((camera) => (
          <li key={camera.id} className="camera-item">
            <div className="camera-item__preview">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                <circle cx="12" cy="13" r="4" />
              </svg>
              {camera.status === 'online' && (
                <span className="camera-item__live">LIVE</span>
              )}
            </div>
            <div className="camera-item__info">
              <span className="camera-item__name">{camera.name}</span>
              <span className={`camera-item__status camera-item__status--${camera.status}`}>
                <span className="camera-item__dot" />
                {camera.status === 'online' ? 'Online' : 'Offline'}
              </span>
            </div>
            <span className="camera-item__uptime">{camera.uptime}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}

export default CameraStatus
