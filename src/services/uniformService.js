import { apiFetch } from './apiClient'

export class UniformInUseError extends Error {
  constructor(message, zones = []) {
    super(message)
    this.name = 'UniformInUseError'
    this.code = 'UNIFORM_IN_USE'
    this.zones = zones
  }
}

function throwApiError(data, fallback) {
  const detail = data?.detail
  if (typeof detail === 'object' && detail?.error === 'UNIFORM_IN_USE') {
    throw new UniformInUseError(detail.message || fallback, detail.zones || [])
  }
  if (typeof detail === 'string') {
    throw new Error(detail)
  }
  if (Array.isArray(detail)) {
    throw new Error(detail.map((item) => item.msg || item).join(', '))
  }
  throw new Error(fallback)
}

export async function listUniforms() {
  const response = await apiFetch('/uniforms')
  if (!response.ok) {
    throw new Error('Không tải được danh sách uniform')
  }
  return response.json()
}

export async function getUniformUsage(uniformId) {
  const response = await apiFetch(`/uniforms/${encodeURIComponent(uniformId)}/usage`)
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throwApiError(error, 'Không tải được thông tin sử dụng uniform')
  }
  return response.json()
}

export async function deleteUniform(uniformId) {
  const response = await apiFetch(`/uniforms/${encodeURIComponent(uniformId)}`, {
    method: 'DELETE',
  })
  if (response.ok || response.status === 204) {
    return
  }
  const error = await response.json().catch(() => ({}))
  throwApiError(error, 'Không xóa được uniform')
}
