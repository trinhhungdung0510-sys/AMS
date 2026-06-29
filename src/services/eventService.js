import { apiFetch } from './apiClient'

const DEFAULT_EVENT_LIMIT = 100

export async function getEvents({ limit = DEFAULT_EVENT_LIMIT, page = 1 } = {}) {
  const response = await apiFetch(`/events?limit=${limit}&page=${page}`)
  if (!response.ok) {
    throw new Error('Failed to load events')
  }
  const data = await response.json()
  if (Array.isArray(data)) {
    return data
  }
  return data.items || []
}

export async function getEngineEvents(limit = DEFAULT_EVENT_LIMIT) {
  const response = await apiFetch(`/events/engine?limit=${limit}`)
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
