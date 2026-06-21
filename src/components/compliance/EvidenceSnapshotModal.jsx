function EvidenceSnapshotModal({ event, open, onClose }) {
  if (!open || !event) return null

  return (
    <div className="compliance-modal" role="dialog" aria-modal="true">
      <button type="button" className="compliance-modal__backdrop" onClick={onClose} aria-label="Đóng" />
      <div className="compliance-modal__panel">
        <header className="compliance-modal__header">
          <div>
            <h2>{event.typeLabel}</h2>
            <p>{event.ruleName || event.ruleId || 'Compliance evidence'}</p>
          </div>
          <button type="button" className="btn btn--outline btn--sm" onClick={onClose}>Đóng</button>
        </header>

        <div className="compliance-modal__content">
          <div className="compliance-modal__image-wrap">
            {event.snapshotUrl ? (
              <img src={event.snapshotUrl} alt={event.typeLabel} className="compliance-modal__image" />
            ) : (
              <div className="compliance-modal__image compliance-modal__image--empty">Không có ảnh bằng chứng</div>
            )}
          </div>

          <dl className="compliance-modal__info">
            <div>
              <dt>Rule Name</dt>
              <dd>{event.ruleName || '—'}</dd>
            </div>
            <div>
              <dt>Camera</dt>
              <dd>{event.cameraName}</dd>
            </div>
            <div>
              <dt>Zone</dt>
              <dd>{event.zoneName}</dd>
            </div>
            <div>
              <dt>Timestamp</dt>
              <dd>{event.timestamp}</dd>
            </div>
            <div>
              <dt>Score</dt>
              <dd>{event.score}%</dd>
            </div>
            <div>
              <dt>Event Type</dt>
              <dd>{event.eventType}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  )
}

export default EvidenceSnapshotModal
