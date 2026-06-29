import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Camera,
  CheckCircle2,
  ExternalLink,
  Image as ImageIcon,
  Video,
  X,
} from 'lucide-react'
import AtshViolationSnapshot from '../AtshViolationSnapshot'
import { useViolationProcessing } from '../../context/ViolationProcessingContext'
import { VIOLATION_EMPTY_LABEL } from '../../utils/violationDetailModel'

function InfoRow({ label, value, children }) {
  return (
    <div className="violation-drawer__row">
      <dt>{label}</dt>
      <dd>{children || value || VIOLATION_EMPTY_LABEL}</dd>
    </div>
  )
}

function ViolationProcessingDrawer() {
  const {
    detail,
    selectedSource,
    isDrawerOpen,
    closeViolation,
    updateViolationState,
    resolveViolation,
  } = useViolationProcessing()
  const [note, setNote] = useState('')
  const [imageZoomOpen, setImageZoomOpen] = useState(false)

  useEffect(() => {
    if (!isDrawerOpen) {
      setImageZoomOpen(false)
      return undefined
    }

    setNote(detail?.note || '')

    const onKeyDown = (event) => {
      if (event.key === 'Escape') {
        if (imageZoomOpen) {
          setImageZoomOpen(false)
        } else {
          closeViolation()
        }
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [isDrawerOpen, detail, closeViolation, imageZoomOpen])

  if (!isDrawerOpen || !detail) return null

  const cameraPath = detail.cameraId ? `/monitoring/${detail.cameraId}` : '/camera'
  const timelineSteps = Array.isArray(detail.timeline) ? detail.timeline : []
  const snapshotViolation = {
    severity: detail.severityTone === 'critical' ? 'CRITICAL' : detail.severityTone === 'warning' ? 'WARNING' : 'INFO',
    confidence: detail.confidence ?? 0,
    snapshotTone: detail.severityTone,
  }

  const markResolved = () => {
    resolveViolation(selectedSource || detail.raw, { note })
  }

  const saveNote = () => {
    updateViolationState(detail.id, { note })
  }

  return (
    <>
      <div className="violation-drawer">
        <button type="button" className="violation-drawer__backdrop" onClick={closeViolation} aria-label="Đóng panel" />
        <aside className="violation-drawer__panel" role="dialog" aria-modal="true" aria-labelledby="violation-drawer-title">
          <header className="violation-drawer__header">
            <div>
              <p className="violation-drawer__eyebrow">Trung tâm xử lý vi phạm</p>
              <h2 id="violation-drawer-title">{detail.typeLabel}</h2>
            </div>
            <button type="button" className="violation-drawer__close" onClick={closeViolation} aria-label="Đóng">
              <X size={18} />
            </button>
          </header>

          <div className="violation-drawer__body">
            <section className="violation-drawer__section">
              <h3>Thông tin chung</h3>
              <dl className="violation-drawer__grid">
                <InfoRow label="Mã vi phạm" value={detail.code} />
                <InfoRow label="Thời gian" value={detail.occurredAt} />
                <InfoRow label="Mức độ">
                  <span className={`atsh-severity atsh-severity--${detail.severityTone}`}>{detail.severityLabel}</span>
                </InfoRow>
                <InfoRow label="Trạng thái">
                  <span className={`atsh-status atsh-status--${detail.statusKey}`}>{detail.statusLabel}</span>
                </InfoRow>
                <InfoRow label="Camera" value={detail.cameraName} />
                <InfoRow label="Khu vực" value={detail.zoneName} />
                <InfoRow label="Quy tắc ATSH" value={detail.ruleName} />
              </dl>
            </section>

            <section className="violation-drawer__section">
              <h3>Đối tượng vi phạm</h3>
              {detail.objectKind === 'person' ? (
                <dl className="violation-drawer__grid">
                  <InfoRow label="Track ID" value={detail.person.trackId} />
                  <InfoRow label="Đồng phục" value={detail.person.uniform} />
                  <InfoRow label="Vùng đang đứng" value={detail.person.currentZone} />
                  <InfoRow label="Vùng được phép" value={detail.person.allowedZone} />
                </dl>
              ) : null}
              {detail.objectKind === 'vehicle' ? (
                <dl className="violation-drawer__grid">
                  <InfoRow label="Loại xe" value={detail.vehicle.vehicleType} />
                  <InfoRow label="Khu vực" value={detail.vehicle.zone} />
                </dl>
              ) : null}
              {detail.objectKind === 'animal' ? (
                <dl className="violation-drawer__grid">
                  <InfoRow label="Loại động vật" value={detail.animal.animalType} />
                </dl>
              ) : null}
            </section>

            <section className="violation-drawer__section">
              <h3>Bằng chứng</h3>
              <div className="violation-drawer__evidence">
                {detail.hasSnapshot ? (
                  <button type="button" className="violation-drawer__snapshot-btn" onClick={() => setImageZoomOpen(true)}>
                    <img src={detail.snapshotUrl} alt={detail.typeLabel} className="violation-drawer__snapshot-image" />
                    <span className="violation-drawer__snapshot-overlay">Khung AI phát hiện</span>
                  </button>
                ) : (
                  <div className="violation-drawer__snapshot-fallback">
                    <AtshViolationSnapshot violation={snapshotViolation} large showMeta />
                    <p className="violation-drawer__hint">Ảnh minh họa Pilot · {VIOLATION_EMPTY_LABEL} snapshot thật</p>
                  </div>
                )}
                <dl className="violation-drawer__grid violation-drawer__grid--compact">
                  <InfoRow label="Snapshot" value={detail.hasSnapshot ? 'Có' : VIOLATION_EMPTY_LABEL} />
                  <InfoRow label="Video" value={detail.hasVideo ? 'Có' : VIOLATION_EMPTY_LABEL} />
                  <InfoRow label="Thời gian ghi nhận" value={detail.occurredAt} />
                </dl>
              </div>
            </section>

            <section className="violation-drawer__section">
              <h3>Diễn biến</h3>
              <div className="violation-drawer__timeline">
                {timelineSteps.map((step, index) => (
                  <div key={`${step.time}-${step.label}-${index}`} className="violation-drawer__timeline-step">
                    <span className="violation-drawer__timeline-time">{step.time}</span>
                    <span className={`violation-drawer__timeline-dot violation-drawer__timeline-dot--${step.tone || 'info'}`} />
                    <p>{step.label}</p>
                    {index < timelineSteps.length - 1 ? (
                      <span className="violation-drawer__timeline-arrow" aria-hidden="true">↓</span>
                    ) : null}
                  </div>
                ))}
              </div>
            </section>

            <section className="violation-drawer__section">
              <h3>Đánh giá</h3>
              <div className="violation-drawer__confidence">
                <strong>{detail.confidenceLabel}</strong>
                <span>Độ tin cậy AI</span>
                {detail.confidence != null ? (
                  <div className="violation-drawer__confidence-bar">
                    <span style={{ width: `${Math.min(100, detail.confidence)}%` }} />
                  </div>
                ) : null}
              </div>
            </section>

            <section className="violation-drawer__section">
              <h3>Trạng thái xử lý</h3>
              <div className="violation-drawer__status-group">
                {[
                  ['new', 'Chưa xử lý'],
                  ['confirmed', 'Đang xử lý'],
                  ['resolved', 'Đã xử lý'],
                  ['dismissed', 'Báo động giả'],
                ].map(([key, label]) => (
                  <button
                    key={key}
                    type="button"
                    className={`violation-drawer__status-btn${detail.statusKey === key ? ' violation-drawer__status-btn--active' : ''}`}
                    onClick={() => updateViolationState(detail.id, { statusKey: key, note })}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </section>

            <section className="violation-drawer__section">
              <h3>Ghi chú</h3>
              <label className="violation-drawer__note">
                <span className="sr-only">Ghi chú xử lý</span>
                <textarea
                  rows={3}
                  placeholder='Ví dụ: "Công nhân đã quay lại sát trùng."'
                  value={note}
                  onChange={(event) => setNote(event.target.value)}
                  onBlur={saveNote}
                />
              </label>
            </section>
          </div>

          <footer className="violation-drawer__footer">
            <Link to={cameraPath} className="btn btn--outline btn--sm" onClick={closeViolation}>
              <Camera size={14} /> Xem Camera
            </Link>
            <button
              type="button"
              className="btn btn--outline btn--sm"
              disabled={!detail.hasSnapshot}
              onClick={() => detail.hasSnapshot && setImageZoomOpen(true)}
            >
              <ImageIcon size={14} /> Mở ảnh
            </button>
            {detail.hasVideo ? (
              <a href={detail.videoUrl} target="_blank" rel="noreferrer" className="btn btn--outline btn--sm">
                <Video size={14} /> Mở video
              </a>
            ) : (
              <button type="button" className="btn btn--outline btn--sm" disabled>
                <Video size={14} /> Mở video
              </button>
            )}
            <button type="button" className="btn btn--primary btn--sm" onClick={markResolved}>
              <CheckCircle2 size={14} /> Đánh dấu đã xử lý
            </button>
            <button type="button" className="btn btn--ghost btn--sm" onClick={closeViolation}>
              Đóng
            </button>
          </footer>
        </aside>
      </div>

      {imageZoomOpen && detail.hasSnapshot ? (
        <div className="violation-drawer__zoom" role="dialog" aria-modal="true">
          <button type="button" className="violation-drawer__zoom-backdrop" onClick={() => setImageZoomOpen(false)} aria-label="Đóng ảnh" />
          <div className="violation-drawer__zoom-panel">
            <img src={detail.snapshotUrl} alt={detail.typeLabel} />
            <button type="button" className="btn btn--outline" onClick={() => window.open(detail.snapshotUrl, '_blank', 'noopener,noreferrer')}>
              <ExternalLink size={14} /> Mở tab mới
            </button>
          </div>
        </div>
      ) : null}
    </>
  )
}

export default ViolationProcessingDrawer
