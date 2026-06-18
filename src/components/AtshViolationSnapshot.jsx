import { ATSH_SEVERITY } from '../data/atshViolations'

function AtshViolationSnapshot({ violation, large = false, showMeta = true }) {
  const severity = ATSH_SEVERITY[violation.severity] || ATSH_SEVERITY.WARNING

  return (
    <div
      className={`atsh-snapshot atsh-snapshot--${violation.snapshotTone || severity.tone}${large ? ' atsh-snapshot--large' : ''}`}
    >
      <div className="atsh-snapshot__grid" />
      <div className="atsh-snapshot__scanline" />
      <div className="atsh-snapshot__bbox" />
      <span className="atsh-snapshot__ai">AI Detect</span>
      {showMeta && (
        <>
          <span className="atsh-snapshot__confidence">{violation.confidence}%</span>
          <span className={`atsh-snapshot__severity atsh-snapshot__severity--${severity.tone}`}>
            {severity.label}
          </span>
        </>
      )}
    </div>
  )
}

export default AtshViolationSnapshot
