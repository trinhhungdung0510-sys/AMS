import { LIFECYCLE_SHORT_LABELS } from '../../utils/cameraLifecycle'

const BADGE_CLASS = {
  NEW: 'camera-lifecycle-badge--new',
  CONFIGURING: 'camera-lifecycle-badge--configuring',
  READY: 'camera-lifecycle-badge--ready',
  MONITORING: 'camera-lifecycle-badge--monitoring',
  PAUSED: 'camera-lifecycle-badge--paused',
}

function CameraLifecycleBadge({ lifecycle, title }) {
  if (!lifecycle) return null

  return (
    <span
      className={`camera-lifecycle-badge ${BADGE_CLASS[lifecycle] || ''}`}
      title={title}
    >
      {LIFECYCLE_SHORT_LABELS[lifecycle] || lifecycle}
    </span>
  )
}

export default CameraLifecycleBadge
