import { apiFetch } from './apiClient'

export async function getSystemSettings() {
  const response = await apiFetch('/system/settings')
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function updateSystemSettings(payload) {
  const response = await apiFetch('/system/settings', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function createSystemBackup() {
  const response = await apiFetch('/system/backup', { method: 'POST' })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function restoreSystemBackup(payload) {
  const response = await apiFetch('/system/restore', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function listAuditLogs(params = {}) {
  const query = new URLSearchParams(params).toString()
  const response = await apiFetch(`/audit${query ? `?${query}` : ''}`)
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}
