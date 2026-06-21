import { COMPLIANCE_DATE_OPTIONS, COMPLIANCE_EVENT_TYPE_OPTIONS } from '../../data/complianceCenter'

function ComplianceFilters({
  filters,
  cameras,
  zones,
  realtimeEnabled,
  onChange,
  onRealtimeToggle,
}) {
  return (
    <section className="compliance-filters panel">
      <div className="panel__header">
        <div>
          <h2 className="panel__title">Bộ lọc</h2>
          <p className="panel__desc">Lọc vi phạm tuân thủ theo loại, camera, vùng và thời gian.</p>
        </div>
        <label className="compliance-filters__realtime">
          <span>Realtime</span>
          <input
            type="checkbox"
            checked={realtimeEnabled}
            onChange={(event) => onRealtimeToggle(event.target.checked)}
          />
          <span className="toggle">
            <span className="toggle__slider" />
          </span>
        </label>
      </div>

      <div className="compliance-filters__grid">
        <label>
          <span>Event Type</span>
          <select
            value={filters.eventType}
            onChange={(event) => onChange({ eventType: event.target.value })}
          >
            {COMPLIANCE_EVENT_TYPE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Camera</span>
          <select
            value={filters.cameraId}
            onChange={(event) => onChange({ cameraId: event.target.value })}
          >
            <option value="all">Tất cả camera</option>
            {cameras.map((camera) => (
              <option key={camera.id} value={camera.id}>{camera.name}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Zone</span>
          <select
            value={filters.zoneId}
            onChange={(event) => onChange({ zoneId: event.target.value })}
          >
            <option value="all">Tất cả vùng</option>
            {zones.map((zone) => (
              <option key={zone.value} value={zone.value}>{zone.label}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Date</span>
          <select
            value={filters.date}
            onChange={(event) => onChange({ date: event.target.value })}
          >
            {COMPLIANCE_DATE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>
      </div>
    </section>
  )
}

export default ComplianceFilters
