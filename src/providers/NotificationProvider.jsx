import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { subscribeWsEvents } from '../services/wsClient'

const NotificationContext = createContext(null)
const TOAST_TTL_MS = 8000

function buildEventToast(event) {
  return {
    id: event.id || `evt-${Date.now()}`,
    tone: (event.severity || 'MEDIUM').toLowerCase(),
    title: event.event_type || event.alert_type || 'Sự kiện',
    message: `${event.zone_name || event.zone_id || event.camera_id || 'Zone'} · ${event.camera_name || event.camera_id || ''}`.trim(),
  }
}

function buildNotificationToast(notification) {
  return {
    id: notification.eventId || `ntf-${Date.now()}`,
    tone: (notification.severity || 'MEDIUM').toLowerCase(),
    title: notification.eventType || notification.type || 'Thông báo',
    message: notification.message || 'Có sự kiện mới từ hệ thống AI',
  }
}

export function NotificationProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const pushToast = useCallback((toast) => {
    setToasts((current) => [toast, ...current.filter((item) => item.id !== toast.id)].slice(0, 5))
    setTimeout(() => {
      setToasts((current) => current.filter((item) => item.id !== toast.id))
    }, TOAST_TTL_MS)
  }, [])

  const notify = useCallback((payload) => {
    console.info('[AMS Notification]', payload)
  }, [])

  useEffect(() => {
    return subscribeWsEvents({
      onMessage: (payload) => {
        if (payload.type === 'event.created') {
          const event = payload.payload?.event
          if (!event) return
          const toast = buildEventToast(event)
          pushToast(toast)
          notify({ type: 'event_created', ...event, message: toast.message })
          return
        }

        if (payload.type === 'notification.created') {
          const notification = payload.payload?.notification
          if (!notification) return
          const toast = buildNotificationToast(notification)
          pushToast(toast)
          notify({ type: 'notification_created', ...notification })
        }
      },
    })
  }, [notify, pushToast])

  const dismissToast = useCallback((id) => {
    setToasts((current) => current.filter((item) => item.id !== id))
  }, [])

  const value = useMemo(() => ({ notify }), [notify])

  return (
    <NotificationContext.Provider value={value}>
      {children}
      <div className="ams-toast-stack" aria-live="polite">
        {toasts.map((toast) => (
          <button
            key={toast.id}
            type="button"
            className={`ams-toast ams-toast--${toast.tone}`}
            onClick={() => dismissToast(toast.id)}
          >
            <strong>{toast.title}</strong>
            <span>{toast.message}</span>
          </button>
        ))}
      </div>
    </NotificationContext.Provider>
  )
}

export function useNotifications() {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider')
  }
  return context
}

export function notifyEventCreated(event) {
  const payload = {
    type: 'event_created',
    eventId: event.id,
    cameraId: event.camera_id,
    zoneId: event.zone_id,
    ruleId: event.rule_id,
    eventType: event.event_type,
    severity: event.severity,
    status: event.status,
    confidence: event.confidence,
    message: `[${event.severity}] ${event.event_type} — ${event.zone_name || event.zone_id}`,
  }

  console.info('[AMS Notification] Event created', payload)
}
