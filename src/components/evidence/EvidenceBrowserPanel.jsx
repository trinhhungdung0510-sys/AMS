import { useEffect, useState } from 'react'
import { browseEvidence } from '../../services/deploymentService'
import { COMPLIANCE_EVENT_TYPE_OPTIONS } from '../../data/complianceCenter'
import { getFarms } from '../../services/farmService'
import { getCameras } from '../../services/cameraService'
import { resolveSnapshotUrl } from '../../utils/complianceEventNormalizer'

const zoneLabels = {
  parking_zone: 'Bãi đỗ xe',
  gestation_barn: 'Chuồng nái bầu',
  person_disinfection_zone: 'Khu sát trùng người',
  vehicle_disinfection_zone: 'Khu sát trùng xe',
  reception_zone: 'Khu tiếp khách',
  farrowing_barn: 'Chuồng nái đẻ',
  pig_loading_zone: 'Khu xuất nhập heo',
  worker_housing: 'Nhà ở công nhân',
  shower_room: 'Nhà tắm',
  handwash_zone: 'Khu rửa tay',
  boot_disinfection_tray: 'Khay sát trùng ủng',
}

function formatZone(zone) {
  if (!zone) return '--'
  return zoneLabels[zone] || zone
}

function formatTime(value) {
  if (!value) return '--'
  return new Date(value).toLocaleString('vi-VN')
}

function EvidenceBrowserPanel({ compact = false }) {
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
      limit: compact ? 24 : 40,
    })
      .then((data) => {
        setItems(data.items || [])
        setTotal(data.total || 0)
      })
      .catch(() => {
        setItems([])
        setTotal(0)
      })
  }, [filters, compact])

  return (
    <div className={`evidence-browser${compact ? ' evidence-browser--compact' : ''}`}>
      {!compact ? (
        <header className="evidence-browser__head">
          <h2>Duyệt bằng chứng</h2>
          <p>Lọc theo trang trại, camera, ngày và quy tắc vi phạm</p>
        </header>
      ) : null}

      <section className="compliance-filters panel">
        <div className="compliance-filters__grid">
          <label>
            Trang trại
            <select value={filters.farmId} onChange={(e) => setFilters({ ...filters, farmId: e.target.value })}>
              <option value="">Tất cả</option>
              {farms.map((farm) => (
                <option key={farm.id} value={farm.id}>{farm.name}</option>
              ))}
            </select>
          </label>
          <label>
            Camera
            <select value={filters.cameraId} onChange={(e) => setFilters({ ...filters, cameraId: e.target.value })}>
              <option value="">Tất cả</option>
              {cameras.map((camera) => (
                <option key={camera.id} value={camera.id}>{camera.name}</option>
              ))}
            </select>
          </label>
          <label>
            Ngày
            <input type="date" value={filters.date} onChange={(e) => setFilters({ ...filters, date: e.target.value })} />
          </label>
          <label>
            Quy tắc vi phạm
            <select value={filters.ruleType} onChange={(e) => setFilters({ ...filters, ruleType: e.target.value })}>
              <option value="">Tất cả</option>
              {COMPLIANCE_EVENT_TYPE_OPTIONS.filter((item) => item.value !== 'all').map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>
        </div>
        <p className="panel__meta">{total} bằng chứng</p>
      </section>

      {items.length === 0 ? (
        <div className="evidence-browser__empty panel">
          <p>Chưa có dữ liệu</p>
        </div>
      ) : (
        <div className="evidence-browser-grid">
          {items.map((item) => {
            const snapshotUrl = resolveSnapshotUrl(item.snapshotUrl)
            const videoUrl = resolveSnapshotUrl(item.videoUrl)
            return (
              <article key={item.id} className="compliance-card evidence-card">
                {snapshotUrl ? (
                  <img src={snapshotUrl} alt="" className="compliance-card__thumb" />
                ) : (
                  <div className="compliance-card__thumb compliance-card__thumb--empty">Chưa có ảnh</div>
                )}
                <div className="compliance-card__body">
                  <h3>{item.ruleName || item.ruleType || 'Quy tắc vi phạm'}</h3>
                  <dl className="evidence-card__meta">
                    <div>
                      <dt>Snapshot</dt>
                      <dd>{snapshotUrl ? 'Có' : 'Không có'}</dd>
                    </div>
                    {videoUrl ? (
                      <div>
                        <dt>Video</dt>
                        <dd>
                          <a href={videoUrl} target="_blank" rel="noreferrer">Xem video</a>
                        </dd>
                      </div>
                    ) : null}
                    <div>
                      <dt>Camera</dt>
                      <dd>{item.cameraName || item.cameraId || '--'}</dd>
                    </div>
                    <div>
                      <dt>Khu vực</dt>
                      <dd>{formatZone(item.zone)}</dd>
                    </div>
                    <div>
                      <dt>Thời gian</dt>
                      <dd>{formatTime(item.occurredAt)}</dd>
                    </div>
                    <div>
                      <dt>Quy tắc vi phạm</dt>
                      <dd>{item.ruleName || item.ruleType || '--'}</dd>
                    </div>
                  </dl>
                </div>
              </article>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default EvidenceBrowserPanel
