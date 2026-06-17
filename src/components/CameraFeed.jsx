import { Camera, Maximize2, Radio, Video } from 'lucide-react'

function CameraFeed({ camera, size = 'tile', showActions = false }) {
  const isOnline = camera.status === 'online'

  return (
    <div className={`camera-feed camera-feed--${size} camera-feed--${camera.status}`}>
      <div className="camera-feed__scanline" />
      <div className="camera-feed__noise" />

      {isOnline ? (
        <>
          <div className="camera-feed__top">
            <span className="live-pill">
              <span className="live-pill__dot" />
              LIVE
            </span>
            <span className="camera-feed__resolution">{camera.resolution}</span>
          </div>
          <span className="camera-feed__time">{new Date().toLocaleTimeString('vi-VN')}</span>
          <Camera className="camera-feed__watermark" size={size === 'large' ? 72 : 44} />
        </>
      ) : (
        <div className="camera-feed__offline">
          <Camera size={size === 'large' ? 56 : 36} />
          <span>OFFLINE</span>
        </div>
      )}

      {showActions && (
        <div className="camera-feed__actions">
          <button type="button" className="icon-btn icon-btn--dark" aria-label="Toàn màn hình">
            <Maximize2 size={18} />
          </button>
          <button type="button" className="icon-btn icon-btn--dark" aria-label="Chụp ảnh hiện tại">
            <Camera size={18} />
          </button>
          <button type="button" className="icon-btn icon-btn--record" aria-label="Ghi hình">
            <Video size={18} />
          </button>
        </div>
      )}

      {size === 'large' && isOnline && (
        <div className="camera-feed__bottom">
          <span>{camera.name}</span>
          <span>
            <Radio size={14} /> {camera.fps} FPS
          </span>
        </div>
      )}
    </div>
  )
}

export default CameraFeed
