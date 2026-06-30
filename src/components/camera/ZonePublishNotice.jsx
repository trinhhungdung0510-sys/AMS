import { useEffect, useState } from 'react'
import { CheckCircle2 } from 'lucide-react'
import { ZONE_PUBLISHED_EVENT, ZONE_PUBLISH_SUCCESS_MESSAGE } from '../../services/zonePublishService'

function ZonePublishNotice({ cameraId }) {
  const [message, setMessage] = useState('')

  useEffect(() => {
    const handlePublished = (event) => {
      const publishedCameraId = event.detail?.cameraId
      if (publishedCameraId && publishedCameraId !== cameraId) return
      setMessage(event.detail?.message || ZONE_PUBLISH_SUCCESS_MESSAGE)
    }

    window.addEventListener(ZONE_PUBLISHED_EVENT, handlePublished)
    return () => window.removeEventListener(ZONE_PUBLISHED_EVENT, handlePublished)
  }, [cameraId])

  useEffect(() => {
    if (!message) return undefined
    const timer = setTimeout(() => setMessage(''), 8000)
    return () => clearTimeout(timer)
  }, [message])

  if (!message) return null

  return (
    <div className="zone-publish-notice" role="status">
      <CheckCircle2 size={18} />
      <span>{message}</span>
    </div>
  )
}

export default ZonePublishNotice
