import { Camera, RefreshCw } from 'lucide-react'
import { resolveSnapshotAssetUrl } from '../../services/cameraSnapshotService'

function CameraSnapshotCard({
  snapshotUrl,
  capturedAt,
  loading,
  capturing,
  error,
  onCapture,
  onRefresh,
}) {
  const imageUrl = snapshotUrl ? `${resolveSnapshotAssetUrl(snapshotUrl)}?t=${encodeURIComponent(capturedAt || Date.now())}` : ''

  return (
    <section className="panel camera-snapshot-card">
      <div className="panel__header">
        <div>
          <h2 className="panel__title">Snapshot thực tế</h2>
          <p className="panel__desc">Ảnh chụp từ luồng RTSP qua ffmpeg</p>
        </div>
        <div className="camera-snapshot-card__actions">
          <button
            type="button"
            className="btn btn--outline"
            onClick={onRefresh}
            disabled={loading || capturing}
          >
            <RefreshCw size={15} />
            Refresh
          </button>
          <button
            type="button"
            className="btn btn--primary"
            onClick={onCapture}
            disabled={loading || capturing}
          >
            <Camera size={15} />
            {capturing ? 'Đang chụp...' : 'Capture Snapshot'}
          </button>
        </div>
      </div>

      {error ? <div className="camera-snapshot-card__error">{error}</div> : null}

      <div className="camera-snapshot-card__preview">
        {loading || capturing ? (
          <div className="camera-snapshot-card__loading">Đang tải snapshot...</div>
        ) : null}

        {!loading && !capturing && imageUrl ? (
          <img
            src={imageUrl}
            alt="Camera snapshot"
            className="camera-snapshot-card__image"
          />
        ) : null}

        {!loading && !capturing && !imageUrl ? (
          <div className="camera-snapshot-card__empty">Chưa có snapshot — bấm Capture Snapshot để chụp.</div>
        ) : null}
      </div>

      {capturedAt ? (
        <p className="camera-snapshot-card__meta">Thời gian chụp: {capturedAt.replace('T', ' ').slice(0, 19)} UTC</p>
      ) : null}
    </section>
  )
}

export default CameraSnapshotCard
