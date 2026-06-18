const API_BASE = 'http://127.0.0.1:8000/api/smart-farm'

export async function fetchSmartFarmDesigner() {
  const res = await fetch(`${API_BASE}/designer`)
  if (!res.ok) return null
  return res.json()
}

export async function saveSmartFarmDesigner(payload) {
  const res = await fetch(`${API_BASE}/designer/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Không thể lưu sơ đồ')
  return res.json()
}

export function toApiPayload(state) {
  const { layout, objects, routes, layers } = state
  return {
    layout: {
      farm_id: 'FARM-001',
      name: layout.name,
      address: layout.address || '',
      center_lat: layout.centerLat,
      center_lng: layout.centerLng,
      zoom: layout.zoom,
      base_layer: layout.baseLayer,
      is_template: layout.isTemplate || false,
    },
    objects: objects.map((obj) => ({
      id: obj.id,
      object_type: obj.objectType,
      name: obj.name,
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
    routes: routes.map((route) => ({
      id: route.id,
      route_type: route.routeType,
      name: route.name,
      points: route.points,
      labels: route.labels || [],
      valid: route.valid !== false,
    })),
    layers: Object.entries(layers || {}).map(([layer_key, visible]) => ({
      layer_key,
      visible: Boolean(visible),
      opacity: 1,
    })),
  }
}

export function fromApiResponse(data) {
  if (!data) return null
  const layerMap = {}
  ;(data.layers || []).forEach((item) => {
    layerMap[item.layer_key] = item.visible
  })

  return {
    layout: {
      id: data.layout.id,
      name: data.layout.name,
      address: data.layout.address,
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
    routes: data.routes.map((route) => ({
      id: route.id,
      routeType: route.route_type,
      name: route.name,
      points: route.points,
      labels: route.labels,
      valid: route.valid,
    })),
    layers: { ...layerMap },
  }
}
