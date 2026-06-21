import { apiFetch } from './apiClient'

async function fetchJson(path) {
  const response = await apiFetch(path)
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

export function fetchComplianceReport() {
  return fetchJson('/reports/compliance')
}

export function fetchComplianceKpis() {
  return fetchJson('/reports/compliance/kpis')
}

export function fetchTopViolations(days = 7, limit = 10) {
  return fetchJson(`/reports/compliance/top-violations?days=${days}&limit=${limit}`)
}

export function fetchCompliancePdfData(days = 30) {
  return fetchJson(`/reports/compliance/pdf-data?days=${days}`)
}

export function fetchCameraHealthSummary() {
  return fetchJson('/camera-health/summary')
}
