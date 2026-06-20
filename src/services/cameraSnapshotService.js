import { API_BASE_URL } from '../config/api'
import { apiFetch } from './apiClient'

export function resolveSnapshotAssetUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
}

export async function captureCameraSnapshot(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/snapshot`)
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.detail || data.error || 'Không thể chụp snapshot')
  }

  return data
}

export async function getLatestCameraSnapshot(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/latest-snapshot`)
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.detail || data.error || 'Không thể tải snapshot mới nhất')
  }

  return data
}
