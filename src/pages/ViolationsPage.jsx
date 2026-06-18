import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  Download,
  FileText,
  Filter,
  ShieldAlert,
  Siren,
} from 'lucide-react'
import AtshViolationSnapshot from '../components/AtshViolationSnapshot'
import EventsListPanel from '../components/EventsListPanel'
import {
  ATSH_SEVERITY,
  ATSH_STATUS,
  ATSH_VIOLATION_TYPES,
  TODAY,
  VI_PHAM_ATSH_ROUTE,
  atshViolations,
  cameraOptions,
  computeAtshKpis,
  dateFilterOptions,
  mapApiEventToViolation,
  severityFilterOptions,
  zoneOptions,
} from '../data/atshViolations'
import { exportRowsAsExcel, formatDateTime } from '../utils/formatters'

const API_BASE_URL = 'http://127.0.0.1:8000'

function ViolationsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const activeTab = searchParams.get('tab') === 'su-kien' ? 'su-kien' : 'vi-pham'

  const [items, setItems] = useState(atshViolations)
  const [dateFilter, setDateFilter] = useState('today')
  const [cameraFilter, setCameraFilter] = useState('all')
  const [zoneFilter, setZoneFilter] = useState('all')
  const [severityFilter, setSeverityFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')

  useEffect(() => {
    const loadEvents = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/events`)
        if (!response.ok) return
        const data = await response.json()
        if (!data.length) return
        const mapped = data.map(mapApiEventToViolation)
        setItems((prev) => {
          const ids = new Set(mapped.map((item) => item.id))
          const rest = prev.filter((item) => !ids.has(item.id))
          return [...mapped, ...rest]
        })
      } catch {
        // keep mock data
      }
    }
    loadEvents()
  }, [])

  const filtered = useMemo(() => items.filter((item) => {
    const matchDate =
      dateFilter === 'all' ||
      (dateFilter === 'today' && item.date === TODAY) ||
      (dateFilter === 'week' && Number(item.date.slice(-2)) >= 12) ||
      (dateFilter === 'month' && item.date.startsWith('2026-06'))

    const matchCamera = cameraFilter === 'all' || item.cameraId === cameraFilter
    const matchZone = zoneFilter === 'all' || item.zone === zoneFilter
    const matchSeverity = severityFilter === 'all' || item.severity === severityFilter
    const matchType = typeFilter === 'all' || item.type === typeFilter

    return matchDate && matchCamera && matchZone && matchSeverity && matchType
  }), [items, dateFilter, cameraFilter, zoneFilter, severityFilter, typeFilter])

  const kpis = useMemo(() => computeAtshKpis(items), [items])

  const exportExcel = () => {
    exportRowsAsExcel(
      'ams-vi-pham-atsh.xls',
      filtered.map((item) => ({
        'Thời gian': formatDateTime(item.date, item.time),
        Camera: item.cameraName,
        'Khu vực': item.zone,
        'Loại vi phạm': item.typeLabel,
        'Độ tin cậy': `${item.confidence}%`,
        'Mức độ': ATSH_SEVERITY[item.severity]?.label || item.severity,
        'Trạng thái': ATSH_STATUS[item.status],
      })),
    )
  }

  const exportPdf = () => window.print()

  return (
    <div className="atsh-soc">
      <header className="atsh-soc__hero">
        <div>
          <span className="atsh-soc__eyebrow">Trung tâm điều hành ATSH</span>
          <h1>Trung tâm vi phạm ATSH</h1>
          <p>Giám sát, phân loại và xử lý vi phạm an toàn sinh học theo thời gian thực.</p>
        </div>
        {activeTab === 'vi-pham' && (
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
          className={`atsh-soc__tab${activeTab === 'vi-pham' ? ' atsh-soc__tab--active' : ''}`}
          onClick={() => setSearchParams({})}
        >
          <ShieldAlert size={16} /> Vi phạm ATSH
        </button>
        <button
          type="button"
          className={`atsh-soc__tab${activeTab === 'su-kien' ? ' atsh-soc__tab--active' : ''}`}
          onClick={() => setSearchParams({ tab: 'su-kien' })}
        >
          <Siren size={16} /> Sự kiện
        </button>
      </nav>

      {activeTab === 'su-kien' ? (
        <EventsListPanel />
      ) : (
        <>
      <section className="atsh-soc__kpis">
        {[
          { label: 'Tổng vi phạm hôm nay', value: kpis.totalToday, icon: ShieldAlert, tone: 'green' },
          { label: 'Vi phạm nghiêm trọng', value: kpis.critical, icon: AlertTriangle, tone: 'red' },
          { label: 'Vi phạm đang xử lý', value: kpis.processing, icon: Clock3, tone: 'orange' },
          { label: 'Vi phạm đã xử lý', value: kpis.resolved, icon: CheckCircle2, tone: 'blue' },
        ].map((item) => {
          const Icon = item.icon
          return (
            <article key={item.label} className={`atsh-kpi atsh-kpi--${item.tone}`}>
              <div>
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>
              <div className="atsh-kpi__icon">
                <Icon size={22} />
              </div>
            </article>
          )
        })}
      </section>

      <section className="atsh-soc__filters panel">
        <div className="atsh-soc__filters-head">
          <Filter size={16} />
          <strong>Bộ lọc</strong>
          <span>{filtered.length} vi phạm</span>
        </div>
        <div className="atsh-soc__filters-grid">
          <label>
            <span>Ngày</span>
            <select value={dateFilter} onChange={(e) => setDateFilter(e.target.value)}>
              {dateFilterOptions.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>
          <label>
            <span>Camera</span>
            <select value={cameraFilter} onChange={(e) => setCameraFilter(e.target.value)}>
              <option value="all">Tất cả camera</option>
              {cameraOptions.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>
          <label>
            <span>Khu vực</span>
            <select value={zoneFilter} onChange={(e) => setZoneFilter(e.target.value)}>
              <option value="all">Tất cả khu vực</option>
              {zoneOptions.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>
          <label>
            <span>Mức độ</span>
            <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
              {severityFilterOptions.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </label>
          <label className="atsh-soc__filter-wide">
            <span>Loại vi phạm</span>
            <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
              <option value="all">Tất cả loại vi phạm</option>
              {ATSH_VIOLATION_TYPES.map((item) => (
                <option key={item.code} value={item.code}>{item.label}</option>
              ))}
            </select>
          </label>
        </div>
      </section>

      <section className="atsh-soc__types panel">
        <h2>Loại vi phạm</h2>
        <div className="atsh-type-chips">
          {ATSH_VIOLATION_TYPES.map((item) => (
            <button
              key={item.code}
              type="button"
              className={`atsh-type-chip${typeFilter === item.code ? ' atsh-type-chip--active' : ''}`}
              onClick={() => setTypeFilter(typeFilter === item.code ? 'all' : item.code)}
            >
              <span className={`atsh-type-chip__dot atsh-type-chip__dot--${item.severity.toLowerCase()}`} />
              {item.label}
            </button>
          ))}
        </div>
      </section>

      {filtered.length === 0 ? (
        <div className="atsh-soc__empty panel">
          <CheckCircle2 size={32} />
          <p>Không có vi phạm phù hợp bộ lọc.</p>
        </div>
      ) : (
        <section className="atsh-soc__grid">
          {filtered.map((item) => {
            const severity = ATSH_SEVERITY[item.severity] || ATSH_SEVERITY.WARNING
            return (
              <Link key={item.id} to={`${VI_PHAM_ATSH_ROUTE}/${item.id}`} className="atsh-card">
                <AtshViolationSnapshot violation={item} />
                <div className="atsh-card__body">
                  <div className="atsh-card__head">
                    <span className={`atsh-severity atsh-severity--${severity.tone}`}>{severity.label}</span>
                    <span className="atsh-card__time">{formatDateTime(item.date, item.time)}</span>
                  </div>
                  <h3>{item.typeLabel}</h3>
                  <p>{item.cameraName}</p>
                  <p>{item.zone}</p>
                  <div className="atsh-card__meta">
                    <span>Độ tin cậy {item.confidence}%</span>
                    <span className={`atsh-status atsh-status--${item.status}`}>{ATSH_STATUS[item.status]}</span>
                  </div>
                </div>
              </Link>
            )
          })}
        </section>
      )}
        </>
      )}
    </div>
  )
}

export default ViolationsPage
