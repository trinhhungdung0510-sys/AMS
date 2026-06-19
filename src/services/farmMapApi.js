import { API_BASE_URL } from '../config/api'

const API_BASE = `${API_BASE_URL}/api/map`

export async function fetchActiveFarmMap() {
  const res = await fetch(`${API_BASE}/active`)
  if (!res.ok) return null
  return res.json()
}

export async function saveFarmMap(payload) {
  const res = await fetch(`${API_BASE}/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Không thể lưu bản đồ')
  return res.json()
}

export async function deleteFarmMapObject(objectId) {
  const res = await fetch(`${API_BASE}/objects/${objectId}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Không thể xóa đối tượng')
  return res.json()
}

export function toApiPayload(layout, objects) {
  return {
    layout: {
      farm_id: 'FARM-001',
      name: layout.name,
      is_template: layout.isTemplate || false,
      center_lat: layout.centerLat,
      center_lng: layout.centerLng,
      zoom: layout.zoom,
      base_layer: layout.baseLayer,
    },
    objects: objects.map((obj) => ({
      id: obj.id,
      object_type: obj.objectType,
      name: obj.name,
      zone: obj.zone || '',
      description: obj.description || '',
      x: obj.x,
      y: obj.y,
      width: obj.width,
      height: obj.height,
      rotation: obj.rotation,
      atsh_zone_type: obj.atshZoneType,
      atsh_level: obj.atshLevel,
      linked_camera_id: obj.linkedCameraId || null,
      linked_zone_id: obj.linkedZoneId || null,
      camera_direction: obj.objectType === 'camera' ? obj.cameraDirection : null,
      camera_fov: obj.objectType === 'camera' ? obj.cameraFov : null,
      status: obj.status || 'active',
    })),
  }
}

export function fromApiResponse(data) {
  if (!data) return null
  return {
    layout: {
      id: data.layout.id,
      name: data.layout.name,
      centerLat: data.layout.center_lat,
      centerLng: data.layout.center_lng,
      zoom: data.layout.zoom,
      baseLayer: data.layout.base_layer,
      isTemplate: data.layout.is_template,
    },
    objects: data.objects.map((obj) => ({
      id: obj.id,
      objectType: obj.object_type,
      name: obj.name,
      zone: obj.zone,
      description: obj.description,
      x: obj.x,
      y: obj.y,
      width: obj.width,
      height: obj.height,
      rotation: obj.rotation,
      atshZoneType: obj.atsh_zone_type,
      atshLevel: obj.atsh_level,
      linkedCameraId: obj.linked_camera_id,
      linkedZoneId: obj.linked_zone_id,
      cameraDirection: obj.camera_direction ?? 90,
      cameraFov: obj.camera_fov ?? 60,
      status: obj.status,
    })),
  }
}
