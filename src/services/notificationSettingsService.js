import { apiFetch } from './apiClient'

function parseApiError(data, fallback) {
  if (typeof data?.detail === 'string') return data.detail
  if (typeof data?.message === 'string') return data.message
  if (Array.isArray(data?.detail)) {
    return data.detail
      .map((item) => {
        if (typeof item === 'string') return item
        if (typeof item?.msg === 'string') return item.msg
        return JSON.stringify(item)
      })
      .join(', ')
  }
  if (data?.detail && typeof data.detail === 'object') {
    return data.detail.message || JSON.stringify(data.detail)
  }
  return fallback
}

export async function getNotificationSettings() {
  const response = await apiFetch('/notifications/settings')
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, 'Không tải được cấu hình thông báo'))
  }
  return data
}

export async function updateNotificationSettings(payload) {
  const response = await apiFetch('/notifications/settings', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, 'Không lưu được cấu hình thông báo'))
  }
  return data
}

export async function connectGmailNotification({ gmail_recipient }) {
  const response = await apiFetch('/notification/gmail/connect', {
    method: 'POST',
    body: JSON.stringify({ gmail_recipient }),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, `Không kết nối được Gmail (HTTP ${response.status})`))
  }
  return data
}

export const connectGmail = connectGmailNotification

export async function testGmailNotification() {
  const response = await apiFetch('/notification/gmail/test', {
    method: 'POST',
    body: JSON.stringify({}),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, `Không gửi được email thử nghiệm (HTTP ${response.status})`))
  }
  return data
}

export const testGmail = testGmailNotification

export async function verifyGmailNotification() {
  const response = await apiFetch('/notification/gmail/verify', {
    method: 'POST',
    body: JSON.stringify({}),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, `Không kiểm tra được kết nối Gmail (HTTP ${response.status})`))
  }
  return data
}

export const verifyGmail = verifyGmailNotification

export async function startZaloConnect() {
  const response = await apiFetch('/notifications/connect/zalo/start', {
    method: 'POST',
    body: JSON.stringify({}),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, 'Không khởi tạo được kết nối Zalo'))
  }
  return data
}

export async function pollZaloConnect(sessionId) {
  const response = await apiFetch(`/notifications/connect/zalo/status/${sessionId}`)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, 'Không kiểm tra được trạng thái Zalo'))
  }
  return data
}

export async function sendNotificationTest(channel = 'dashboard') {
  const response = await apiFetch('/notifications/test', {
    method: 'POST',
    body: JSON.stringify({ channel }),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, 'Không gửi được thông báo thử nghiệm'))
  }
  return data
}

export async function getNotificationDeliveries({ eventId, limit = 50 } = {}) {
  const params = new URLSearchParams()
  if (eventId) params.set('event_id', eventId)
  if (limit) params.set('limit', String(limit))
  const response = await apiFetch(`/notifications/deliveries?${params.toString()}`)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(parseApiError(data, 'Không tải được lịch sử gửi thông báo'))
  }
  return data
}
