import { useEffect, useMemo, useState } from 'react'
import { Mail, Send, ShieldCheck, SlidersHorizontal, Users } from 'lucide-react'
import { Link } from 'react-router-dom'
import CameraFormPanel from '../components/camera/CameraFormPanel'
import { alertSettings, severityLabels } from '../data/mockData'
import { getFarms } from '../services/farmService'
import { getSystemSettings, updateSystemSettings, createSystemBackup } from '../services/systemSettingsService'
import { fetchDemoStatus, startDemoMode, stopDemoMode } from '../services/demoService'
import { listUsers } from '../services/userService'
import {
  EMPTY_CAMERA_FORM,
  buildCameraPayload,
  cameraToFormValues,
  createCamera,
  deleteCamera,
  getCameraIp,
  getCameras,
  updateCamera,
  validateCameraForm,
} from '../services/cameraService'

function SettingsPage() {
  const [cameras, setCameras] = useState([])
  const [farms, setFarms] = useState([{ id: 'FARM-001', name: 'AMS Farm Long An' }])
  const [loading, setLoading] = useState(true)
  const [formMode, setFormMode] = useState(null)
  const [editingCamera, setEditingCamera] = useState(null)
  const [statusMessage, setStatusMessage] = useState('')
  const [systemSettings, setSystemSettings] = useState(null)
  const [demoStatus, setDemoStatus] = useState(null)
  const [managedUsers, setManagedUsers] = useState([])

  const formInitialValues = useMemo(() => {
    if (formMode === 'edit') return cameraToFormValues(editingCamera)
    return { ...EMPTY_CAMERA_FORM }
  }, [editingCamera, formMode])

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [cameraData, farmData, settingsData, usersData, demoData] = await Promise.all([
        getCameras(),
        getFarms().catch(() => []),
        getSystemSettings().catch(() => null),
        listUsers().catch(() => []),
        fetchDemoStatus().catch(() => null),
      ])
      setCameras(cameraData)
      setSystemSettings(settingsData)
      setDemoStatus(demoData)
      setManagedUsers(usersData)
      if (farmData.length) {
        setFarms(farmData.map((farm) => ({ id: farm.id, name: farm.name })))
      }
    } catch (error) {
      setStatusMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  const openCreateForm = () => {
    setEditingCamera(null)
    setFormMode('create')
    setStatusMessage('')
  }

  const openEditForm = (camera) => {
    setEditingCamera(camera)
    setFormMode('edit')
    setStatusMessage('')
  }

  const closeForm = () => {
    setFormMode(null)
    setEditingCamera(null)
  }

  const handleCreate = async (values, setErrors) => {
    const validationErrors = validateCameraForm(values)
    if (Object.keys(validationErrors).length) {
      setErrors(validationErrors)
      return
    }

    try {
      const created = await createCamera(buildCameraPayload(values))
      setCameras((prev) => [...prev, created])
      setStatusMessage(`Đã thêm ${created.name}`)
      closeForm()
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const handleUpdate = async (values, setErrors) => {
    const validationErrors = validateCameraForm(values, { isEdit: true })
    if (Object.keys(validationErrors).length) {
      setErrors(validationErrors)
      return
    }

    try {
      const updated = await updateCamera(
        editingCamera.id,
        buildCameraPayload(values, { isEdit: true }),
      )
      setCameras((prev) => prev.map((camera) => (camera.id === updated.id ? updated : camera)))
      setStatusMessage(`Đã cập nhật ${updated.name}`)
      closeForm()
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const handleDelete = async (camera) => {
    if (!window.confirm(`Xóa camera ${camera.name}?`)) return

    try {
      await deleteCamera(camera.id)
      setCameras((prev) => prev.filter((item) => item.id !== camera.id))
      setStatusMessage(`Đã xóa ${camera.name}`)
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const toggleActive = async (camera) => {
    try {
      const updated = await updateCamera(camera.id, { is_active: !camera.is_active })
      setCameras((prev) => prev.map((item) => (item.id === updated.id ? updated : item)))
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const handleSaveSystemSettings = async () => {
    if (!systemSettings) return
    try {
      const saved = await updateSystemSettings(systemSettings)
      setSystemSettings(saved)
      setStatusMessage('Đã lưu cấu hình hệ thống')
      const status = await fetchDemoStatus().catch(() => null)
      setDemoStatus(status)
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const handleStartDemo = async () => {
    try {
      const result = await startDemoMode()
      setDemoStatus(await fetchDemoStatus())
      setStatusMessage(`Demo stream đang chạy · Compliance ${result.complianceScore}%`)
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const handleStopDemo = async () => {
    try {
      await stopDemoMode()
      setDemoStatus(await fetchDemoStatus())
      setStatusMessage('Đã dừng demo stream')
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  const handleCreateBackup = async () => {
    try {
      const backup = await createSystemBackup()
      const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `ams-backup-${new Date().toISOString().slice(0, 10)}.json`
      link.click()
      URL.revokeObjectURL(url)
      setStatusMessage('Đã xuất backup JSON')
    } catch (error) {
      setStatusMessage(error.message)
    }
  }

  return (
    <div className="settings-page">
      <div className="settings-grid">
        <section className="panel">
          <div className="panel__header">
            <div>
              <h2><Users size={18} /> Danh sách người dùng</h2>
              <p>5 người dùng mẫu và trạng thái tài khoản</p>
            </div>
          </div>
          <div className="settings-list">
            {(managedUsers.length ? managedUsers : []).map((user) => (
              <div key={user.id} className="settings-list__item">
                <div>
                  <strong>{user.full_name}</strong>
                  <span>{user.email} · {user.role}</span>
                </div>
                <span className={`status-tag status-tag--${user.is_active ? 'resolved' : 'new'}`}>
                  {user.is_active ? 'Hoạt động' : 'Tạm khóa'}
                </span>
              </div>
            ))}
            {!managedUsers.length ? (
              <p className="panel__meta">Chưa tải được danh sách user từ API.</p>
            ) : null}
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2><ShieldCheck size={18} /> Phân quyền</h2>
              <p>Vai trò và phạm vi truy cập</p>
            </div>
          </div>
          <div className="role-grid">
            {[
              ['SUPER_ADMIN', 'Quản lý toàn bộ hệ thống'],
              ['FARM_ADMIN', 'Quản lý farm được gán'],
              ['VIEWER', 'Chỉ xem dữ liệu'],
            ].map(([role, desc]) => (
              <div key={role} className="role-card">
                <strong>{role}</strong>
                <span>{desc}</span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="settings-sections">
        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title"><SlidersHorizontal size={18} /> Cấu hình hệ thống</h2>
              <p className="panel__desc">Compliance threshold, workflow timeout, demo mode, retention</p>
            </div>
          </div>
          {systemSettings ? (
            <div className="settings-form">
              <label className="settings-form__label">
                <span>Ngưỡng tuân thủ (0-1)</span>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  className="settings-form__input"
                  value={systemSettings.compliance_threshold}
                  onChange={(event) =>
                    setSystemSettings((prev) => ({
                      ...prev,
                      compliance_threshold: Number(event.target.value),
                    }))
                  }
                />
              </label>
              <label className="settings-form__label">
                <span>Workflow timeout (giây)</span>
                <input
                  type="number"
                  min="30"
                  className="settings-form__input"
                  value={systemSettings.workflow_timeout}
                  onChange={(event) =>
                    setSystemSettings((prev) => ({
                      ...prev,
                      workflow_timeout: Number(event.target.value),
                    }))
                  }
                />
              </label>
              <label className="settings-form__label">
                <span>Retention (ngày)</span>
                <input
                  type="number"
                  min="1"
                  className="settings-form__input"
                  value={systemSettings.retention_days}
                  onChange={(event) =>
                    setSystemSettings((prev) => ({
                      ...prev,
                      retention_days: Number(event.target.value),
                    }))
                  }
                />
              </label>
              <label className="settings-form__label settings-form__label--inline">
                <span>Demo mode</span>
                <label className="toggle">
                  <input
                    type="checkbox"
                    checked={Boolean(systemSettings.demo_mode)}
                    onChange={(event) =>
                      setSystemSettings((prev) => ({
                        ...prev,
                        demo_mode: event.target.checked,
                      }))
                    }
                  />
                  <span className="toggle__slider" />
                </label>
              </label>
              {demoStatus ? (
                <div className="settings-form__demo-panel">
                  <p className="panel__meta">
                    Stream: {demoStatus.running ? 'Đang chạy' : 'Dừng'} · Events: {demoStatus.eventsGenerated ?? 0} ·
                    Compliance: {demoStatus.complianceScore ?? '—'}%
                  </p>
                  <div className="settings-form__actions">
                    <button type="button" className="btn btn--outline" onClick={handleStopDemo} disabled={!demoStatus.running}>
                      Dừng Demo
                    </button>
                    <button type="button" className="btn btn--primary" onClick={handleStartDemo} disabled={!systemSettings.demo_mode}>
                      Bắt đầu Demo
                    </button>
                  </div>
                </div>
              ) : null}
              <div className="settings-form__actions">
                <button type="button" className="btn btn--outline" onClick={handleCreateBackup}>
                  Xuất backup JSON
                </button>
                <button type="button" className="btn btn--primary" onClick={handleSaveSystemSettings}>
                  Lưu cấu hình
                </button>
              </div>
            </div>
          ) : (
            <p className="panel__meta">Không tải được cấu hình hệ thống.</p>
          )}
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Quản lý camera</h2>
              <p className="panel__desc">Thêm, sửa và cấu hình camera IP thực trong hệ thống AMS</p>
              {statusMessage ? <p className="panel__meta">{statusMessage}</p> : null}
            </div>
            <button type="button" className="btn btn--primary" onClick={openCreateForm}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              Thêm camera
            </button>
            <Link to="/thiet-ke-vung-atsh" className="btn btn--outline">
              Thiết kế vùng ATSH
            </Link>
          </div>

          {loading ? (
            <div className="violation-empty">Đang tải danh sách camera...</div>
          ) : (
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Mã</th>
                    <th>Tên camera</th>
                    <th>Hãng</th>
                    <th>Khu vực</th>
                    <th>IP</th>
                    <th>Port</th>
                    <th>Độ phân giải</th>
                    <th>FPS</th>
                    <th>Trạng thái</th>
                    <th>Kích hoạt</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {cameras.map((camera) => (
                    <tr key={camera.id}>
                      <td className="data-table__mono">{camera.id}</td>
                      <td className="data-table__desc">{camera.name}</td>
                      <td>{camera.manufacturer || '—'}</td>
                      <td>{camera.zone}</td>
                      <td className="data-table__mono">{getCameraIp(camera)}</td>
                      <td>{camera.port ?? 554}</td>
                      <td>{camera.resolution}</td>
                      <td>{camera.fps}</td>
                      <td>
                        <span className={`status-pill status-pill--${camera.status}`}>
                          {camera.status === 'online' ? 'Online' : 'Offline'}
                        </span>
                      </td>
                      <td>
                        <label className="toggle">
                          <input
                            type="checkbox"
                            checked={camera.is_active}
                            onChange={() => toggleActive(camera)}
                          />
                          <span className="toggle__slider" />
                        </label>
                      </td>
                      <td>
                        <div className="action-group">
                          <button
                            type="button"
                            className="btn-icon"
                            aria-label="Chỉnh sửa"
                            onClick={() => openEditForm(camera)}
                          >
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                            </svg>
                          </button>
                          <button
                            type="button"
                            className="btn-icon btn-icon--danger"
                            aria-label="Xóa"
                            onClick={() => handleDelete(camera)}
                          >
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <polyline points="3 6 5 6 21 6" />
                              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                            </svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title"><SlidersHorizontal size={18} /> Thiết lập cảnh báo</h2>
              <p className="panel__desc">Bật/tắt và ngưỡng tin cậy AI theo từng loại cảnh báo</p>
            </div>
          </div>
          <div className="settings-list">
            {alertSettings.map((setting) => (
              <div key={setting.id} className="settings-list__item">
                <div>
                  <strong>{setting.name}</strong>
                  <span>Ngưỡng: {setting.threshold} · Mức độ: {severityLabels[setting.severity]}</span>
                </div>
                <label className="toggle">
                  <input type="checkbox" defaultChecked={setting.enabled} />
                  <span className="toggle__slider" />
                </label>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Kênh nhận cảnh báo</h2>
              <p className="panel__desc">Email và Telegram nhận cảnh báo AI tức thời</p>
            </div>
          </div>
          <div className="settings-form">
            <label className="settings-form__label">
              <span><Mail size={15} /> Email nhận cảnh báo</span>
              <input type="email" className="settings-form__input" defaultValue="ops@ams-farm.vn" />
            </label>
            <label className="settings-form__label">
              <span><Send size={15} /> Telegram nhận cảnh báo</span>
              <input type="text" className="settings-form__input" defaultValue="@ams_farm_alerts" />
            </label>
            <div className="settings-form__actions">
              <button type="button" className="btn btn--outline">Gửi thử</button>
              <button type="button" className="btn btn--primary">Lưu cấu hình</button>
            </div>
          </div>
        </section>
      </div>

      {formMode === 'create' ? (
        <CameraFormPanel
          title="Thêm camera"
          submitLabel="Thêm camera"
          initialValues={formInitialValues}
          farms={farms}
          onSubmit={handleCreate}
          onCancel={closeForm}
        />
      ) : null}

      {formMode === 'edit' ? (
        <CameraFormPanel
          title={`Sửa camera · ${editingCamera?.name || ''}`}
          submitLabel="Lưu thay đổi"
          initialValues={formInitialValues}
          farms={farms}
          isEdit
          onSubmit={handleUpdate}
          onCancel={closeForm}
        />
      ) : null}
    </div>
  )
}

export default SettingsPage
