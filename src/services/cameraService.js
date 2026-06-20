import { apiFetch } from './apiClient'

export function getCameraIp(camera) {
  return camera?.ip ?? camera?.ip_address ?? ''
}

export async function getCameras() {
  const response = await apiFetch('/cameras')
  if (!response.ok) {
    throw new Error('Failed to load cameras')
  }
  return response.json()
}

export async function getCameraById(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}`)
  if (response.status === 404) return null
  if (!response.ok) {
    throw new Error('Failed to load camera')
  }
  return response.json()
}

export async function createCamera(payload) {
  const response = await apiFetch('/cameras', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to create camera')
  }
  return response.json()
}

export async function updateCamera(cameraId, payload) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Failed to update camera')
  }
  return response.json()
}

export async function deleteCamera(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}`, {
    method: 'DELETE',
  })
  if (!response.ok && response.status !== 404) {
    throw new Error('Failed to delete camera')
  }
}

export const EMPTY_CAMERA_FORM = {
  name: '',
  manufacturer: '',
  ip: '',
  port: 554,
  username: '',
  password: '',
  rtsp_url: '',
  zone: '',
  farm_id: 'FARM-001',
  resolution: '1080p',
  fps: 25,
  status: 'online',
  is_active: true,
}

export function cameraToFormValues(camera) {
  if (!camera) return { ...EMPTY_CAMERA_FORM }

  return {
    name: camera.name || '',
    manufacturer: camera.manufacturer || '',
    ip: getCameraIp(camera),
    port: camera.port ?? 554,
    username: camera.username || '',
    password: '',
    rtsp_url: camera.rtsp_url || '',
    zone: camera.zone || '',
    farm_id: camera.farm_id || 'FARM-001',
    resolution: camera.resolution || '1080p',
    fps: camera.fps ?? 25,
    status: camera.status || 'online',
    is_active: camera.is_active ?? true,
  }
}

export function validateCameraForm(values, { isEdit = false } = {}) {
  const errors = {}

  if (!values.name?.trim()) errors.name = 'Tên camera là bắt buộc'
  if (!values.ip?.trim()) errors.ip = 'IP là bắt buộc'
  if (!values.username?.trim()) errors.username = 'Username là bắt buộc'
  if (!isEdit && !values.password?.trim()) errors.password = 'Mật khẩu là bắt buộc'

  return errors
}

export function buildCameraPayload(values, { isEdit = false } = {}) {
  const payload = {
    name: values.name.trim(),
    manufacturer: values.manufacturer.trim() || null,
    ip: values.ip.trim(),
    port: Number(values.port) || 554,
    username: values.username.trim(),
    rtsp_url: values.rtsp_url.trim() || null,
    zone: values.zone.trim() || 'Chưa phân vùng',
    farm_id: values.farm_id || 'FARM-001',
    resolution: values.resolution || '1080p',
    fps: Number(values.fps) || 25,
    status: values.status || 'online',
    is_active: Boolean(values.is_active),
  }

  if (!isEdit || values.password?.trim()) {
    payload.password = values.password.trim()
  }

  return payload
}

export function resolveRtspUrl(values) {
  if (values.rtsp_url?.trim()) return values.rtsp_url.trim()
  if (!values.ip?.trim() || !values.username?.trim()) return ''

  const password = encodeURIComponent(values.password?.trim() || '')
  const username = encodeURIComponent(values.username.trim())
  const port = Number(values.port) || 554
  return `rtsp://${username}:${password}@${values.ip.trim()}:${port}/Streaming/Channels/101`
}

export async function testCameraConnection(rtspUrl) {
  const response = await apiFetch('/cameras/test', {
    method: 'POST',
    body: JSON.stringify({ rtspUrl }),
  })

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = typeof data.detail === 'string'
      ? data.detail
      : Array.isArray(data.detail)
        ? data.detail.map((item) => item.msg).join(', ')
        : 'Không thể kiểm tra kết nối camera'
    throw new Error(detail)
  }

  return data
}
