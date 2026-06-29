import { useEffect, useState } from 'react'
import { AlertTriangle } from 'lucide-react'
import { useEventStore } from '../../context/EventStore'
import { getNotificationSettings } from '../../services/notificationSettingsService'

function formatSentAt(value) {
  if (!value) return null
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('vi-VN')
}

export default function GmailDeliveryAlert() {
  const { lastGmailFailure } = useEventStore()
  const [settingsFailure, setSettingsFailure] = useState(null)

  useEffect(() => {
    let active = true
    getNotificationSettings()
      .then((settings) => {
        if (!active) return
        if (settings.gmail_last_status === 'failed') {
          setSettingsFailure({
            message: settings.gmail_last_error || 'Gửi Email thất bại',
            sentAt: settings.gmail_last_sent_at,
          })
        } else {
          setSettingsFailure(null)
        }
      })
      .catch(() => {})
    return () => {
      active = false
    }
  }, [lastGmailFailure])

  const failure = lastGmailFailure || settingsFailure
  if (!failure) return null

  return (
    <div className="gmail-delivery-alert" role="alert">
      <AlertTriangle size={18} />
      <div>
        <strong>Gửi Email thất bại</strong>
        <span>{failure.message}</span>
        {failure.sentAt ? <small>Lần gửi cuối: {formatSentAt(failure.sentAt)}</small> : null}
      </div>
    </div>
  )
}
