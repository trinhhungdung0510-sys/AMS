import { apiFetch } from './apiClient'

export async function getFarms() {
  const response = await apiFetch('/farms')
  if (!response.ok) {
    throw new Error('Failed to load farms')
  }
  return response.json()
}
