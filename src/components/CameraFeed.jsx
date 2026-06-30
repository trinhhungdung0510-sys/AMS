import { useEffect, useState } from 'react'
import { Camera, Radio } from 'lucide-react'
import { apiFetch } from '../services/apiClient'

function CameraFeed({ camera, size = 'tile', children = null }) {
  const isOnline = camera.status === 'online'
  const [frameSrc, setFrameSrc] = useState('')
  const [frameTick, setFrameTick] = useState(() => Date.now())

  useEffect(() => {
    if (!isOnline) return undefined

    const timer = setInterval(() => setFrameTick(Date.now()), 15000)
    return () => clearInterval(timer)
  }, [isOnline, camera.id])

  useEffect(() => {
    if (!isOnline) {
      setFrameSrc((prev) => {
        if (prev) URL.revokeObjectURL(prev)
        return ''
      })
      return undefined
    }

    let cancelled = false
    let objectUrl = ''

    async function loadFrame() {
      try {
        const response = await apiFetch(`/cameras/${camera.id}/frame?t=${frameTick}`)
        if (!response.ok || cancelled) return

        const blob = await response.blob()
        objectUrl = URL.createObjectURL(blob)
        if (cancelled) {
          URL.revokeObjectURL(objectUrl)
          return
        }
        setFrameSrc((prev) => {
          if (prev) URL.revokeObjectURL(prev)
          return objectUrl
        })
      } catch (error) {
        console.error('Load camera frame failed', error)
      }
    }

    loadFrame()

    return () => {
      cancelled = true
      if (objectUrl) URL.revokeObjectURL(objectUrl)
    }
  }, [camera.id, isOnline, frameTick])

  return (
    <div
      className={`camera-feed camera-feed--${size} camera-feed--${camera.status}`}
    >
      {isOnline ? (
        <>
          {frameSrc ? (
            <img
              src={frameSrc}
              alt={camera.name}
              className="camera-feed__image"
            />
          ) : null}

          {children ? (
            <div className="camera-feed__overlay-layer">
              {children}
            </div>
          ) : null}

          <div className="camera-feed__top">
            <span className="live-pill">
              <span className="live-pill__dot" />
              LIVE
            </span>

            <span className="camera-feed__resolution">
              {camera.resolution}
            </span>
          </div>

          <span className="camera-feed__time">
            {new Date().toLocaleTimeString('vi-VN')}
          </span>
        </>
      ) : (
        <div className="camera-feed__offline">
          <Camera size={48} />
          <span>OFFLINE</span>
        </div>
      )}

      {size === 'large' && isOnline && (
        <div className="camera-feed__bottom">
          <span>{camera.name}</span>

          <span>
            <Radio size={14} />
            {' '}
            {camera.fps} FPS
          </span>
        </div>
      )}
    </div>
  )
}

export default CameraFeed
