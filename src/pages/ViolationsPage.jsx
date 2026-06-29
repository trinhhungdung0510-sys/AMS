import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  Download,
  FileText,
  ShieldAlert,
} from 'lucide-react'
import ErrorBoundary from '../components/common/ErrorBoundary'
import OpenViolationsPanel from '../components/violations/OpenViolationsPanel'
import ProcessedViolationsPanel from '../components/violations/ProcessedViolationsPanel'
import { useViolationProcessing } from '../context/ViolationProcessingContext'
import {
  ATSH_SEVERITY,
  ATSH_STATUS,
  TODAY,
  atshViolations,
  mapApiEventToViolation,
} from '../data/atshViolations'
import { exportRowsAsExcel, formatDateTime } from '../utils/formatters'
import { getEvents } from '../services/eventService'
import { mapSourceStatusKey } from '../utils/violationStatus'

function ViolationsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const {
    openViolation,
    isViolationOpen,
    getOverride,
    openMetrics,
    resolvedRecords,
  } = useViolationProcessing()

  const activeTab = searchParams.get('tab') === 'da-xu-ly' ? 'da-xu-ly' : 'chua-xu-ly'
  const [items, setItems] = useState(atshViolations)
  const [loadError, setLoadError] = useState(null)

  useEffect(() => {
    const loadEvents = async () => {
      try {
        setLoadError(null)
        const data = await getEvents()
        if (!Array.isArray(data) || data.length === 0) return

        const mapped = data
          .map((event) => {
            try {
              return mapApiEventToViolation(event)
            } catch {
              return null
            }
          })
          .filter(Boolean)

        if (!mapped.length) return

        setItems((prev) => {
          const ids = new Set(mapped.map((item) => item.id))
          const rest = prev.filter((item) => !ids.has(item.id))
          return [...mapped, ...rest]
        })
      } catch {
        setLoadError('Không tải được dữ liệu từ API. Đang hiển thị dữ liệu cục bộ.')
      }
    }

    loadEvents()
  }, [])

  const openMockItems = useMemo(
    () => (Array.isArray(items) ? items : []).filter((item) => isViolationOpen(item)),
    [items, isViolationOpen],
  )

  const metrics = openMetrics || {}

  const kpis = useMemo(() => {
    const todayOpen =
      openMockItems.filter((item) => item?.date === TODAY).length + (metrics.openToday ?? 0)

    return {
      totalToday: todayOpen,
      critical:
        openMockItems.filter((item) => item?.severity === 'CRITICAL').length + (metrics.openCritical ?? 0),
      processing: openMockItems.filter(
        (item) => mapSourceStatusKey(item, getOverride?.(item?.id)) === 'confirmed',
      ).length,
      resolved:
        (Array.isArray(resolvedRecords) ? resolvedRecords.length : 0)
        + (Array.isArray(items) ? items.filter((item) => item?.status === 'resolved').length : 0),
    }
  }, [openMockItems, metrics.openToday, metrics.openCritical, resolvedRecords, items, getOverride])

  const exportExcel = () => {
    exportRowsAsExcel(
      'ams-vi-pham-atsh.xls',
      openMockItems.map((item) => ({
        'Thời gian': formatDateTime(item?.date, item?.time),
        Camera: item?.cameraName || 'Chưa có dữ liệu',
        'Khu vực': item?.zone || item?.zoneName || 'Chưa có dữ liệu',
        'Loại vi phạm': item?.typeLabel || 'Vi phạm ATSH',
        'Độ tin cậy': `${item?.confidence ?? 0}%`,
        'Mức độ': ATSH_SEVERITY[item?.severity]?.label || item?.severity || 'Chưa có dữ liệu',
        'Trạng thái': ATSH_STATUS[mapSourceStatusKey(item, getOverride?.(item?.id))] || 'Chưa xử lý',
      })),
    )
  }

  const exportPdf = () => window.print()

  return (
    <div className="atsh-soc">
      <header className="atsh-soc__hero">
        <div>
          <span className="atsh-soc__eyebrow">Trung tâm quản lý vi phạm</span>
          <h1>Vi phạm ATSH</h1>
          <p>Một trung tâm duy nhất — theo dõi realtime, xử lý và tra cứu lịch sử vi phạm an toàn sinh học.</p>
        </div>
        {activeTab === 'chua-xu-ly' && (
          <div className="atsh-soc__hero-actions">
            <button type="button" className="btn btn--outline atsh-soc__btn" onClick={exportExcel}>
              <Download size={16} /> Excel
            </button>
            <button type="button" className="btn btn--primary atsh-soc__btn" onClick={exportPdf}>
              <FileText size={16} /> PDF
            </button>
          </div>
        )}
      </header>

      <nav className="atsh-soc__tabs">
        <button
          type="button"
          className={`atsh-soc__tab${activeTab === 'chua-xu-ly' ? ' atsh-soc__tab--active' : ''}`}
          onClick={() => setSearchParams({})}
        >
          <ShieldAlert size={16} /> Vi phạm chưa xử lý
        </button>
        <button
          type="button"
          className={`atsh-soc__tab${activeTab === 'da-xu-ly' ? ' atsh-soc__tab--active' : ''}`}
          onClick={() => setSearchParams({ tab: 'da-xu-ly' })}
        >
          <CheckCircle2 size={16} /> Vi phạm đã xử lý
        </button>
      </nav>

      {loadError ? (
        <p className="atsh-soc__notice panel" role="status">{loadError}</p>
      ) : null}

      <section className="atsh-soc__kpis">
        {[
          { label: 'Vi phạm chưa xử lý hôm nay', value: kpis.totalToday, icon: ShieldAlert, tone: 'green' },
          { label: 'Vi phạm nghiêm trọng', value: kpis.critical, icon: AlertTriangle, tone: 'red' },
          { label: 'Đang xử lý', value: kpis.processing, icon: Clock3, tone: 'orange' },
          { label: 'Đã xử lý', value: kpis.resolved, icon: CheckCircle2, tone: 'blue' },
        ].map((item) => {
          const Icon = item.icon
          return (
            <article key={item.label} className={`atsh-kpi atsh-kpi--${item.tone}`}>
              <div>
                <span>{item.label}</span>
                <strong>{item.value ?? 0}</strong>
              </div>
              <div className="atsh-kpi__icon">
                <Icon size={22} />
              </div>
            </article>
          )
        })}
      </section>

      <ErrorBoundary
        fallbackTitle={
          activeTab === 'da-xu-ly'
            ? 'Không thể hiển thị tab Vi phạm đã xử lý'
            : 'Không thể hiển thị tab Vi phạm chưa xử lý'
        }
      >
        {activeTab === 'da-xu-ly' ? (
          <ProcessedViolationsPanel mockItems={items} />
        ) : (
          <OpenViolationsPanel
            items={openMockItems}
            onOpenViolation={openViolation}
            getOverride={getOverride}
          />
        )}
      </ErrorBoundary>
    </div>
  )
}

export default ViolationsPage
