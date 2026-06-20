import { apiFetch } from './apiClient'

export async function getCameraDetections(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/detections`)
  if (!response.ok) {
    throw new Error('Không tải được danh sách phát hiện AI')
  }
  return response.json()
}

export async function createCameraDetection(cameraId, payload) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/detections`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Không lưu được phát hiện AI')
  }
  return response.json()
}
