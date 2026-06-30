import { hasValidMonitoringZones } from './cameraZoneReadiness'

/** Mandatory camera lifecycle — derived from published zones + camera flags (no DB schema change). */
export const CAMERA_LIFECYCLE = {
  NEW: 'NEW',
  CONFIGURING: 'CONFIGURING',
  READY: 'READY',
  MONITORING: 'MONITORING',
  PAUSED: 'PAUSED',
}

export const LIFECYCLE_LABELS = {
  [CAMERA_LIFECYCLE.NEW]: 'Camera mới (NEW)',
  [CAMERA_LIFECYCLE.CONFIGURING]: 'Đang cấu hình vùng ATSH (CONFIGURING)',
  [CAMERA_LIFECYCLE.READY]: 'Sẵn sàng giám sát (READY)',
  [CAMERA_LIFECYCLE.MONITORING]: 'Đang giám sát (MONITORING)',
  [CAMERA_LIFECYCLE.PAUSED]: 'Tạm dừng (PAUSED)',
}

export const LIFECYCLE_SHORT_LABELS = {
  [CAMERA_LIFECYCLE.NEW]: 'NEW',
  [CAMERA_LIFECYCLE.CONFIGURING]: 'CONFIGURING',
  [CAMERA_LIFECYCLE.READY]: 'READY',
  [CAMERA_LIFECYCLE.MONITORING]: 'MONITORING',
  [CAMERA_LIFECYCLE.PAUSED]: 'PAUSED',
}

/**
 * Resolve lifecycle from camera record + published (server) zones only.
 * Draft edits must NOT affect lifecycle — pass isZoneEditing for CONFIGURING session.
 */
export function resolveCameraLifecycle({ camera, publishedZones = [], isZoneEditing = false }) {
  if (!camera) return null

  if (camera.is_active === false) {
    return CAMERA_LIFECYCLE.PAUSED
  }

  const hasPublished = hasValidMonitoringZones(publishedZones)

  if (isZoneEditing) {
    return CAMERA_LIFECYCLE.CONFIGURING
  }

  if (!hasPublished) {
    return CAMERA_LIFECYCLE.NEW
  }

  if (camera.status === 'online') {
    return CAMERA_LIFECYCLE.MONITORING
  }

  return CAMERA_LIFECYCLE.READY
}

export function getLifecycleCapabilities(lifecycle, publishedZones = []) {
  const hasPublished = hasValidMonitoringZones(publishedZones)

  const base = {
    rtsp: true,
    liveView: true,
    onlineCheck: true,
    zoneOverlay: false,
    zoneEdit: false,
    aiDetection: false,
    ruleEngine: false,
    notifications: false,
    dashboardAnalytics: false,
  }

  if (!lifecycle) return base

  if (lifecycle === CAMERA_LIFECYCLE.PAUSED) {
    return {
      ...base,
      liveView: true,
      zoneOverlay: hasPublished,
    }
  }

  if (lifecycle === CAMERA_LIFECYCLE.NEW) {
    return { ...base }
  }

  const pipelineEnabled = hasPublished && [
    CAMERA_LIFECYCLE.CONFIGURING,
    CAMERA_LIFECYCLE.READY,
    CAMERA_LIFECYCLE.MONITORING,
  ].includes(lifecycle)

  if (lifecycle === CAMERA_LIFECYCLE.CONFIGURING) {
    return {
      ...base,
      zoneOverlay: hasPublished,
      zoneEdit: true,
      aiDetection: pipelineEnabled,
      ruleEngine: pipelineEnabled,
    }
  }

  if (lifecycle === CAMERA_LIFECYCLE.READY) {
    return {
      ...base,
      zoneOverlay: true,
      zoneEdit: true,
      aiDetection: true,
      ruleEngine: true,
      notifications: true,
      dashboardAnalytics: true,
    }
  }

  if (lifecycle === CAMERA_LIFECYCLE.MONITORING) {
    return {
      rtsp: true,
      liveView: true,
      onlineCheck: true,
      zoneOverlay: true,
      zoneEdit: true,
      aiDetection: true,
      ruleEngine: true,
      notifications: true,
      dashboardAnalytics: true,
    }
  }

  return base
}

export function canRunAiPipeline(lifecycle, publishedZones = []) {
  return getLifecycleCapabilities(lifecycle, publishedZones).aiDetection
}

export function canRunRuleEngine(lifecycle, publishedZones = []) {
  return getLifecycleCapabilities(lifecycle, publishedZones).ruleEngine
}

export function shouldShowLargeNewCameraBanner(lifecycle) {
  return lifecycle === CAMERA_LIFECYCLE.NEW
}
