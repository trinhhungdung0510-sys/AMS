import { apiFetch } from './apiClient'

export async function getEvents() {
  const response = await apiFetch('/events')
  if (!response.ok) {
    throw new Error('Failed to load events')
  }
  return response.json()
}

export async function getEngineEvents() {
  const response = await apiFetch('/events/engine')
  if (!response.ok) {
    throw new Error('Không tải được sự kiện rule engine')
  }
  return response.json()
}

export async function getCameraEventTimeline(cameraId) {
  const response = await apiFetch(`/events/cameras/${encodeURIComponent(cameraId)}/timeline`)
  if (!response.ok) {
    throw new Error('Không tải được timeline sự kiện')
  }
  return response.json()
}

export async function createEngineEvent(payload) {
  const response = await apiFetch('/events/engine', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.detail || 'Không tạo được sự kiện từ evaluator')
  }
  return data
}
