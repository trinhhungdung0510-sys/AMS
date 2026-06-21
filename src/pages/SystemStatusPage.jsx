import { useEffect, useState } from 'react'
import { fetchSystemStatus } from '../services/deploymentService'

function SystemStatusPage() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true)
        setStatus(await fetchSystemStatus())
      } catch {
        setStatus(null)
      } finally {
        setLoading(false)
      }
    }
    load()
    const timer = setInterval(load, 15000)
    return () => clearInterval(timer)
  }, [])

  const cards = [
    { label: 'Camera Online', value: status?.cameraOnline ?? '—' },
    { label: 'Camera Offline', value: status?.cameraOffline ?? '—' },
    { label: 'RTSP / FFmpeg', value: status?.rtspStatus?.ffmpeg ?? '—' },
    { label: 'Storage Free (GB)', value: status?.storage?.freeGb ?? '—' },
    { label: 'CPU Cores', value: status?.cpu?.cores ?? '—' },
    { label: 'RAM Used (%)', value: status?.ram?.percentUsed ?? '—' },
    { label: 'GPU', value: status?.gpu?.status ?? '—' },
    { label: 'WebSocket Clients', value: status?.websocket?.connectedClients ?? '—' },
  ]

  return (
    <div className="deployment-page">
      <header className="deployment-page__head">
        <h1>System Status</h1>
        <p>Trạng thái vận hành realtime — AMS v2.0</p>
      </header>
      <div className="compliance-kpi-grid">
        {cards.map((card) => (
          <article key={card.label} className="metric-card metric-card--green">
            <div>
              <span className="metric-card__label">{card.label}</span>
              <strong>{loading ? '…' : card.value}</strong>
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}

export default SystemStatusPage
