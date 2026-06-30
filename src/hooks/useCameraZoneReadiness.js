import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  CAMERA_ZONES_UPDATED_EVENT,
  loadCameraZones,
} from '../services/cameraZoneOverlayService'
import { ZONE_PUBLISHED_EVENT } from '../services/zonePublishService'
import {
  getMonitoringStatus,
  getMonitoringStatusLabel,
  hasValidMonitoringZones,
} from '../utils/cameraZoneReadiness'

const ZONE_SYNC_STORAGE_KEY = 'ams:zone-sync'

function shouldRefreshForCamera(eventCameraId, cameraId) {
  if (!eventCameraId) return true
  return eventCameraId === cameraId
}

export function useCameraZoneReadiness(cameraId) {
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    if (!cameraId) {
      setZones([])
      setLoading(false)
      return
    }

    setLoading(true)
    try {
      const data = await loadCameraZones(cameraId)
      setZones(data)
    } catch {
      setZones([])
    } finally {
      setLoading(false)
    }
  }, [cameraId])

  useEffect(() => {
    refresh()
  }, [refresh])

  useEffect(() => {
    const handleUpdated = (event) => {
      if (shouldRefreshForCamera(event.detail?.cameraId, cameraId)) {
        refresh()
      }
    }

    const handleStorage = (event) => {
      if (event.key !== ZONE_SYNC_STORAGE_KEY || !event.newValue) return
      try {
        const detail = JSON.parse(event.newValue)
        if (shouldRefreshForCamera(detail?.cameraId, cameraId)) {
          refresh()
        }
      } catch {
        refresh()
      }
    }

    const handlePublished = (event) => {
      if (shouldRefreshForCamera(event.detail?.cameraId, cameraId)) {
        refresh()
      }
    }

    window.addEventListener(CAMERA_ZONES_UPDATED_EVENT, handleUpdated)
    window.addEventListener(ZONE_PUBLISHED_EVENT, handlePublished)
    window.addEventListener('storage', handleStorage)

    return () => {
      window.removeEventListener(CAMERA_ZONES_UPDATED_EVENT, handleUpdated)
      window.removeEventListener(ZONE_PUBLISHED_EVENT, handlePublished)
      window.removeEventListener('storage', handleStorage)
    }
  }, [cameraId, refresh])

  const status = useMemo(() => getMonitoringStatus(zones), [zones])
  const statusLabel = useMemo(() => getMonitoringStatusLabel(zones), [zones])
  const isMonitoringReady = useMemo(() => hasValidMonitoringZones(zones), [zones])

  return {
    zones,
    loading,
    refresh,
    status,
    statusLabel,
    isMonitoringReady,
  }
}
