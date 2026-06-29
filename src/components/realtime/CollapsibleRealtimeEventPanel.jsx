import { useEffect, useRef, useState } from 'react'
import { ChevronDown } from 'lucide-react'
import { useEventStore } from '../../context/EventStore'
import { useDashboardBootstrap } from '../../context/DashboardBootstrapStore'
import { useViolationProcessing } from '../../context/ViolationProcessingContext'
import { severityLabels } from '../../data/mockData'

const SCROLL_NEAR_TOP_THRESHOLD = 24
const PANEL_BODY_HEIGHT = 400

function formatEventTime(event) {
  const value = event.occurredAt || `${event.date}T${event.time || '00:00'}`
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return value || '--'
  return parsed.toLocaleString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    day: '2-digit',
    month: '2-digit',
  })
}

function CollapsibleRealtimeEventPanel({
  defaultExpanded = false,
  variant = 'default',
  filterCameraId = null,
  limit = 50,
}) {
  const { connected, loading, error } = useEventStore()
  const { retry } = useDashboardBootstrap()
  const { openViolation, openFeedEvents, openMetrics } = useViolationProcessing()
  const [expanded, setExpanded] = useState(defaultExpanded)
  const scrollRef = useRef(null)
  const pinnedToTopRef = useRef(true)
  const prevScrollHeightRef = useRef(0)

  const openToday = openMetrics?.openToday ?? 0
  const feed = Array.isArray(openFeedEvents) ? openFeedEvents : []
  const items = (filterCameraId
    ? feed.filter((item) => item?.cameraId === filterCameraId)
    : feed
  ).slice(0, limit)

  const handleScroll = () => {
    const element = scrollRef.current
    if (!element) return
    pinnedToTopRef.current = element.scrollTop <= SCROLL_NEAR_TOP_THRESHOLD
  }

  useEffect(() => {
    const element = scrollRef.current
    if (!element || !expanded) return

    const previousHeight = prevScrollHeightRef.current
    const nextHeight = element.scrollHeight

    if (pinnedToTopRef.current) {
      element.scrollTop = 0
    } else if (previousHeight > 0 && nextHeight > previousHeight) {
      element.scrollTop += nextHeight - previousHeight
    }

    prevScrollHeightRef.current = nextHeight
  }, [items, expanded])

  const PanelTag = variant === 'sidebar' ? 'aside' : 'section'

  return (
    <PanelTag
      className={`realtime-panel panel realtime-panel--${variant}${expanded ? ' realtime-panel--expanded' : ' realtime-panel--collapsed'}`}
    >
      <header className="realtime-panel__header">
        <div className="realtime-panel__title-group">
          <h2 className="realtime-panel__title">Vi phạm trực tiếp</h2>
          <p className="realtime-panel__status">
            <span className={`realtime-panel__live-dot${connected ? ' realtime-panel__live-dot--online' : ''}`} />
            {connected ? 'Đang theo dõi' : 'Đang kết nối lại…'}
          </p>
          {!expanded ? (
            <p className="realtime-panel__summary">({openToday} vi phạm chưa xử lý hôm nay)</p>
          ) : null}
        </div>

        <div className="realtime-panel__actions">
          <span className="realtime-panel__count">{openToday} chưa xử lý</span>
          <button
            type="button"
            className="realtime-panel__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            <ChevronDown size={16} className="realtime-panel__toggle-icon" />
            {expanded ? 'Thu gọn' : 'Mở'}
          </button>
        </div>
      </header>

      <div className={`realtime-panel__body${expanded ? ' realtime-panel__body--expanded' : ''}`}>
        <div className="realtime-panel__body-inner">
          {error ? (
            <div className="realtime-feed__error">
              <p>{error}</p>
              <button type="button" className="btn btn--outline btn--sm" onClick={retry}>
                Tải lại
              </button>
            </div>
          ) : null}

          {loading && items.length === 0 ? (
            <p className="realtime-feed__empty">Đang tải sự kiện…</p>
          ) : null}

          {!loading && !error && items.length === 0 ? (
            <p className="realtime-feed__empty">Chưa có dữ liệu.</p>
          ) : null}

          {items.length > 0 ? (
            <ul
              ref={scrollRef}
              className="realtime-panel__list"
              style={{ maxHeight: PANEL_BODY_HEIGHT }}
              onScroll={handleScroll}
            >
              {items.map((event) => (
                <li key={event.id} className="realtime-panel__item">
                  <button
                    type="button"
                    className="realtime-panel__item-link"
                    onClick={() => openViolation(event)}
                  >
                    <span className={`badge badge--${event.severity}`}>
                      {severityLabels[event.severity] || event.severityRaw || 'Cảnh báo'}
                    </span>
                    <span className="realtime-panel__item-time">{formatEventTime(event)}</span>
                    <span className="realtime-panel__item-camera">{event.cameraName || event.cameraId || '--'}</span>
                    <span className="realtime-panel__item-zone">{event.zoneName || event.zoneId || '--'}</span>
                    <strong className="realtime-panel__item-label">{event.typeLabel || event.eventType}</strong>
                  </button>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      </div>
    </PanelTag>
  )
}

export default CollapsibleRealtimeEventPanel
