import { resolveScorePercent } from '../../data/complianceCenter'

function ComplianceEventCard({ event, onOpenSnapshot }) {
  const thumbUrl = event.snapshotUrl

  return (
    <article className="compliance-card">
      <button
        type="button"
        className="compliance-card__thumb-btn"
        onClick={() => onOpenSnapshot(event)}
        aria-label="Xem ảnh bằng chứng"
      >
        {thumbUrl ? (
          <img src={thumbUrl} alt="" className="compliance-card__thumb" loading="lazy" />
        ) : (
          <div className="compliance-card__thumb compliance-card__thumb--empty">
            <span>Không có ảnh</span>
          </div>
        )}
      </button>

      <div className="compliance-card__body">
        <h3 className="compliance-card__title">{event.title || event.typeLabel}</h3>
        {event.description ? <p className="compliance-card__description">{event.description}</p> : null}
        {event.recommendedAction ? (
          <p className="compliance-card__action">
            <strong>Hành động:</strong> {event.recommendedAction}
          </p>
        ) : null}

        <dl className="compliance-card__meta">
          <div>
            <dt>Camera</dt>
            <dd>{event.cameraName}</dd>
          </div>
          <div>
            <dt>Zone</dt>
            <dd>{event.zoneName}</dd>
          </div>
          <div>
            <dt>Time</dt>
            <dd>{event.timestamp}</dd>
          </div>
          <div>
            <dt>Mức độ</dt>
            <dd>{event.severityLabel || event.severity || '—'}</dd>
          </div>
          <div>
            <dt>Score</dt>
            <dd>{resolveScorePercent(event)}%</dd>
          </div>
        </dl>
      </div>
    </article>
  )
}

export default ComplianceEventCard
