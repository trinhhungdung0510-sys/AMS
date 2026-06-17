import { alertTypes } from '../data/mockData'

const variantStyles = {
  dress: {
    gradient: 'linear-gradient(145deg, #1a3a28 0%, #0f2918 50%, #2d4a32 100%)',
    accent: '#f97316',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
    ),
  },
  intrusion: {
    gradient: 'linear-gradient(145deg, #3a1a1a 0%, #291010 50%, #4a2d2d 100%)',
    accent: '#ef4444',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
    ),
  },
  fever: {
    gradient: 'linear-gradient(145deg, #3a2a1a 0%, #291a0f 50%, #4a3a2d 100%)',
    accent: '#eab308',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z" />
      </svg>
    ),
  },
}

function ViolationSnapshot({ alert, camera }) {
  const style = variantStyles[alert.snapshotVariant] ?? variantStyles.dress

  return (
    <article className="violation-card">
      <div
        className="violation-card__image"
        style={{ background: style.gradient, '--accent': style.accent }}
      >
        <div className="violation-card__scanline" />
        <div className="violation-card__icon">{style.icon}</div>
        <div className="violation-card__bbox" />
        <span className="violation-card__ai-tag">AI Detect</span>
        <span className="violation-card__time">{alert.time}</span>
      </div>
      <div className="violation-card__info">
        <span className="violation-card__type">{alertTypes[alert.type]}</span>
        <span className="violation-card__meta">
          {camera.name} · {alert.date}
        </span>
        <span className={`badge badge--${alert.severity}`}>
          {alert.id}
        </span>
      </div>
    </article>
  )
}

export default ViolationSnapshot
