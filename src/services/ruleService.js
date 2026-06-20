import { apiFetch } from './apiClient'

function parseApiError(data, fallback) {
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg || item).join(', ')
  }
  return fallback
}

export async function getRules(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/rules`)
  if (!response.ok) {
    throw new Error('Không tải được danh sách rule')
  }
  return response.json()
}

export async function createRule(cameraId, data) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/rules`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(parseApiError(error, 'Không tạo được rule'))
  }
  return response.json()
}

export async function updateRule(id, data) {
  const response = await apiFetch(`/rules/${encodeURIComponent(id)}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(parseApiError(error, 'Không cập nhật được rule'))
  }
  return response.json()
}

export async function deleteRule(id) {
  const response = await apiFetch(`/rules/${encodeURIComponent(id)}`, {
    method: 'DELETE',
  })
  if (!response.ok && response.status !== 404) {
    throw new Error('Không xóa được rule')
  }
}

export async function toggleRule(id) {
  const response = await apiFetch(`/rules/${encodeURIComponent(id)}/toggle`, {
    method: 'PATCH',
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(parseApiError(error, 'Không đổi trạng thái rule'))
  }
  return response.json()
}
