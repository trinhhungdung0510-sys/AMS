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
  const isViolationAlert = notification.type === 'violation_alert'
  return {
    id: notification.eventId || notification.id || `ntf-${Date.now()}`,
    tone: (notification.severity || 'MEDIUM').toLowerCase(),
    title: notification.title || (isViolationAlert ? '🚨 CẢNH BÁO VI PHẠM AN TOÀN SINH HỌC' : notification.eventType || notification.type || 'Thông báo'),
    message: isViolationAlert
      ? `${notification.zoneName || 'Khu vực'} · ${notification.cameraName || 'Camera'} · ${notification.ruleName || 'Vi phạm ATSH'}`
      : (notification.message || 'Có sự kiện mới từ hệ thống AI'),
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

  const showViolationAlert = useCallback((notification, { force = false } = {}) => {
    if (!notification) return
    const toast = buildNotificationToast(notification)
    if (force) {
      toast.id = `${toast.id}-${Date.now()}`
    }
    pushToast(toast)
  }, [pushToast])

  useEffect(() => {
    if (!lastWsEvent?.id) return
    const statusKey = String(lastWsEvent.statusRaw || lastWsEvent.status || '').toUpperCase()
    if (statusKey === 'RESOLVED' || statusKey === 'DISMISSED') return
    const toast = buildEventToast(lastWsEvent)
    pushToast(toast)
  }, [lastWsEvent, pushToast])

  useEffect(() => {
    if (!lastNotification) return
    const toast = buildNotificationToast(lastNotification)
    pushToast(toast)
  }, [lastNotification, pushToast])

  const dismissToast = useCallback((id) => {
    setToasts((current) => current.filter((item) => item.id !== id))
  }, [])

  const value = useMemo(() => ({ showViolationAlert }), [showViolationAlert])

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

export function notifyEventCreated(_event) {
  // Realtime notifications are delivered through WebSocket (event.created / notification.created).
}
