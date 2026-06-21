import { Wifi, WifiOff, AlertTriangle } from 'lucide-react'

function CameraHealthWidget({ summary, loading }) {
  const cards = [
    { label: 'Online', value: summary?.online ?? 0, icon: Wifi, tone: 'green' },
    { label: 'Offline', value: summary?.offline ?? 0, icon: WifiOff, tone: 'red' },
    { label: 'Warning', value: summary?.warning ?? 0, icon: AlertTriangle, tone: 'amber' },
  ]

  return (
    <article className="panel panel--compact">
      <div className="panel__header">
        <div>
          <h2>Sức khỏe camera</h2>
          <p>Trạng thái thiết bị giám sát</p>
        </div>
        <span className="panel__badge">
          {loading ? '…' : `${summary?.total ?? 0} camera`}
        </span>
      </div>
      <div className="camera-health-grid">
        {cards.map((card) => (
          <div key={card.label} className={`camera-health-item camera-health-item--${card.tone}`}>
            <card.icon size={18} />
            <div>
              <strong>{loading ? '…' : card.value}</strong>
              <span>{card.label}</span>
            </div>
          </div>
        ))}
      </div>
    </article>
  )
}

export default CameraHealthWidget
