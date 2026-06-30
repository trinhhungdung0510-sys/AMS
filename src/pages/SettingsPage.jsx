import { useEffect, useMemo, useRef, useState } from 'react'
import { Activity, CheckCircle2, Mail, MessageCircle, Rocket, ShieldCheck, SlidersHorizontal, Stethoscope, X } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import CameraFormPanel from '../components/camera/CameraFormPanel'
import UserManagementPanel from '../components/settings/UserManagementPanel'
import { alertSettings, severityLabels } from '../data/mockData'
import { getFarms } from '../services/farmService'
import { getSystemSettings, updateSystemSettings, createSystemBackup } from '../services/systemSettingsService'
import { fetchDemoStatus, startDemoMode, stopDemoMode } from '../services/demoService'
import { listUsers } from '../services/userService'
import {
  connectGmailNotification,
  getNotificationSettings,
  pollZaloConnect,
  startZaloConnect,
  testGmailNotification,
  verifyGmailNotification,
  updateNotificationSettings,
} from '../services/notificationSettingsService'
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
import { loadCameraZones } from '../services/cameraZoneOverlayService'
import { NEW_CAMERA_ZONE_MESSAGE } from '../utils/cameraZoneReadiness'

function SettingsPage() {
  const navigate = useNavigate()
  const [cameras, setCameras] = useState([])
  const [farms, setFarms] = useState([{ id: 'FARM-001', name: 'AMS Farm Long An' }])
  const [loading, setLoading] = useState(true)
  const [formMode, setFormMode] = useState(null)
  const [editingCamera, setEditingCamera] = useState(null)
  const [statusMessage, setStatusMessage] = useState('')
  const [systemSettings, setSystemSettings] = useState(null)
  const [demoStatus, setDemoStatus] = useState(null)
  const [managedUsers, setManagedUsers] = useState([])
  const [notificationSettings, setNotificationSettings] = useState(null)
  const [notificationStatus, setNotificationStatus] = useState('')
  const [notificationAction, setNotificationAction] = useState('')
  const [zaloModalOpen, setZaloModalOpen] = useState(false)
  const [zaloSession, setZaloSession] = useState(null)
  const [alertPrefs, setAlertPrefs] = useState(() =>
    Object.fromEntries(alertSettings.map((setting) => [setting.id, setting.enabled])),
  )
  const zaloPollRef = useRef(null)

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
      const [cameraData, farmData, settingsData, usersData, demoData, notifySettings] = await Promise.all([
        getCameras(),
        getFarms().catch(() => []),
        getSystemSettings().catch(() => null),
        listUsers().catch(() => []),
        fetchDemoStatus().catch(() => null),
        getNotificationSettings().catch(() => null),
      ])
      setCameras(cameraData)
      setSystemSettings(settingsData)
      setDemoStatus(demoData)
      setManagedUsers(usersData)
      setNotificationSettings(notifySettings)
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
      closeForm()

      const zones = await loadCameraZones(created.id).catch(() => [])
      if (zones.length === 0) {
        setStatusMessage(NEW_CAMERA_ZONE_MESSAGE)
        navigate(`/thiet-ke-vung-atsh?camera=${encodeURIComponent(created.id)}`)
        return
      }

      setStatusMessage(`Đã thêm ${created.name}`)
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

  const handleSaveNotificationSettings = async () => {
    if (!notificationSettings || notificationAction) return
    setNotificationAction('save')
    setNotificationStatus('')
    try {
      const saved = await updateNotificationSettings({
        gmail_enabled: notificationSettings.gmail_enabled,
        zalo_enabled: notificationSettings.zalo_enabled,
        gmail_recipient: notificationSettings.gmail_recipient,
      })
      setNotificationSettings(saved)
      setNotificationStatus('Đã lưu cấu hình thông báo')
    } catch (error) {
      setNotificationStatus(error.message)
    } finally {
      setNotificationAction('')
    }
  }

  const handleConnectGmail = async () => {
    if (!notificationSettings || notificationAction) return
    setNotificationAction('gmail-connect')
    setNotificationStatus('')
    try {
      await connectGmailNotification({
        gmail_recipient: notificationSettings.gmail_recipient,
      })
      const saved = await getNotificationSettings()
      setNotificationSettings(saved)
      setNotificationStatus('✓ Đã kết nối Gmail')
    } catch (error) {
      setNotificationStatus(error.message)
    } finally {
      setNotificationAction('')
    }
  }

  const handleGmailVerify = async () => {
    if (!notificationSettings || notificationAction) return
    setNotificationAction('gmail-verify')
    setNotificationStatus('')
    try {
      await verifyGmailNotification()
      setNotificationStatus('✓ Kết nối SMTP Gmail thành công')
    } catch (error) {
      setNotificationStatus(error.message)
    } finally {
      setNotificationAction('')
    }
  }

  const handleGmailTest = async () => {
    if (!notificationSettings || notificationAction) return
    setNotificationAction('gmail-test')
    setNotificationStatus('')
    try {
      await testGmailNotification()
      const saved = await getNotificationSettings()
      setNotificationSettings(saved)
      setNotificationStatus('✓ Đã gửi Email thành công')
    } catch (error) {
      const saved = await getNotificationSettings().catch(() => null)
      if (saved) setNotificationSettings(saved)
      setNotificationStatus(error.message)
    } finally {
      setNotificationAction('')
    }
  }

  const formatGmailSentAt = (value) => {
    if (!value) return '—'
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return value
    return date.toLocaleString('vi-VN')
  }

  const closeZaloModal = () => {
    if (zaloPollRef.current) {
      clearInterval(zaloPollRef.current)
      zaloPollRef.current = null
    }
    setZaloModalOpen(false)
    setZaloSession(null)
  }

  const handleStartZaloConnect = async () => {
    if (notificationAction) return
    setNotificationAction('zalo-connect')
    setNotificationStatus('')
    try {
      const session = await startZaloConnect()
      setZaloSession(session)
      setZaloModalOpen(true)

      if (zaloPollRef.current) clearInterval(zaloPollRef.current)
      zaloPollRef.current = setInterval(async () => {
        try {
          const result = await pollZaloConnect(session.session_id)
          if (result.connected && result.settings) {
            setNotificationSettings(result.settings)
            setNotificationStatus('Zalo: ✓ Đã kết nối')
            closeZaloModal()
          } else if (result.status === 'expired') {
            setNotificationStatus('Phiên quét mã QR đã hết hạn. Vui lòng thử lại.')
            closeZaloModal()
          }
        } catch (error) {
          setNotificationStatus(error.message)
          closeZaloModal()
        }
      }, 2500)
    } catch (error) {
      setNotificationStatus(error.message)
    } finally {
      setNotificationAction('')
    }
  }

  useEffect(() => () => {
    if (zaloPollRef.current) clearInterval(zaloPollRef.current)
  }, [])

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
      <section className="panel settings-tools-panel">
        <div className="panel__header">
          <div>
            <h2>Công cụ hệ thống</h2>
            <p>Triển khai, giám sát và chẩn đoán AMS</p>
          </div>
        </div>
        <div className="settings-tools-grid">
          <Link to="/setup" className="settings-tools-card">
            <Rocket size={20} />
            <div>
              <strong>Hướng dẫn cài đặt</strong>
              <span>Thiết lập ban đầu cho trang trại</span>
            </div>
          </Link>
          <Link to="/system-status" className="settings-tools-card">
            <Activity size={20} />
            <div>
              <strong>Trạng thái hệ thống</strong>
              <span>Theo dõi database, Redis, camera</span>
            </div>
          </Link>
          <Link to="/diagnostics" className="settings-tools-card">
            <Stethoscope size={20} />
            <div>
              <strong>Chẩn đoán hệ thống</strong>
              <span>Kiểm tra sự cố và log vận hành</span>
            </div>
          </Link>
        </div>
      </section>

      <div className="settings-grid">
        <section className="panel">
          <UserManagementPanel
            users={managedUsers}
            onUsersChange={setManagedUsers}
            onStatus={setStatusMessage}
          />
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
                  <input
                    type="checkbox"
                    checked={Boolean(alertPrefs[setting.id])}
                    onChange={(event) => {
                      setAlertPrefs((prev) => ({
                        ...prev,
                        [setting.id]: event.target.checked,
                      }))
                      setStatusMessage(`Đã ${event.target.checked ? 'bật' : 'tắt'} cảnh báo: ${setting.name}`)
                    }}
                  />
                  <span className="toggle__slider" />
                </label>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Thông báo vi phạm ATSH</h2>
              <p className="panel__desc">Tự động gửi cảnh báo khi Compliance Engine xác nhận vi phạm mới (OPEN)</p>
              {notificationStatus ? <p className="panel__meta">{notificationStatus}</p> : null}
            </div>
          </div>
          {notificationSettings ? (
            <div className="settings-form notification-simple">
              <p className="notification-simple__intro">
                Khi Compliance Engine xác nhận vi phạm mới (OPEN), AMS tự động gửi Gmail cảnh báo — không cần thao tác thêm.
              </p>

              <div className="notification-simple__card">
                <label className="settings-form__label settings-form__label--inline">
                  <span><Mail size={15} /> Bật Gmail</span>
                  <label className="toggle">
                    <input
                      type="checkbox"
                      checked={Boolean(notificationSettings.gmail_enabled)}
                      onChange={(event) =>
                        setNotificationSettings((prev) => ({
                          ...prev,
                          gmail_enabled: event.target.checked,
                        }))
                      }
                    />
                    <span className="toggle__slider" />
                  </label>
                </label>

                <label className="settings-form__label">
                  <span>Email nhận cảnh báo</span>
                  <input
                    type="email"
                    className="settings-form__input"
                    placeholder="email-cua-ban@gmail.com"
                    value={notificationSettings.gmail_recipient || ''}
                    disabled={Boolean(notificationSettings.gmail_connected)}
                    onChange={(event) =>
                      setNotificationSettings((prev) => ({
                        ...prev,
                        gmail_recipient: event.target.value,
                      }))
                    }
                  />
                </label>

                {notificationSettings.gmail_connected ? (
                  <>
                    <p className="notification-simple__connected">
                      <CheckCircle2 size={16} /> ✓ Gmail đã kết nối
                    </p>
                    <div className="notification-simple__meta">
                      <p><strong>Email gửi:</strong> {notificationSettings.gmail_sender || '—'}</p>
                      <p><strong>Email nhận:</strong> {notificationSettings.gmail_recipient || '—'}</p>
                      <p><strong>Lần gửi cuối:</strong> {formatGmailSentAt(notificationSettings.gmail_last_sent_at)}</p>
                      <p>
                        <strong>Trạng thái:</strong>{' '}
                        {notificationSettings.gmail_last_status === 'success' ? (
                          <span className="notification-simple__status notification-simple__status--ok">✓ Thành công</span>
                        ) : notificationSettings.gmail_last_status === 'failed' ? (
                          <span className="notification-simple__status notification-simple__status--error">Gửi thất bại</span>
                        ) : (
                          '—'
                        )}
                      </p>
                      {notificationSettings.gmail_last_error ? (
                        <p className="notification-simple__error">{notificationSettings.gmail_last_error}</p>
                      ) : null}
                    </div>
                    <div className="notification-simple__actions">
                      <button
                        type="button"
                        className="btn btn--outline"
                        disabled={Boolean(notificationAction)}
                        onClick={handleGmailVerify}
                      >
                        {notificationAction === 'gmail-verify' ? 'Đang kiểm tra…' : 'Kiểm tra kết nối'}
                      </button>
                      <button
                        type="button"
                        className="btn btn--secondary"
                        disabled={Boolean(notificationAction)}
                        onClick={handleGmailTest}
                      >
                        {notificationAction === 'gmail-test' ? 'Đang gửi…' : 'Gửi Email thử'}
                      </button>
                    </div>
                  </>
                ) : (
                  <button
                    type="button"
                    className="btn btn--primary"
                    disabled={Boolean(notificationAction) || !notificationSettings.gmail_recipient}
                    onClick={handleConnectGmail}
                  >
                    {notificationAction === 'gmail-connect' ? 'Đang kết nối…' : 'Kết nối Gmail'}
                  </button>
                )}
              </div>

              <div className="notification-simple__card">
                <label className="settings-form__label settings-form__label--inline">
                  <span><MessageCircle size={15} /> Bật Zalo</span>
                  <label className="toggle">
                    <input
                      type="checkbox"
                      checked={Boolean(notificationSettings.zalo_enabled)}
                      onChange={(event) =>
                        setNotificationSettings((prev) => ({
                          ...prev,
                          zalo_enabled: event.target.checked,
                        }))
                      }
                    />
                    <span className="toggle__slider" />
                  </label>
                </label>

                {notificationSettings.zalo_connected ? (
                  <p className="notification-simple__connected">
                    <CheckCircle2 size={16} /> Đã kết nối
                  </p>
                ) : (
                  <button
                    type="button"
                    className="btn btn--outline"
                    disabled={Boolean(notificationAction)}
                    onClick={handleStartZaloConnect}
                  >
                    {notificationAction === 'zalo-connect' ? 'Đang mở…' : 'Quét mã QR'}
                  </button>
                )}
              </div>

              <div className="settings-form__actions">
                <button
                  type="button"
                  className="btn btn--primary"
                  disabled={Boolean(notificationAction)}
                  onClick={handleSaveNotificationSettings}
                >
                  {notificationAction === 'save' ? 'Đang lưu…' : 'Lưu cấu hình'}
                </button>
              </div>
            </div>
          ) : (
            <p className="panel__meta">Không tải được cấu hình thông báo.</p>
          )}
        </section>
      </div>

      {zaloModalOpen && zaloSession ? (
        <div className="notification-qr-modal" role="dialog" aria-modal="true">
          <div className="notification-qr-modal__backdrop" onClick={closeZaloModal} />
          <div className="notification-qr-modal__panel">
            <button type="button" className="notification-qr-modal__close" onClick={closeZaloModal} aria-label="Đóng">
              <X size={18} />
            </button>
            <h3>Quét mã QR bằng Zalo</h3>
            <p>{zaloSession.message}</p>
            <img src={zaloSession.qr_url} alt="Mã QR quan tâm Zalo OA" className="notification-qr-modal__image" />
            <p className="notification-qr-modal__hint">Sau khi quan tâm Official Account, AMS sẽ tự nhận kết nối.</p>
          </div>
        </div>
      ) : null}

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
