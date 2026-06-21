function UniformInUseDialog({ open, zones = [], onClose }) {
  if (!open) return null

  return (
    <div className="compliance-modal" role="dialog" aria-modal="true" aria-labelledby="uniform-in-use-title">
      <button type="button" className="compliance-modal__backdrop" onClick={onClose} aria-label="Đóng" />
      <div className="compliance-modal__panel">
        <header className="compliance-modal__header">
          <div>
            <h2 id="uniform-in-use-title">Không thể xóa Uniform</h2>
            <p>Các Zone đang sử dụng:</p>
          </div>
          <button type="button" className="btn btn--outline btn--sm" onClick={onClose}>Đóng</button>
        </header>

        <div className="compliance-modal__content">
          <ul className="uniform-in-use-dialog__zones">
            {zones.map((zone) => (
              <li key={zone.id}>{zone.name}</li>
            ))}
          </ul>
          <p className="uniform-in-use-dialog__hint">
            Vui lòng gỡ gán trước khi xóa.
          </p>
        </div>
      </div>
    </div>
  )
}

export default UniformInUseDialog
