import { Link } from 'react-router-dom'
import { AlertTriangle } from 'lucide-react'
import { CAMERA_LIFECYCLE } from '../../utils/cameraLifecycle'

function CameraAtshStatusBanner({
  cameraId,
  lifecycle,
  loading = false,
  canManage = false,
  compact = false,
}) {
  if (loading || !lifecycle) return null

  if (lifecycle === CAMERA_LIFECYCLE.NEW) {
    return (
      <div className="camera-atsh-status camera-atsh-status--new-large" role="alert">
        <div className="camera-atsh-status__icon" aria-hidden="true">
          <AlertTriangle size={28} />
        </div>
        <div className="camera-atsh-status__content">
          <strong>Camera chưa được thiết kế vùng an toàn sinh học.</strong>
          <p>
            Để đưa Camera vào vận hành, hãy hoàn tất thiết kế vùng ATSH.
          </p>
          <p className="camera-atsh-status__hint">
            Trạng thái NEW: chỉ xem Live, kiểm tra RTSP/Online. AI, Rule Engine, Notification và Dashboard Analytics chưa hoạt động.
          </p>
        </div>
        {canManage && cameraId ? (
          <Link
            className="btn btn--primary"
            to={`/thiet-ke-vung-atsh?camera=${encodeURIComponent(cameraId)}`}
          >
            Thiết kế ngay
          </Link>
        ) : null}
      </div>
    )
  }

  if (lifecycle === CAMERA_LIFECYCLE.CONFIGURING) {
    return (
      <div className="camera-atsh-status camera-atsh-status--configuring" role="status">
        <div>
          <strong>Đang cấu hình vùng ATSH (CONFIGURING)</strong>
          <p>
            AI và Rule Engine vẫn dùng vùng đã lưu gần nhất. Chỉ khi nhấn Lưu, dữ liệu mới được publish.
          </p>
        </div>
        {canManage && cameraId ? (
          <Link
            className="btn btn--outline btn--sm"
            to={`/thiet-ke-vung-atsh?camera=${encodeURIComponent(cameraId)}`}
          >
            Tiếp tục thiết kế
          </Link>
        ) : null}
      </div>
    )
  }

  if (lifecycle === CAMERA_LIFECYCLE.PAUSED) {
    return (
      <div className="camera-atsh-status camera-atsh-status--paused" role="status">
        <strong>Camera tạm dừng (PAUSED)</strong>
        <p>Giám sát AI và Rule Engine đã tắt. Live view vẫn khả dụng.</p>
      </div>
    )
  }

  const isMonitoring = lifecycle === CAMERA_LIFECYCLE.MONITORING

  return (
    <div
      className={`camera-atsh-status camera-atsh-status--${isMonitoring ? 'monitoring' : 'ready'}${compact ? ' camera-atsh-status--compact' : ''}`}
      role="status"
    >
      <div>
        <strong>{isMonitoring ? 'Đang giám sát (MONITORING)' : 'Sẵn sàng giám sát (READY)'}</strong>
        <p>
          Camera Live, AI Engine và Rule Engine dùng cùng dữ liệu vùng ATSH đã publish — không cần tải lại trang.
        </p>
      </div>
    </div>
  )
}

export default CameraAtshStatusBanner
