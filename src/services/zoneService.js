import { apiFetch } from './apiClient'

export async function listZones(cameraId) {
  const query = cameraId ? `?camera_id=${encodeURIComponent(cameraId)}` : ''
  const response = await apiFetch(`/zones${query}`)
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

export async function createZone(payload) {
  const response = await apiFetch('/zones', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

export async function updateZone(zoneId, payload) {
  const response = await apiFetch(`/zones/${zoneId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

export async function deleteZone(zoneId) {
  const response = await apiFetch(`/zones/${zoneId}`, { method: 'DELETE' })
  if (!response.ok && response.status !== 404) {
    throw new Error(`HTTP ${response.status}`)
  }
}
