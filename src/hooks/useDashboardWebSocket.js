import { useEffect, useRef, useState } from 'react'
import { getWebSocketBaseUrl } from '../config/api'

const WS_URL = `${getWebSocketBaseUrl()}/ws/dashboard`

export function useDashboardWebSocket(onMessage) {
  const [connected, setConnected] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(null)
  const onMessageRef = useRef(onMessage)
  onMessageRef.current = onMessage

  useEffect(() => {
    let socket
    let retryTimer

    const connect = () => {
      try {
        socket = new WebSocket(WS_URL)
      } catch {
        setConnected(false)
        retryTimer = setTimeout(connect, 5000)
        return
      }

      socket.onopen = () => {
        setConnected(true)
        setLastUpdate(new Date())
      }

      socket.onmessage = (event) => {
        setLastUpdate(new Date())
        try {
          const payload = JSON.parse(event.data)
          onMessageRef.current?.(payload)
        } catch {
          // ignore malformed payloads
        }
      }

      socket.onclose = () => {
        setConnected(false)
        retryTimer = setTimeout(connect, 5000)
      }

      socket.onerror = () => {
        setConnected(false)
        socket.close()
      }
    }

    connect()

    return () => {
      clearTimeout(retryTimer)
      if (socket) socket.close()
    }
  }, [])

  return { connected, lastUpdate }
}
