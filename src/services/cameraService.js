import { apiFetch } from './apiClient'

export async function getCameras() {
  const response = await apiFetch('/cameras')
  if (!response.ok) {
    throw new Error('Failed to load cameras')
  }
  return response.json()
}
