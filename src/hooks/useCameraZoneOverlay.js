import { useCallback, useEffect, useState } from 'react'
import {
  CAMERA_ZONES_UPDATED_EVENT,
  getZoneUpdatedCameraId,
  isZoneUpdatedWsPayload,
  loadCameraZones,
} from '../services/cameraZoneOverlayService'
import { subscribeWsEvents } from '../services/wsClient'

const ZONE_SYNC_STORAGE_KEY = 'ams:zone-sync'

function shouldRefreshForCamera(eventCameraId, cameraId) {
  if (!eventCameraId) return true
  return eventCameraId === cameraId
}

export function useCameraZoneOverlay(cameraId) {
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)

  const refreshZones = useCallback(async () => {
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
    refreshZones()
  }, [refreshZones])

  useEffect(() => {
    const handleZonesUpdated = (event) => {
      const updatedCameraId = event.detail?.cameraId
      if (shouldRefreshForCamera(updatedCameraId, cameraId)) {
        refreshZones()
      }
    }

    const handleStorageSync = (event) => {
      if (event.key !== ZONE_SYNC_STORAGE_KEY || !event.newValue) return

      try {
        const detail = JSON.parse(event.newValue)
        if (shouldRefreshForCamera(detail?.cameraId, cameraId)) {
          refreshZones()
        }
      } catch {
        refreshZones()
      }
    }

    const handleVisibility = () => {
      if (document.visibilityState === 'visible') {
        refreshZones()
      }
    }

    window.addEventListener(CAMERA_ZONES_UPDATED_EVENT, handleZonesUpdated)
    window.addEventListener('storage', handleStorageSync)
    document.addEventListener('visibilitychange', handleVisibility)

    const unsubscribeWs = subscribeWsEvents({
      onMessage: (payload) => {
        if (!isZoneUpdatedWsPayload(payload)) return
        const updatedCameraId = getZoneUpdatedCameraId(payload)
        if (shouldRefreshForCamera(updatedCameraId, cameraId)) {
          refreshZones()
        }
      },
    })

    return () => {
      window.removeEventListener(CAMERA_ZONES_UPDATED_EVENT, handleZonesUpdated)
      window.removeEventListener('storage', handleStorageSync)
      document.removeEventListener('visibilitychange', handleVisibility)
      unsubscribeWs()
    }
  }, [cameraId, refreshZones])

  return { zones, loading, refreshZones }
}
