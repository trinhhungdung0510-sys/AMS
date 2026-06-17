function MonitoringCameraTile({ camera, onClick }) {
  const hasAlerts = camera.alertsToday > 0

  return (
    <button
      type="button"
      className={`monitoring-tile monitoring-tile--${camera.status}`}
      onClick={onClick}
    >
      <div
        className="monitoring-tile__feed"
        style={{ '--feed-hue': camera.feedHue }}
      >
        <div className="monitoring-tile__scanline" />
        <div className="monitoring-tile__noise" />

        {camera.status === 'online' ? (
          <>
            <span className="monitoring-tile__rec">
              <span className="monitoring-tile__rec-dot" />
              REC
            </span>
            <span className="monitoring-tile__timestamp">
              {new Date().toLocaleTimeString('vi-VN')}
            </span>
          </>
        ) : (
          <span className="monitoring-tile__no-signal">NO SIGNAL</span>
        )}

        {hasAlerts && (
          <span className="monitoring-tile__alert-badge">
            {camera.alertsToday} cảnh báo
          </span>
        )}

        <div className="monitoring-tile__hover">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" />
          </svg>
          Xem chi tiết
        </div>
      </div>

      <div className="monitoring-tile__footer">
        <div className="monitoring-tile__info">
          <span className="monitoring-tile__name">{camera.name}</span>
          <span className="monitoring-tile__zone">{camera.zone}</span>
        </div>
        <div className="monitoring-tile__meta">
          <span className={`status-pill status-pill--${camera.status}`}>
            {camera.status === 'online' ? 'Online' : 'Offline'}
          </span>
          <span className={`monitoring-tile__alerts${hasAlerts ? ' monitoring-tile__alerts--active' : ''}`}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
            </svg>
            {camera.alertsToday} hôm nay
          </span>
        </div>
      </div>
    </button>
  )
}

export default MonitoringCameraTile
