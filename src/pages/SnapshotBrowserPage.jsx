import { useEffect, useState } from 'react'
import { browseEvidence } from '../services/deploymentService'
import { COMPLIANCE_EVENT_TYPE_OPTIONS } from '../data/complianceCenter'
import { getFarms } from '../services/farmService'
import { getCameras } from '../services/cameraService'
import { resolveSnapshotUrl } from '../utils/complianceEventNormalizer'

function SnapshotBrowserPage() {
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [farms, setFarms] = useState([])
  const [cameras, setCameras] = useState([])
  const [filters, setFilters] = useState({ farmId: '', cameraId: '', date: '', ruleType: '' })

  useEffect(() => {
    Promise.all([getFarms().catch(() => []), getCameras().catch(() => [])]).then(([farmData, cameraData]) => {
      setFarms(farmData)
      setCameras(cameraData)
    })
  }, [])

  useEffect(() => {
    browseEvidence({
      farmId: filters.farmId || undefined,
      cameraId: filters.cameraId || undefined,
      date: filters.date || undefined,
      ruleType: filters.ruleType || undefined,
      limit: 40,
    })
      .then((data) => {
        setItems(data.items || [])
        setTotal(data.total || 0)
      })
      .catch(() => {
        setItems([])
        setTotal(0)
      })
  }, [filters])

  return (
    <div className="deployment-page">
      <header className="deployment-page__head">
        <h1>Snapshot Browser</h1>
        <p>Duyệt evidence theo farm, camera, ngày, rule</p>
      </header>

      <section className="compliance-filters panel">
        <div className="compliance-filters__grid">
          <label>
            Farm
            <select value={filters.farmId} onChange={(e) => setFilters({ ...filters, farmId: e.target.value })}>
              <option value="">Tất cả</option>
              {farms.map((farm) => <option key={farm.id} value={farm.id}>{farm.name}</option>)}
            </select>
          </label>
          <label>
            Camera
            <select value={filters.cameraId} onChange={(e) => setFilters({ ...filters, cameraId: e.target.value })}>
              <option value="">Tất cả</option>
              {cameras.map((camera) => <option key={camera.id} value={camera.id}>{camera.name}</option>)}
            </select>
          </label>
          <label>
            Ngày
            <input type="date" value={filters.date} onChange={(e) => setFilters({ ...filters, date: e.target.value })} />
          </label>
          <label>
            Rule
            <select value={filters.ruleType} onChange={(e) => setFilters({ ...filters, ruleType: e.target.value })}>
              <option value="">Tất cả</option>
              {COMPLIANCE_EVENT_TYPE_OPTIONS.filter((item) => item.value !== 'all').map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>
        </div>
        <p className="panel__meta">{total} evidence</p>
      </section>

      <div className="evidence-browser-grid">
        {items.map((item) => {
          const url = resolveSnapshotUrl(item.snapshotUrl)
          return (
            <article key={item.id} className="compliance-card">
              {url ? <img src={url} alt="" className="compliance-card__thumb" /> : <div className="compliance-card__thumb compliance-card__thumb--empty">No snapshot</div>}
              <div className="compliance-card__body">
                <h3>{item.ruleName || item.ruleType}</h3>
                <p>{item.cameraName} · {item.occurredAt}</p>
              </div>
            </article>
          )
        })}
      </div>
    </div>
  )
}

export default SnapshotBrowserPage
