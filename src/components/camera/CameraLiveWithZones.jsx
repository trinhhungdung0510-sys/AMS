import { useMemo } from 'react'
import CameraFeed from '../CameraFeed'
import ZoneLiveOverlay from './ZoneLiveOverlay'
import { useCameraZoneReadiness } from '../../hooks/useCameraZoneReadiness'
import { getLifecycleCapabilities, resolveCameraLifecycle } from '../../utils/cameraLifecycle'

function normalizeCamera(camera) {
  if (!camera?.id) return null
  return {
    id: camera.id,
    name: camera.name || camera.ten_camera || camera.id,
    status: String(camera.status || 'offline').toLowerCase(),
    resolution: camera.resolution || '1080p',
    fps: camera.fps || 25,
  }
}

function CameraLiveWithZones({ camera, size = 'tile', compactLabels = false }) {
  const normalized = useMemo(() => normalizeCamera(camera), [camera])
  const { zones } = useCameraZoneReadiness(normalized?.id)

  const lifecycle = useMemo(
    () => resolveCameraLifecycle({ camera: normalized, publishedZones: zones }),
    [normalized, zones],
  )

  const capabilities = useMemo(
    () => getLifecycleCapabilities(lifecycle, zones),
    [lifecycle, zones],
  )

  if (!normalized) return null

  const showCompactLabels = compactLabels || size === 'tile'

  return (
    <CameraFeed camera={normalized} size={size}>
      {capabilities.zoneOverlay ? (
        <ZoneLiveOverlay cameraId={normalized.id} compact={showCompactLabels} />
      ) : null}
    </CameraFeed>
  )
}

export default CameraLiveWithZones
