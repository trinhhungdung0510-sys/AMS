import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Camera, Shapes } from 'lucide-react'
import CameraLiveWithZones from '../camera/CameraLiveWithZones'
import CameraAtshStatusBanner from '../camera/CameraAtshStatusBanner'
import { usePermissions } from '../../hooks/usePermissions'
import { useCameraZoneReadiness } from '../../hooks/useCameraZoneReadiness'
import { getLifecycleCapabilities, resolveCameraLifecycle } from '../../utils/cameraLifecycle'
import { cameras as fallbackCameras } from '../../data/mockData'

function normalizeCamera(camera) {
  if (!camera?.id) return null
  return {
    id: camera.id,
    name: camera.name || camera.ten_camera || camera.id,
    status: String(camera.status || 'offline').toLowerCase(),
    resolution: camera.resolution || '1080p',
    fps: camera.fps || 25,
  }
}

function DashboardLiveFeed({ camera }) {
  const normalized = normalizeCamera(camera)
  const { canManageAtshZones } = usePermissions()
  const { zones, loading: zonesLoading } = useCameraZoneReadiness(normalized?.id)

  const lifecycle = useMemo(
    () => resolveCameraLifecycle({ camera: normalized, publishedZones: zones }),
    [normalized, zones],
  )

  const capabilities = useMemo(
    () => getLifecycleCapabilities(lifecycle, zones),
    [lifecycle, zones],
  )

  if (!normalized) return null

  const showZoneEmpty = !capabilities.zoneOverlay && !zonesLoading

  return (
    <div className="dashboard-live__pane">
      <div className="dashboard-live__viewport">
        <CameraLiveWithZones camera={normalized} size="large" />
        {showZoneEmpty ? (
          <div className="dashboard-live__zone-empty">
            <Shapes size={22} />
            <p>Chưa thiết kế vùng ATSH</p>
            {canManageAtshZones ? (
              <Link
                className="btn btn--primary btn--sm"
                to={`/thiet-ke-vung-atsh?camera=${encodeURIComponent(normalized.id)}`}
              >
                Thiết kế ngay
              </Link>
            ) : null}
          </div>
        ) : null}
      </div>
      {!showZoneEmpty ? (
        <CameraAtshStatusBanner
          cameraId={normalized.id}
          lifecycle={lifecycle}
          loading={zonesLoading}
          canManage={canManageAtshZones}
          compact
        />
      ) : null}
    </div>
  )
}

function DashboardLiveSection({ cameras = null, title = 'Camera giám sát trực tiếp' }) {
  const list = useMemo(() => {
    const source = Array.isArray(cameras) && cameras.length > 0 ? cameras : fallbackCameras
    return source.map(normalizeCamera).filter(Boolean).slice(0, 6)
  }, [cameras])

  const [selectedId, setSelectedId] = useState(null)
  const activeId = list.some((camera) => camera.id === selectedId) ? selectedId : list[0]?.id
  const activeCamera = list.find((camera) => camera.id === activeId) ?? list[0]

  if (list.length === 0) {
    return (
      <section className="panel dashboard-live dashboard-live--empty">
        <div className="panel__header">
          <div>
            <h2>{title}</h2>
            <p>Chưa có camera trong hệ thống</p>
          </div>
        </div>
        <div className="dashboard-live__empty-state">
          <Camera size={32} />
          <p>Thêm camera trong Cài đặt để bắt đầu giám sát.</p>
        </div>
      </section>
    )
  }

  return (
    <section className="panel dashboard-live">
      <div className="panel__header">
        <div>
          <h2>{title}</h2>
          <p>Chọn camera để xem live và overlay vùng ATSH</p>
        </div>
      </div>

      <div className="dashboard-live__picker" role="tablist" aria-label="Chọn camera">
        {list.map((camera) => (
          <button
            key={camera.id}
            type="button"
            role="tab"
            aria-selected={camera.id === activeId}
            className={`dashboard-live__tab${camera.id === activeId ? ' dashboard-live__tab--active' : ''}`}
            onClick={() => setSelectedId(camera.id)}
          >
            {camera.name}
          </button>
        ))}
      </div>

      <div className="dashboard-live__feeds">
        {activeCamera ? <DashboardLiveFeed key={activeCamera.id} camera={activeCamera} /> : null}
      </div>
    </section>
  )
}

export default DashboardLiveSection
