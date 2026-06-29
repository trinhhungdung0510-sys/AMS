import { useMemo, useState } from 'react'
import { CheckCircle2, Filter, Inbox, Search } from 'lucide-react'
import AtshViolationSnapshot from '../AtshViolationSnapshot'
import { useViolationProcessing } from '../../context/ViolationProcessingContext'
import { ATSH_SEVERITY, ATSH_STATUS, TODAY } from '../../data/atshViolations'
import { formatDateTime } from '../../utils/formatters'
import { mapSourceStatusKey } from '../../utils/violationStatus'

function formatProcessedTime(item) {
  if (item?.resolvedAt) {
    const parsed = new Date(item.resolvedAt)
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toLocaleString('vi-VN')
    }
  }

  if (item?.occurredAt) {
    const parsed = new Date(item.occurredAt)
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toLocaleString('vi-VN')
    }
  }

  return formatDateTime(item?.date, item?.time)
}

function ProcessedViolationsPanel({ mockItems = [] }) {
  const { resolvedRecords, openViolation, getOverride } = useViolationProcessing()
  const [search, setSearch] = useState('')
  const [dateFilter, setDateFilter] = useState('all')

  const safeMockItems = Array.isArray(mockItems) ? mockItems : []
  const safeResolvedRecords = Array.isArray(resolvedRecords) ? resolvedRecords : []

  const processedMock = useMemo(
    () => safeMockItems.filter((item) => {
      if (!item?.id) return false
      const statusKey = mapSourceStatusKey(item, getOverride?.(item.id))
      return statusKey === 'resolved' || statusKey === 'dismissed'
    }),
    [safeMockItems, getOverride],
  )

  const allProcessed = useMemo(() => {
    const map = new Map()
    ;[...processedMock, ...safeResolvedRecords].forEach((item) => {
      if (item?.id) map.set(item.id, item)
    })
    return [...map.values()].sort((left, right) =>
      String(right?.resolvedAt || right?.occurredAt || right?.date || '').localeCompare(
        String(left?.resolvedAt || left?.occurredAt || left?.date || ''),
      ),
    )
  }, [processedMock, safeResolvedRecords])

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase()
    return allProcessed.filter((item) => {
      const matchSearch =
        query === '' ||
        String(item?.typeLabel || '').toLowerCase().includes(query) ||
        String(item?.cameraName || '').toLowerCase().includes(query) ||
        String(item?.zoneName || item?.zone || '').toLowerCase().includes(query) ||
        String(item?.handler || '').toLowerCase().includes(query) ||
        String(item?.note || '').toLowerCase().includes(query)

      const dateValue = item?.date || String(item?.occurredAt || item?.resolvedAt || '').slice(0, 10)
      const matchDate =
        dateFilter === 'all' ||
        (dateFilter === 'today' && dateValue === TODAY) ||
        (dateFilter === 'week' && dateValue) ||
        (dateFilter === 'month' && String(dateValue).startsWith(TODAY.slice(0, 7)))

      return matchSearch && matchDate
    })
  }, [allProcessed, search, dateFilter])

  return (
    <div className="violation-processed">
      <section className="atsh-soc__filters panel">
        <div className="atsh-soc__filters-head">
          <Filter size={16} />
          <strong>Bộ lọc lịch sử</strong>
          <span>{filtered.length} vi phạm đã xử lý</span>
        </div>
        <div className="atsh-soc__filters-grid">
          <label className="atsh-soc__filter-wide">
            <span>Tìm kiếm</span>
            <div className="search-box">
              <Search size={16} />
              <input
                type="search"
                className="search-box__input"
                placeholder="Camera, khu vực, người xử lý, ghi chú..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>
          </label>
          <label>
            <span>Thời gian</span>
            <select value={dateFilter} onChange={(event) => setDateFilter(event.target.value)}>
              <option value="all">Tất cả</option>
              <option value="today">Hôm nay</option>
              <option value="week">7 ngày</option>
              <option value="month">30 ngày</option>
            </select>
          </label>
        </div>
      </section>

      {allProcessed.length === 0 ? (
        <div className="atsh-soc__empty panel">
          <Inbox size={32} />
          <p>Chưa có dữ liệu.</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="atsh-soc__empty panel">
          <CheckCircle2 size={32} />
          <p>Chưa có vi phạm đã xử lý phù hợp bộ lọc.</p>
        </div>
      ) : (
        <section className="atsh-soc__grid">
          {filtered.map((item) => {
            const severityKey = item?.severity === 'CRITICAL'
              ? 'CRITICAL'
              : item?.severity === 'WARNING'
                ? 'WARNING'
                : 'INFO'
            const severity = ATSH_SEVERITY[severityKey] || ATSH_SEVERITY.WARNING
            const resolvedTime = formatProcessedTime(item)

            return (
              <button
                key={item.id}
                type="button"
                className="atsh-card atsh-card--button"
                onClick={() => openViolation?.(item.raw || item)}
              >
                <AtshViolationSnapshot
                  violation={{
                    severity: severityKey,
                    confidence: item?.confidence ?? 0,
                    snapshotTone: severity.tone,
                  }}
                />
                <div className="atsh-card__body">
                  <div className="atsh-card__head">
                    <span className={`atsh-severity atsh-severity--${severity.tone}`}>{severity.label}</span>
                    <span className="atsh-card__time">{resolvedTime}</span>
                  </div>
                  <h3>{item?.typeLabel || 'Vi phạm ATSH'}</h3>
                  <p>{item?.cameraName || 'Chưa có dữ liệu'}</p>
                  <p>{item?.zoneName || item?.zone || 'Chưa có dữ liệu'}</p>
                  <div className="atsh-card__meta">
                    <span>Người xử lý: {item?.handler || 'Chưa có dữ liệu'}</span>
                    <span className="atsh-status atsh-status--resolved">{ATSH_STATUS.resolved}</span>
                  </div>
                  {item?.note ? <p className="violation-processed__note">{item.note}</p> : null}
                </div>
              </button>
            )
          })}
        </section>
      )}
    </div>
  )
}

export default ProcessedViolationsPanel
