import { apiFetch } from './apiClient'

async function parseJson(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }
  return response.json()
}

export function fetchDemoStatus() {
  return parseJson(apiFetch('/demo/status'))
}

export function startDemoMode() {
  return parseJson(apiFetch('/demo/start', { method: 'POST' }))
}

export function stopDemoMode() {
  return parseJson(apiFetch('/demo/stop', { method: 'POST' }))
}

export function generateDemoViolations(count = 12, publish = true) {
  return parseJson(
    apiFetch(`/demo/generate-violations?count=${count}&publish=${publish ? 'true' : 'false'}`, {
      method: 'POST',
    }),
  )
}
