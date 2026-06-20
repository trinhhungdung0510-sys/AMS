import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { useEventStore } from '../context/EventStore'

const NotificationContext = createContext(null)
const TOAST_TTL_MS = 8000

function buildEventToast(event) {
  return {
    id: event.id || `evt-${Date.now()}`,
    tone: (event.severityRaw || event.severity || 'MEDIUM').toLowerCase(),
    title: event.typeLabel || event.eventType || 'Sự kiện',
    message: `${event.zoneName || event.zoneId || event.cameraId || 'Zone'} · ${event.cameraName || event.cameraId || ''}`.trim(),
  }
}

function buildNotificationToast(notification) {
  return {
    id: notification.eventId || notification.id || `ntf-${Date.now()}`,
    tone: (notification.severity || 'MEDIUM').toLowerCase(),
    title: notification.eventType || notification.type || 'Thông báo',
    message: notification.message || 'Có sự kiện mới từ hệ thống AI',
  }
}

export function NotificationProvider({ children }) {
  const { lastWsEvent, lastNotification } = useEventStore()
  const [toasts, setToasts] = useState([])
  const seenToastIds = useRef(new Set())

  const pushToast = useCallback((toast) => {
    if (seenToastIds.current.has(toast.id)) return
    seenToastIds.current.add(toast.id)

    setToasts((current) => [toast, ...current.filter((item) => item.id !== toast.id)].slice(0, 5))
    setTimeout(() => {
      setToasts((current) => current.filter((item) => item.id !== toast.id))
    }, TOAST_TTL_MS)
  }, [])

  const notify = useCallback((payload) => {
    console.info('[AMS Notification]', payload)
  }, [])

  useEffect(() => {
    if (!lastWsEvent?.id) return
    const toast = buildEventToast(lastWsEvent)
    pushToast(toast)
    notify({ type: 'event_created', ...lastWsEvent, message: toast.message })
  }, [lastWsEvent, notify, pushToast])

  useEffect(() => {
    if (!lastNotification) return
    const toast = buildNotificationToast(lastNotification)
    pushToast(toast)
    notify({ type: 'notification_created', ...lastNotification })
  }, [lastNotification, notify, pushToast])

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
