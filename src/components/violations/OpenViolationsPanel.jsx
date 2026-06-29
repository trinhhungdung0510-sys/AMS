import { Inbox } from 'lucide-react'
import CollapsibleRealtimeEventPanel from '../realtime/CollapsibleRealtimeEventPanel'
import AtshViolationSnapshot from '../AtshViolationSnapshot'
import { ATSH_SEVERITY, ATSH_STATUS, ATSH_VIOLATION_TYPES } from '../../data/atshViolations'
import { formatDateTime } from '../../utils/formatters'
import { mapSourceStatusKey } from '../../utils/violationStatus'

function OpenViolationsPanel({ items = [], onOpenViolation, getOverride }) {
  const safeItems = Array.isArray(items) ? items : []

  return (
    <>
      <CollapsibleRealtimeEventPanel defaultExpanded variant="page" />

      {safeItems.length > 0 ? (
        <section className="atsh-soc__grid">
          {safeItems.map((item) => {
            if (!item?.id) return null

            const severity = ATSH_SEVERITY[item.severity] || ATSH_SEVERITY.WARNING
            const statusKey = mapSourceStatusKey(item, getOverride?.(item.id))

            return (
              <button
                key={item.id}
                type="button"
                className="atsh-card atsh-card--button"
                onClick={() => onOpenViolation?.(item)}
              >
                <AtshViolationSnapshot violation={item} />
                <div className="atsh-card__body">
                  <div className="atsh-card__head">
                    <span className={`atsh-severity atsh-severity--${severity.tone}`}>{severity.label}</span>
                    <span className="atsh-card__time">{formatDateTime(item.date, item.time)}</span>
                  </div>
                  <h3>{item.typeLabel || 'Vi phạm ATSH'}</h3>
                  <p>{item.cameraName || 'Chưa có dữ liệu'}</p>
                  <p>{item.zone || item.zoneName || 'Chưa có dữ liệu'}</p>
                  <div className="atsh-card__meta">
                    <span>Độ tin cậy {item.confidence ?? 0}%</span>
                    <span className={`atsh-status atsh-status--${statusKey}`}>
                      {ATSH_STATUS[statusKey] || 'Chưa xử lý'}
                    </span>
                  </div>
                </div>
              </button>
            )
          })}
        </section>
      ) : (
        <div className="atsh-soc__empty panel">
          <Inbox size={32} />
          <p>Chưa có dữ liệu.</p>
        </div>
      )}

      <section className="atsh-soc__types panel">
        <h2>Loại vi phạm thường gặp</h2>
        <div className="atsh-type-chips">
          {ATSH_VIOLATION_TYPES.slice(0, 6).map((item) => (
            <span key={item.code} className="atsh-type-chip">
              <span className={`atsh-type-chip__dot atsh-type-chip__dot--${item.severity.toLowerCase()}`} />
              {item.label}
            </span>
          ))}
        </div>
      </section>
    </>
  )
}

export default OpenViolationsPanel
