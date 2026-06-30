import { useMemo } from 'react'
import { useCameraZoneReadiness } from './useCameraZoneReadiness'
import {
  CAMERA_LIFECYCLE,
  canRunAiPipeline,
  canRunRuleEngine,
  getLifecycleCapabilities,
  LIFECYCLE_LABELS,
  LIFECYCLE_SHORT_LABELS,
  resolveCameraLifecycle,
  shouldShowLargeNewCameraBanner,
} from '../utils/cameraLifecycle'

export function useCameraLifecycle(camera, { isZoneEditing = false } = {}) {
  const cameraId = camera?.id ?? null
  const readiness = useCameraZoneReadiness(cameraId)

  const lifecycle = useMemo(
    () => resolveCameraLifecycle({
      camera,
      publishedZones: readiness.zones,
      isZoneEditing,
    }),
    [camera, readiness.zones, isZoneEditing],
  )

  const capabilities = useMemo(
    () => getLifecycleCapabilities(lifecycle, readiness.zones),
    [lifecycle, readiness.zones],
  )

  const canRunAi = useMemo(
    () => canRunAiPipeline(lifecycle, readiness.zones),
    [lifecycle, readiness.zones],
  )

  const canRunRules = useMemo(
    () => canRunRuleEngine(lifecycle, readiness.zones),
    [lifecycle, readiness.zones],
  )

  return {
    ...readiness,
    lifecycle,
    lifecycleLabel: lifecycle ? LIFECYCLE_LABELS[lifecycle] : '',
    lifecycleShortLabel: lifecycle ? LIFECYCLE_SHORT_LABELS[lifecycle] : '',
    capabilities,
    canRunAi,
    canRunRules,
    isMonitoringReady: canRunAi,
    showNewCameraBanner: shouldShowLargeNewCameraBanner(lifecycle),
    isPaused: lifecycle === CAMERA_LIFECYCLE.PAUSED,
  }
}
