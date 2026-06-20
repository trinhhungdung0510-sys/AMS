import { useEffect, useRef, useState } from 'react'
import { subscribeWsEvents } from '../services/wsClient'

export function useRealtimeEvents({ onMessage, filterCameraId = null, eventTypes = null } = {}) {
  const [connected, setConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)
  const onMessageRef = useRef(onMessage)
  onMessageRef.current = onMessage

  useEffect(() => {
    const unsubscribe = subscribeWsEvents({
      onConnect: () => setConnected(true),
      onDisconnect: () => setConnected(false),
      onMessage: (payload) => {
        if (eventTypes && !eventTypes.includes(payload.type)) return

        const data = payload.payload || payload
        const cameraId = data?.event?.camera_id
          || data?.observation?.camera_id
          || data?.track?.cameraId
          || data?.cameraId

        if (filterCameraId && cameraId && cameraId !== filterCameraId) return

        setLastMessage(payload)
        onMessageRef.current?.(payload)
      },
    })

    return unsubscribe
  }, [filterCameraId, eventTypes])

  return { connected, lastMessage }
}
