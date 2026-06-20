import { apiFetch } from './apiClient'

function parseApiError(data, fallback) {
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg || item).join(', ')
  }
  return fallback
}

export async function getZones(cameraId) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/zones`)
  if (!response.ok) {
    throw new Error('Không tải được danh sách vùng camera')
  }
  return response.json()
}

export async function createZone(cameraId, data) {
  const response = await apiFetch(`/cameras/${encodeURIComponent(cameraId)}/zones`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(parseApiError(error, 'Không tạo được vùng'))
  }
  return response.json()
}

export async function updateZone(id, data) {
  const response = await apiFetch(`/zones/${encodeURIComponent(id)}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(parseApiError(error, 'Không cập nhật được vùng'))
  }
  return response.json()
}

export async function deleteZone(id) {
  const response = await apiFetch(`/zones/${encodeURIComponent(id)}`, {
    method: 'DELETE',
  })
  if (!response.ok && response.status !== 404) {
    throw new Error('Không xóa được vùng')
  }
}

export function buildZoneTree(zones) {
  const roots = zones.filter((zone) => !zone.parent_zone_id)
  const knownRootIds = new Set(roots.map((zone) => zone.id))

  const tree = roots.map((root) => ({
    ...root,
    subzones: zones.filter((zone) => zone.parent_zone_id === root.id),
  }))

  // SubZone mồ côi (parent bị xóa) vẫn hiển thị ở cấp root để tránh mất dữ liệu trên UI
  const orphans = zones.filter(
    (zone) => zone.parent_zone_id && !knownRootIds.has(zone.parent_zone_id),
  )
  orphans.forEach((zone) => {
    tree.push({ ...zone, subzones: [], orphaned: true })
  })

  return tree
}
