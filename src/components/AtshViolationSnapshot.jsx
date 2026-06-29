import { ATSH_SEVERITY } from '../data/atshViolations'

function AtshViolationSnapshot({ violation, large = false, showMeta = true }) {
  const safeViolation = violation || {}
  const severity = ATSH_SEVERITY[safeViolation.severity] || ATSH_SEVERITY.WARNING

  return (
    <div
      className={`atsh-snapshot atsh-snapshot--${safeViolation.snapshotTone || severity.tone}${large ? ' atsh-snapshot--large' : ''}`}
    >
      <div className="atsh-snapshot__grid" />
      <div className="atsh-snapshot__scanline" />
      <div className="atsh-snapshot__bbox" />
      <span className="atsh-snapshot__ai">AI Detect</span>
      {showMeta && (
        <>
          <span className="atsh-snapshot__confidence">{safeViolation.confidence ?? 0}%</span>
          <span className={`atsh-snapshot__severity atsh-snapshot__severity--${severity.tone}`}>
            {severity.label}
          </span>
        </>
      )}
    </div>
  )
}

export default AtshViolationSnapshot
