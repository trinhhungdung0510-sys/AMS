import { createContext, useCallback, useContext, useMemo } from 'react'

const NotificationContext = createContext(null)

const CHANNELS = ['console', 'email', 'telegram', 'zalo', 'push']

function logNotification(channel, payload) {
  if (channel !== 'console') return
  console.info('[AMS Notification]', payload)
}

export function NotificationProvider({ children }) {
  const notify = useCallback((payload) => {
    CHANNELS.forEach((channel) => logNotification(channel, payload))
  }, [])

  const value = useMemo(() => ({ notify }), [notify])

  return (
    <NotificationContext.Provider value={value}>
      {children}
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
