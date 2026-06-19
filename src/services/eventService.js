import { apiFetch } from './apiClient'

export async function getEvents() {
  const response = await apiFetch('/events')
  if (!response.ok) {
    throw new Error('Failed to load events')
  }
  return response.json()
}
