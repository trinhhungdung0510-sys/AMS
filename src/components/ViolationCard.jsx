import { CheckCircle2, Download, Eye } from 'lucide-react'

function ViolationCard({ image, onResolve, onViewLarge, onDownload }) {
  return (
    <article className="violation-card">
      <div className={`violation-card__snapshot violation-card__snapshot--${image.type}`}>
        <div className="violation-card__scanline" />
        <div className="violation-card__bbox" />
        <span className="violation-card__tag">AI Snapshot</span>
        <span className="violation-card__confidence">{image.confidence}%</span>
      </div>
      <div className="violation-card__content">
        <h3>{image.typeLabel}</h3>
        <p>{image.cameraName}</p>
        <span>{image.time}</span>
        <div className="violation-card__actions">
          <button
            type="button"
            className="btn btn--ghost"
            onClick={() => onViewLarge?.(image)}
          >
            <Eye size={15} />
            Xem lớn
          </button>
          <button
            type="button"
            className="btn btn--ghost"
            onClick={() => onDownload?.(image)}
          >
            <Download size={15} />
            Tải ảnh
          </button>
          <button
            type="button"
            className={`btn ${image.resolved ? 'btn--success' : 'btn--outline'}`}
            onClick={() => onResolve?.(image.id)}
          >
            <CheckCircle2 size={15} />
            {image.resolved ? 'Đã xử lý' : 'Đánh dấu'}
          </button>
        </div>
      </div>
    </article>
  )
}

export default ViolationCard
