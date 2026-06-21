import { apiFetch } from './apiClient'

function buildQuery(params = {}) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value != null && value !== '' && value !== 'all') {
      search.set(key, String(value))
    }
  })
  const query = search.toString()
  return query ? `?${query}` : ''
}

export async function getComplianceEvents(params = {}) {
  const response = await apiFetch(`/compliance/events${buildQuery(params)}`)
  if (!response.ok) {
    throw new Error('Không tải được sự kiện tuân thủ')
  }
  return response.json()
}

export async function getComplianceEventsSummary(date) {
  const response = await apiFetch(`/compliance/events/summary${buildQuery({ date })}`)
  if (!response.ok) {
    throw new Error('Không tải được tổng hợp vi phạm')
  }
  return response.json()
}

export async function getEventsPaginated(params = {}) {
  const mapped = {
    page: params.page,
    limit: params.limit,
    eventType: params.eventType,
    cameraId: params.cameraId,
    zoneId: params.zoneId,
  }
  const response = await apiFetch(`/events${buildQuery(mapped)}`)
  if (!response.ok) {
    throw new Error('Không tải được sự kiện')
  }
  return response.json()
}
