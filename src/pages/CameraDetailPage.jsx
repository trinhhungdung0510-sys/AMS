import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ChevronLeft } from 'lucide-react'
import { useRealtimeEvents } from '../hooks/useRealtimeEvents'
import { usePermissions } from '../hooks/usePermissions'
import { useCameraLifecycle } from '../hooks/useCameraLifecycle'
import CameraFeed from '../components/CameraFeed'
import CameraAtshStatusBanner from '../components/camera/CameraAtshStatusBanner'
import CameraLifecycleBadge from '../components/camera/CameraLifecycleBadge'
import ZonePublishNotice from '../components/camera/ZonePublishNotice'
import ViolationCard from '../components/ViolationCard'
import {
  alertTypeOptions,
  getCameraById as getMockCameraById,
  getEventsByCamera,
  getViolationImagesByCamera,
  severityLabels,
  statusLabels,
} from '../data/mockData'
import { mapApiEventToViolation, TODAY } from '../data/atshViolations'
import { getCameraById, getCameraIp } from '../services/cameraService'
import {
  captureCameraSnapshot,
  getLatestCameraSnapshot,
  resolveSnapshotAssetUrl,
} from '../services/cameraSnapshotService'
import CameraSnapshotCard from '../components/camera/CameraSnapshotCard'
import DetectionOverlay from '../components/camera/DetectionOverlay'
import ZoneLiveOverlay from '../components/camera/ZoneLiveOverlay'
import ZoneEditor from '../components/zones/ZoneEditor'
import RuleEditor from '../components/rules/RuleEditor'
import ObservationViewer from '../components/observations/ObservationViewer'
import EventTimeline from '../components/events/EventTimeline'
import { CAMERA_DETAIL_TABS } from '../config/cameraZones'
import { getEvents, getCameraEventTimeline } from '../services/eventService'
import { listAuditLogs } from '../services/systemSettingsService'
import { formatDateTime, downloadTextFile } from '../utils/formatters'
import AtshViolationSnapshot from '../components/AtshViolationSnapshot'

const timeFilters = [
  { value: 'all', label: 'Tất cả' },
  { value: 'today', label: 'Hôm nay' },
  { value: 'week', label: '7 ngày' },
  { value: 'month', label: '30 ngày' },
]

const API_SEVERITY_TO_BADGE = {
  CRITICAL: 'critical',
  WARNING: 'warning',
  INFO: 'info',
}

const API_STATUS_TO_UI = {
  new: 'new',
  confirmed: 'processing',
  resolved: 'resolved',
}

function mapToAlert(violation) {
  return {
    id: violation.id,
    time: violation.time,
    date: violation.date,
    typeLabel: violation.typeLabel,
    type: violation.type,
    severity: API_SEVERITY_TO_BADGE[violation.severity] || 'warning',
    status: API_STATUS_TO_UI[violation.status] || violation.status,
    confidence: violation.confidence,
  }
}

function mapToImage(violation) {
  return {
    id: `IMG-${violation.id}`,
    eventId: violation.id,
    type: violation.type,
    typeLabel: violation.typeLabel,
    cameraId: violation.cameraId,
    cameraName: violation.cameraName,
    zone: violation.zone,
    time: `${violation.date} ${violation.time}`,
    confidence: violation.confidence,
    severity: API_SEVERITY_TO_BADGE[violation.severity] || 'warning',
    resolved: violation.status === 'resolved',
  }
}

function auditLogMatchesCamera(log, cameraId) {
  if (!cameraId) return false
  if (log.resource_id === cameraId) return true
  if (log.resource_type === 'camera' && log.resource_id === cameraId) return true

  try {
    const metadata = JSON.parse(log.metadata_json || '{}')
    return metadata.camera_id === cameraId || metadata.cameraId === cameraId
  } catch {
    return (log.metadata_json || '').includes(cameraId)
  }
}

function CameraDetailPage() {
  const { cameraId } = useParams()
  const { canManageAtshZones } = usePermissions()
  const [camera, setCamera] = useState(null)
  const {
    lifecycle,
    lifecycleLabel,
    capabilities,
    canRunAi,
    canRunRules,
    loading: zoneReadinessLoading,
  } = useCameraLifecycle(camera)
  const [alerts, setAlerts] = useState([])
  const [images, setImages] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [snapshotUrl, setSnapshotUrl] = useState('')
  const [snapshotCapturedAt, setSnapshotCapturedAt] = useState('')
  const [snapshotLoading, setSnapshotLoading] = useState(false)
  const [snapshotCapturing, setSnapshotCapturing] = useState(false)
  const [snapshotError, setSnapshotError] = useState('')
  const [timeFilter, setTimeFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')
  const [engineEvents, setEngineEvents] = useState([])
  const [timelineLoading, setTimelineLoading] = useState(false)
  const [auditLogs, setAuditLogs] = useState([])
  const [journalLoading, setJournalLoading] = useState(false)
  const [journalError, setJournalError] = useState('')
  const [zoomImage, setZoomImage] = useState(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      setLoading(true)

      try {
        const loadedCamera = await getCameraById(cameraId)
        if (cancelled) return

        if (!loadedCamera) {
          setCamera(null)
          setAlerts([])
          setImages([])
          return
        }

        setCamera(loadedCamera)

        try {
          const events = await getEvents()
          if (cancelled) return

          const violations = events
            .map(mapApiEventToViolation)
            .map((item) => ({ ...item, cameraId: loadedCamera.id }))
            .filter((item) => item.cameraName === loadedCamera.name)

          setAlerts(violations.map(mapToAlert))
          setImages(violations.map(mapToImage))
        } catch {
          if (cancelled) return
          setAlerts(getEventsByCamera(cameraId))
          setImages(getViolationImagesByCamera(cameraId))
        }
      } catch {
        if (cancelled) return
        const mockCamera = getMockCameraById(cameraId)
        setCamera(mockCamera)
        if (mockCamera) {
          setAlerts(getEventsByCamera(cameraId))
          setImages(getViolationImagesByCamera(cameraId))
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()

    return () => {
      cancelled = true
    }
  }, [cameraId])

  const loadLatestSnapshot = useCallback(async (targetCameraId) => {
    if (!targetCameraId) return

    setSnapshotLoading(true)
    setSnapshotError('')

    try {
      const result = await getLatestCameraSnapshot(targetCameraId)
      if (result.success && result.url) {
        setSnapshotUrl(result.url)
        setSnapshotCapturedAt(result.captured_at || '')
      } else {
        setSnapshotUrl('')
        setSnapshotCapturedAt('')
        if (result.error) setSnapshotError(result.error)
      }
    } catch (error) {
      setSnapshotUrl('')
      setSnapshotCapturedAt('')
      setSnapshotError(error.message)
    } finally {
      setSnapshotLoading(false)
    }
  }, [])

  useEffect(() => {
    if (!cameraId || !camera) return
    loadLatestSnapshot(cameraId)
  }, [camera, cameraId, loadLatestSnapshot])

  const loadEngineTimeline = useCallback(async () => {
    if (!cameraId) return
    setTimelineLoading(true)
    try {
      const timeline = await getCameraEventTimeline(cameraId)
      setEngineEvents(timeline)
    } catch {
      setEngineEvents([])
    } finally {
      setTimelineLoading(false)
    }
  }, [cameraId])

  const loadJournal = useCallback(async () => {
    if (!cameraId) return

    setJournalLoading(true)
    setJournalError('')

    try {
      const logs = await listAuditLogs({ limit: 200 })
      setAuditLogs(logs.filter((log) => auditLogMatchesCamera(log, cameraId)))
    } catch (error) {
      setAuditLogs([])
      setJournalError(error.message)
    } finally {
      setJournalLoading(false)
    }
  }, [cameraId])

  useEffect(() => {
    if (activeTab === 'events' || activeTab === 'ai') {
      loadEngineTimeline()
    }
    if (activeTab === 'journal') {
      loadJournal()
    }
  }, [activeTab, loadEngineTimeline, loadJournal])

  useRealtimeEvents({
    filterCameraId: cameraId,
    eventTypes: ['event.created', 'event.updated'],
    onMessage: () => {
      loadEngineTimeline()
    },
  })

  const handleCaptureSnapshot = async () => {
    if (!cameraId) return

    setSnapshotCapturing(true)
    setSnapshotError('')

    try {
      const result = await captureCameraSnapshot(cameraId)
      if (result.success && result.url) {
        setSnapshotUrl(result.url)
        setSnapshotCapturedAt(result.captured_at || new Date().toISOString())
      } else {
        setSnapshotError(result.error || 'Không chụp được snapshot')
      }
    } catch (error) {
      setSnapshotError(error.message)
    } finally {
      setSnapshotCapturing(false)
    }
  }

  const filteredAlerts = useMemo(() => {
    let result = alerts
    if (timeFilter === 'today') result = result.filter((alert) => alert.date === TODAY)
    if (timeFilter === 'week') result = result.filter((alert) => Number(alert.date.slice(-2)) >= 12)
    if (timeFilter === 'month') result = result.filter((alert) => alert.date.startsWith(TODAY.slice(0, 7)))
    if (typeFilter !== 'all') {
      result = result.filter((alert) => alert.type === typeFilter)
    }
    return result
  }, [alerts, timeFilter, typeFilter])

  const filteredImages = images.filter((image) =>
    filteredAlerts.some((alert) => alert.id === image.eventId),
  )

  const openAlerts = useMemo(
    () => alerts.filter((alert) => alert.status !== 'resolved').length,
    [alerts],
  )

  const toggleResolved = (imageId) => {
    setImages((current) =>
      current.map((image) =>
        image.id === imageId ? { ...image, resolved: !image.resolved } : image,
      ),
    )
  }

  const viewViolationLarge = (image) => {
    if (!image) return
    setZoomImage(image)
  }

  const downloadViolationImage = (image) => {
    if (!image) return

    const lines = [
      'AMS — Bằng chứng vi phạm ATSH',
      `ID: ${image.eventId || image.id}`,
      `Loại: ${image.typeLabel}`,
      `Camera: ${image.cameraName}`,
      `Khu vực: ${image.zone || 'N/A'}`,
      `Thời gian: ${image.time}`,
      `Độ tin cậy AI: ${image.confidence}%`,
      `Trạng thái: ${image.resolved ? 'Đã xử lý' : 'Chưa xử lý'}`,
    ]

    downloadTextFile(
      `vi-pham-${image.eventId || image.id}.txt`,
      `${lines.join('\n')}\n`,
    )
  }

  if (loading) {
    return (
      <div className="camera-detail camera-detail--empty">
        <p>Đang tải thông tin camera...</p>
      </div>
    )
  }

  if (!camera) {
    return (
      <div className="camera-detail camera-detail--empty">
        <p>Không tìm thấy camera.</p>
        <Link className="btn btn--primary" to="/monitoring">Quay lại</Link>
      </div>
    )
  }

  const cameraIp = getCameraIp(camera)
  const snapshotImageUrl = snapshotUrl
    ? `${resolveSnapshotAssetUrl(snapshotUrl)}?t=${encodeURIComponent(snapshotCapturedAt || 'latest')}`
    : ''

  const snapshotCard = (
    <CameraSnapshotCard
      snapshotUrl={snapshotUrl}
      capturedAt={snapshotCapturedAt}
      loading={snapshotLoading}
      capturing={snapshotCapturing}
      error={snapshotError}
      onCapture={handleCaptureSnapshot}
      onRefresh={() => loadLatestSnapshot(cameraId)}
    />
  )

  const infoGrid = (
    <div className="info-grid">
      <div><span>ID camera</span><strong>{camera.id}</strong></div>
      <div><span>Tên camera</span><strong>{camera.name}</strong></div>
      <div><span>IP camera</span><strong>{cameraIp}</strong></div>
      <div><span>Khu vực</span><strong>{camera.zone}</strong></div>
      <div><span>Trạng thái</span><strong>{camera.status === 'online' ? 'Online' : 'Offline'}</strong></div>
      <div><span>Uptime</span><strong>{camera.uptime}%</strong></div>
      <div><span>FPS</span><strong>{camera.fps}</strong></div>
      <div><span>Cảnh báo mở</span><strong>{openAlerts}</strong></div>
    </div>
  )

  const eventsPanel = (
    <>
      <section className="panel panel--compact">
        <div className="panel__header">
          <h2 className="panel__title">Event Timeline (Rule Engine)</h2>
          <button type="button" className="btn btn--outline" onClick={loadEngineTimeline}>
            Refresh
          </button>
        </div>
        <EventTimeline
          events={engineEvents}
          loading={timelineLoading}
          emptyMessage="Chưa có sự kiện từ Rule Engine. Dùng Test Rule để sinh event giả."
        />
      </section>

      <section className="panel panel--compact">
        <div className="panel__header">
          <h2 className="panel__title">Bộ lọc</h2>
        </div>
        <div className="filter-panel">
          <div className="filter-panel__group">
            <span className="filter-panel__label">Thời gian</span>
            <div className="filter-chips">
              {timeFilters.map((filter) => (
                <button
                  key={filter.value}
                  type="button"
                  className={`filter-chip${timeFilter === filter.value ? ' filter-chip--active' : ''}`}
                  onClick={() => setTimeFilter(filter.value)}
                >
                  {filter.label}
                </button>
              ))}
            </div>
          </div>

          <div className="filter-panel__group">
            <span className="filter-panel__label">Loại cảnh báo</span>
            <select
              className="toolbar__select toolbar__select--full"
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
            >
              <option value="all">Tất cả loại</option>
              {alertTypeOptions.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
          </div>
        </div>
      </section>

      <section className="panel panel--compact">
        <div className="panel__header">
          <h2 className="panel__title">Danh sách cảnh báo</h2>
          <span className="panel__meta">{filteredAlerts.length} kết quả</span>
        </div>
        <ul className="alert-list">
          {filteredAlerts.length === 0 ? (
            <li className="alert-list__empty">Không có cảnh báo trong khoảng thời gian này.</li>
          ) : (
            filteredAlerts.map((alert) => (
              <li key={alert.id} className="alert-list__item">
                <div className="alert-list__time">
                  <span>{alert.time}</span>
                  <span>{alert.date.slice(5)}</span>
                </div>
                <div className="alert-list__body">
                  <span className="alert-list__type">{alert.typeLabel}</span>
                  <div className="alert-list__tags">
                    <span className={`badge badge--${alert.severity}`}>
                      {severityLabels[alert.severity]}
                    </span>
                    <span className={`status-tag status-tag--${alert.status}`}>
                      {statusLabels[alert.status]}
                    </span>
                    <span className="confidence-pill">{alert.confidence}% AI</span>
                  </div>
                </div>
              </li>
            ))
          )}
        </ul>
      </section>

      <section className="panel">
        <div className="panel__header">
          <h2 className="panel__title">Ảnh vi phạm</h2>
          <span className="panel__meta">{filteredImages.length} ảnh</span>
        </div>
        {filteredImages.length === 0 ? (
          <div className="violation-empty">Chưa có ảnh vi phạm trong khoảng thời gian đã chọn.</div>
        ) : (
          <div className="violation-grid">
            {filteredImages.map((image) => (
              <ViolationCard
                key={image.id}
                image={{ ...image, time: formatDateTime(image.time.slice(0, 10), image.time.slice(11)) }}
                onResolve={toggleResolved}
                onViewLarge={viewViolationLarge}
                onDownload={downloadViolationImage}
              />
            ))}
          </div>
        )}
      </section>
    </>
  )

  return (
    <div className="camera-detail">
      <div className="camera-detail__topbar">
        <Link className="btn btn--outline" to="/monitoring">
          <ChevronLeft size={16} />
          Quay lại giám sát
        </Link>
        <div className="camera-detail__camera-info">
          <span className="camera-detail__id">{camera.id}</span>
          <span className="camera-detail__name">{camera.name}</span>
          <span className={`status-pill status-pill--${camera.status}`}>
            {camera.status === 'online' ? 'Online' : 'Offline'}
          </span>
          <CameraLifecycleBadge lifecycle={lifecycle} title={lifecycleLabel} />
          <span className="camera-detail__ip">{cameraIp}</span>
        </div>
      </div>

      <nav className="camera-detail__tabs" aria-label="Camera detail tabs">
        {CAMERA_DETAIL_TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={`camera-detail__tab${activeTab === tab.id ? ' camera-detail__tab--active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <ZonePublishNotice cameraId={cameraId} />

      <CameraAtshStatusBanner
        cameraId={cameraId}
        lifecycle={lifecycle}
        loading={zoneReadinessLoading}
        canManage={canManageAtshZones}
      />

      {activeTab === 'overview' ? (
        <div className="camera-detail__layout">
          <section className="panel">
            <div className="panel__header">
              <div>
                <h2 className="panel__title">Tổng quan camera</h2>
                <p className="panel__desc">Thông tin vận hành và trạng thái giám sát hiện tại</p>
              </div>
            </div>
            {infoGrid}
            {snapshotCard}
          </section>
        </div>
      ) : null}

      {activeTab === 'live' ? (
        <div className="camera-detail__layout">
          <section className="camera-detail__video-section">
            <CameraFeed camera={camera} size="large">
              {capabilities.zoneOverlay ? <ZoneLiveOverlay cameraId={cameraId} /> : null}
            </CameraFeed>
            {capabilities.aiDetection ? (
              <DetectionOverlay cameraId={cameraId} snapshotUrl={snapshotImageUrl} />
            ) : (
              <section className="panel camera-detail__ai-gate">
                <p role="status">
                  AI Detection chưa kích hoạt — camera cần hoàn tất thiết kế và publish vùng ATSH (READY trở lên).
                </p>
              </section>
            )}
            {snapshotCard}
          </section>
        </div>
      ) : null}

      {activeTab === 'biosecurity' ? (
        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Quản lý Zone v1.1</h2>
              <p className="panel__desc">Vùng giám sát trên ảnh camera — hỗ trợ Zone và SubZone</p>
            </div>
          </div>
          <ZoneEditor
            cameraId={cameraId}
            previewUrl={snapshotImageUrl}
            readOnly={!canManageAtshZones}
          />
        </section>
      ) : null}

      {activeTab === 'ai' ? (
        <div className="camera-detail__events-layout">
          <section className="panel">
            <div className="panel__header">
              <div>
                <h2 className="panel__title">Rule Engine v1.3</h2>
                <p className="panel__desc">Gắn rule với zone trên camera — mock engine sinh event để test pipeline</p>
              </div>
            </div>
            <RuleEditor
              cameraId={cameraId}
              monitoringReady={canRunRules}
              onEventCreated={() => loadEngineTimeline()}
            />
          </section>

          <section className="panel">
            <div className="panel__header">
              <div>
                <h2 className="panel__title">Observations v1.4</h2>
                <p className="panel__desc">Lớp trung gian Detector → Evaluator — normalized bbox, zone mapping</p>
              </div>
            </div>
            <ObservationViewer
              cameraId={cameraId}
              monitoringReady={canRunAi}
              onEventsCreated={() => loadEngineTimeline()}
            />
          </section>
        </div>
      ) : null}

      {activeTab === 'events' ? (
        <div className="camera-detail__events-layout">{eventsPanel}</div>
      ) : null}

      {activeTab === 'journal' ? (
        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Nhật ký camera</h2>
              <p className="panel__desc">Lịch sử thao tác và thay đổi cấu hình liên quan đến camera này</p>
            </div>
            <button type="button" className="btn btn--outline" onClick={loadJournal}>
              Refresh
            </button>
          </div>
          {journalError ? (
            <p className="panel__desc">{journalError}</p>
          ) : null}
          {journalLoading ? (
            <p className="camera-detail__placeholder">Đang tải nhật ký...</p>
          ) : auditLogs.length === 0 ? (
            <p className="camera-detail__placeholder">Chưa có nhật ký cho camera này.</p>
          ) : (
            <ul className="alert-list">
              {auditLogs.map((log) => (
                <li key={log.id} className="alert-list__item">
                  <div className="alert-list__time">
                    <span>{formatDateTime(log.created_at.slice(0, 10), log.created_at.slice(11, 19))}</span>
                  </div>
                  <div className="alert-list__body">
                    <span className="alert-list__type">{log.action}</span>
                    <div className="alert-list__tags">
                      <span className="status-tag">{log.resource_type}</span>
                      <span className="confidence-pill">{log.user_id}</span>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      ) : null}

      {activeTab === 'settings' ? (
        <section className="panel">
          <div className="panel__header">
            <h2 className="panel__title">Cài đặt camera</h2>
          </div>
          {infoGrid}
          {snapshotCard}
        </section>
      ) : null}

      {zoomImage ? (
        <div className="violation-drawer__zoom" role="dialog" aria-modal="true">
          <button
            type="button"
            className="violation-drawer__zoom-backdrop"
            onClick={() => setZoomImage(null)}
            aria-label="Đóng ảnh"
          />
          <div className="violation-drawer__zoom-panel">
            <AtshViolationSnapshot
              violation={{
                severity: zoomImage.severity === 'critical' ? 'CRITICAL' : 'WARNING',
                confidence: zoomImage.confidence,
                snapshotTone: zoomImage.severity,
              }}
              large
              showMeta
            />
            <p className="violation-drawer__hint">
              {zoomImage.typeLabel} · {zoomImage.cameraName} · {zoomImage.time}
            </p>
            <div className="violation-drawer__zoom-actions">
              <button type="button" className="btn btn--outline" onClick={() => downloadViolationImage(zoomImage)}>
                Tải bằng chứng
              </button>
              <button type="button" className="btn btn--ghost" onClick={() => setZoomImage(null)}>
                Đóng
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}

export default CameraDetailPage
