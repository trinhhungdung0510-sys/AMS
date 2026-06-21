import { API_BASE_URL } from '../config/api'
import { apiFetch } from './apiClient'

async function parseJson(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }
  return response.json()
}

export async function fetchApiHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  return parseJson(response)
}

export async function fetchSetupStatus() {
  return parseJson(await apiFetch('/deployment/setup/status'))
}

export async function fetchSystemStatus() {
  return parseJson(await apiFetch('/deployment/status'))
}

export async function fetchDiagnostics() {
  return parseJson(await apiFetch('/deployment/diagnostics'))
}

export async function testZone(zoneId) {
  return parseJson(await apiFetch(`/deployment/zones/${encodeURIComponent(zoneId)}/test`))
}

export async function testComplianceRule(payload) {
  return parseJson(
    await apiFetch('/deployment/rules/test', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  )
}

export async function browseEvidence(params = {}) {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value != null && value !== ''),
  ).toString()
  return parseJson(await apiFetch(`/deployment/evidence${query ? `?${query}` : ''}`))
}

export async function exportConfigBundle() {
  return parseJson(await apiFetch('/deployment/export'))
}

export async function importConfigBundle(payload) {
  return parseJson(
    await apiFetch('/deployment/import', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  )
}

export async function createFarm(payload) {
  return parseJson(
    await apiFetch('/farms', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  )
}

export async function createUniform(payload) {
  return parseJson(
    await apiFetch('/uniforms', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  )
}

export async function createCameraZone(cameraId, payload) {
  return parseJson(
    await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/zones`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  )
}
