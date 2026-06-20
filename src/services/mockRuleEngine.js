import { apiFetch } from './apiClient'
import { notifyEventCreated } from '../providers/NotificationProvider'

function parseApiError(data, fallback) {
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg || item).join(', ')
  }
  return fallback
}

/**
 * Mock Rule Engine — gọi backend trigger endpoint, sinh Event giả.
 */
export async function triggerRule(ruleId, options = {}) {
  const response = await apiFetch(`/rules/${encodeURIComponent(ruleId)}/trigger`, {
    method: 'POST',
    body: JSON.stringify(options),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(parseApiError(error, 'Không kích hoạt được rule'))
  }

  const event = await response.json()
  notifyEventCreated(event)
  return event
}
