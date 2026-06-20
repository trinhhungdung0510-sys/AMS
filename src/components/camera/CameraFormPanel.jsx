import { useEffect, useState } from 'react'
import { resolveRtspUrl, testCameraConnection } from '../../services/cameraService'

const STATUS_OPTIONS = [
  { value: 'online', label: 'Online' },
  { value: 'offline', label: 'Offline' },
]

function CameraFormPanel({
  title,
  submitLabel,
  initialValues,
  farms = [],
  isEdit = false,
  onSubmit,
  onCancel,
}) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState(null)
  const [testError, setTestError] = useState('')

  useEffect(() => {
    setValues(initialValues)
    setErrors({})
    setTestResult(null)
    setTestError('')
  }, [initialValues])

  const updateField = (field, value) => {
    setValues((current) => ({ ...current, [field]: value }))
    setErrors((current) => ({ ...current, [field]: undefined }))
    setTestResult(null)
    setTestError('')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)
    try {
      await onSubmit(values, setErrors)
    } finally {
      setSubmitting(false)
    }
  }

  const handleTestConnection = async () => {
    setTesting(true)
    setTestResult(null)
    setTestError('')

    const rtspUrl = resolveRtspUrl(values)
    if (!rtspUrl) {
      setTestError('Nhập RTSP URL hoặc IP + username + password để kiểm tra')
      setTesting(false)
      return
    }

    if (!values.rtsp_url?.trim() && !values.password?.trim()) {
      setTestError('Cần mật khẩu để dựng RTSP URL khi chưa nhập URL trực tiếp')
      setTesting(false)
      return
    }

    try {
      const result = await testCameraConnection(rtspUrl)
      setTestResult(result)
      if (result.success) {
        setValues((current) => ({
          ...current,
          status: 'online',
          fps: result.fps ?? current.fps,
          resolution: result.resolution || current.resolution,
        }))
      } else {
        setValues((current) => ({ ...current, status: 'offline' }))
      }
    } catch (error) {
      setTestError(error.message)
      setValues((current) => ({ ...current, status: 'offline' }))
    } finally {
      setTesting(false)
    }
  }

  const connectionOnline = testResult?.success === true
  const connectionOffline = testResult?.success === false || Boolean(testError)

  return (
    <div className="camera-form-overlay">
      <div className="camera-form-panel panel">
        <div className="panel__header">
          <div>
            <h2 className="panel__title">{title}</h2>
            <p className="panel__desc">
              {isEdit ? 'Cập nhật thông tin kết nối camera IP thực' : 'Thêm camera IP mới vào hệ thống AMS'}
            </p>
          </div>
          <button type="button" className="btn btn--ghost" onClick={onCancel}>
            Đóng
          </button>
        </div>

        <form className="camera-form settings-form" onSubmit={handleSubmit}>
          <div className="camera-form__grid">
            <label className="settings-form__label">
              <span>Tên camera *</span>
              <input
                className="settings-form__input"
                value={values.name}
                onChange={(e) => updateField('name', e.target.value)}
                placeholder="Camera Cổng trại"
              />
              {errors.name ? <small className="camera-form__error">{errors.name}</small> : null}
            </label>

            <label className="settings-form__label">
              <span>Hãng sản xuất</span>
              <input
                className="settings-form__input"
                value={values.manufacturer}
                onChange={(e) => updateField('manufacturer', e.target.value)}
                placeholder="Hikvision, Dahua..."
              />
            </label>

            <label className="settings-form__label">
              <span>IP *</span>
              <input
                className="settings-form__input"
                value={values.ip}
                onChange={(e) => updateField('ip', e.target.value)}
                placeholder="192.168.10.11"
              />
              {errors.ip ? <small className="camera-form__error">{errors.ip}</small> : null}
            </label>

            <label className="settings-form__label">
              <span>Port</span>
              <input
                type="number"
                className="settings-form__input"
                value={values.port}
                onChange={(e) => updateField('port', e.target.value)}
                min={1}
                max={65535}
              />
            </label>

            <label className="settings-form__label">
              <span>Username *</span>
              <input
                className="settings-form__input"
                value={values.username}
                onChange={(e) => updateField('username', e.target.value)}
                placeholder="admin"
                autoComplete="off"
              />
              {errors.username ? <small className="camera-form__error">{errors.username}</small> : null}
            </label>

            <label className="settings-form__label">
              <span>Mật khẩu {isEdit ? '' : '*'}</span>
              <input
                type="password"
                className="settings-form__input"
                value={values.password}
                onChange={(e) => updateField('password', e.target.value)}
                placeholder={isEdit ? 'Để trống nếu không đổi' : '••••••••'}
                autoComplete="new-password"
              />
              {errors.password ? <small className="camera-form__error">{errors.password}</small> : null}
            </label>

            <label className="settings-form__label camera-form__full">
              <span>RTSP URL</span>
              <input
                className="settings-form__input"
                value={values.rtsp_url}
                onChange={(e) => updateField('rtsp_url', e.target.value)}
                placeholder="rtsp://user:pass@ip:554/Streaming/Channels/101"
              />
            </label>

            <div className="camera-form__full camera-connection-test">
              <div className="camera-connection-test__actions">
                <button
                  type="button"
                  className="btn btn--outline"
                  onClick={handleTestConnection}
                  disabled={testing}
                >
                  {testing ? 'Đang kiểm tra...' : 'Test Connection'}
                </button>
              </div>

              {(testResult || testError) ? (
                <div className={`camera-connection-test__result${connectionOnline ? ' camera-connection-test__result--online' : ''}${connectionOffline ? ' camera-connection-test__result--offline' : ''}`}>
                  <div className="camera-connection-test__row">
                    <span>Trạng thái</span>
                    <strong>
                      {testing ? 'Đang kiểm tra...' : connectionOnline ? 'Online' : 'Offline'}
                    </strong>
                  </div>
                  <div className="camera-connection-test__row">
                    <span>Resolution</span>
                    <strong>{testResult?.resolution || '—'}</strong>
                  </div>
                  <div className="camera-connection-test__row">
                    <span>FPS</span>
                    <strong>{testResult?.fps ?? '—'}</strong>
                  </div>
                  {(testResult?.error || testError) ? (
                    <p className="camera-connection-test__error">{testResult?.error || testError}</p>
                  ) : null}
                </div>
              ) : null}
            </div>

            <label className="settings-form__label">
              <span>Khu vực</span>
              <input
                className="settings-form__input"
                value={values.zone}
                onChange={(e) => updateField('zone', e.target.value)}
                placeholder="Cổng trại"
              />
            </label>

            <label className="settings-form__label">
              <span>Trại</span>
              <select
                className="settings-form__input"
                value={values.farm_id}
                onChange={(e) => updateField('farm_id', e.target.value)}
              >
                {farms.map((farm) => (
                  <option key={farm.id} value={farm.id}>{farm.name}</option>
                ))}
              </select>
            </label>

            <label className="settings-form__label">
              <span>Độ phân giải</span>
              <input
                className="settings-form__input"
                value={values.resolution}
                onChange={(e) => updateField('resolution', e.target.value)}
                placeholder="1080p"
              />
            </label>

            <label className="settings-form__label">
              <span>FPS</span>
              <input
                type="number"
                className="settings-form__input"
                value={values.fps}
                onChange={(e) => updateField('fps', e.target.value)}
                min={0}
                max={120}
              />
            </label>

            <label className="settings-form__label">
              <span>Trạng thái</span>
              <select
                className="settings-form__input"
                value={values.status}
                onChange={(e) => updateField('status', e.target.value)}
              >
                {STATUS_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </label>

            <label className="settings-form__label camera-form__checkbox">
              <input
                type="checkbox"
                checked={values.is_active}
                onChange={(e) => updateField('is_active', e.target.checked)}
              />
              <span>Kích hoạt camera</span>
            </label>
          </div>

          <div className="settings-form__actions">
            <button type="button" className="btn btn--outline" onClick={onCancel}>
              Hủy
            </button>
            <button type="submit" className="btn btn--primary" disabled={submitting}>
              {submitting ? 'Đang lưu...' : submitLabel}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CameraFormPanel
