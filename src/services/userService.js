import { apiFetch } from './apiClient'

export async function listUsers(farmId) {
  const query = farmId ? `?farm_id=${encodeURIComponent(farmId)}` : ''
  const response = await apiFetch(`/users${query}`)
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function createUser(payload) {
  const response = await apiFetch('/users', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function updateUser(userId, payload) {
  const response = await apiFetch(`/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}
