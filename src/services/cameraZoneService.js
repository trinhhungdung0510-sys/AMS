import { apiFetch } from './apiClient'

export async function getCameraZones(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/zones`)
  if (!response.ok) {
    throw new Error('Không tải được danh sách vùng')
  }
  return response.json()
}

export async function createCameraZone(cameraId, payload) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/zones`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Không lưu được vùng')
  }
  return response.json()
}

export async function updateCameraZone(zoneId, payload) {
  const response = await apiFetch(`/zones/${encodeURIComponent(zoneId)}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Không cập nhật được vùng')
  }
  return response.json()
}

export async function deleteCameraZone(zoneId) {
  const response = await apiFetch(`/zones/${encodeURIComponent(zoneId)}`, {
    method: 'DELETE',
  })
  if (!response.ok && response.status !== 404) {
    throw new Error('Không xóa được vùng')
  }
}

export const ZONE_TYPE_OPTIONS = [
  { value: 'restricted', label: 'Vùng cấm' },
  { value: 'clean', label: 'Vùng sạch' },
  { value: 'dirty', label: 'Vùng bẩn' },
  { value: 'warning', label: 'Cảnh báo' },
  { value: 'monitoring', label: 'Giám sát' },
]
