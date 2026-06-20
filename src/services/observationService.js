import { apiFetch } from './apiClient'

async function parseJson(response) {
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.detail || data.message || `HTTP ${response.status}`)
  }
  return data
}

export async function createObservation(payload) {
  const response = await apiFetch('/observations', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  return parseJson(response)
}

export async function getObservation(observationId) {
  const response = await apiFetch(`/observations/${observationId}`)
  return parseJson(response)
}

export async function listObservations(cameraId, limit = 50) {
  const response = await apiFetch(`/cameras/${cameraId}/observations?limit=${limit}`)
  return parseJson(response)
}
