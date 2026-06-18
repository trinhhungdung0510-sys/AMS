import { cameras } from './mockData'
import { FARM_MAP_ZONES } from './farmControlDashboard'

export const GIS_STORAGE_KEY = 'ams-farm-gis-editor-v2'
export const TEMPLATE_STORAGE_KEY = 'ams-farm-gis-template-v1'

export const FARM_CENTER = [10.9321, 106.8521]
export const FARM_ZOOM = 17
const PCT_SCALE = 0.00018

export const TILE_LAYERS = {
  satellite: {
    id: 'satellite',
    label: 'Vệ tinh',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri',
  },
  street: {
    id: 'street',
    label: 'Bản đồ',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; OpenStreetMap',
  },
  hybrid: {
    id: 'hybrid',
    label: 'Vệ tinh + Nhãn',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    overlayUrl: 'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    overlayOpacity: 0.75,
    attribution: 'Esri + OSM',
  },
}

export const ATSH_LEVELS = {
  green: { label: 'An toàn', color: '#16a34a' },
  yellow: { label: 'Cần chú ý', color: '#eab308' },
  orange: { label: 'Nguy cơ', color: '#f97316' },
  red: { label: 'Nguy cơ cao', color: '#dc2626' },
}

export const ATSH_ZONE_TYPES = {
  clean: { label: 'Vùng sạch', color: '#16a34a', fill: 'rgba(22,163,74,0.28)' },
  buffer: { label: 'Vùng trung gian', color: '#eab308', fill: 'rgba(234,179,8,0.25)' },
  dirty: { label: 'Vùng bẩn', color: '#f97316', fill: 'rgba(249,115,22,0.28)' },
  forbidden: { label: 'Vùng cấm', color: '#dc2626', fill: 'rgba(220,38,38,0.3)' },
  sanitation: { label: 'Vùng sát trùng', color: '#2563eb', fill: 'rgba(37,99,235,0.25)' },
  quarantine: { label: 'Vùng cách ly', color: '#9333ea', fill: 'rgba(147,51,234,0.28)' },
}

export const FARM_OBJECT_TYPES = [
  { type: 'gate-in', label: 'Cổng vào', icon: '🚪', atshZoneType: 'dirty', defaultW: 0.00025, defaultH: 0.00035 },
  { type: 'gate-out', label: 'Cổng ra', icon: '🚪', atshZoneType: 'buffer', defaultW: 0.00025, defaultH: 0.00035 },
  { type: 'guard', label: 'Nhà bảo vệ', icon: '🛡️', atshZoneType: 'buffer', defaultW: 0.0003, defaultH: 0.00035 },
  { type: 'shower', label: 'Nhà tắm', icon: '🚿', atshZoneType: 'sanitation', defaultW: 0.00035, defaultH: 0.0004 },
  { type: 'cafeteria', label: 'Nhà ăn', icon: '🍽️', atshZoneType: 'buffer', defaultW: 0.00035, defaultH: 0.0004 },
  { type: 'feed', label: 'Kho cám', icon: '🌾', atshZoneType: 'dirty', defaultW: 0.00035, defaultH: 0.0004 },
  { type: 'medicine', label: 'Kho thuốc', icon: '💊', atshZoneType: 'forbidden', defaultW: 0.0003, defaultH: 0.00035 },
  { type: 'supply', label: 'Kho vật tư', icon: '📦', atshZoneType: 'buffer', defaultW: 0.0003, defaultH: 0.00035 },
  { type: 'person-quarantine', label: 'Khu cách ly người', icon: '👤', atshZoneType: 'quarantine', defaultW: 0.0004, defaultH: 0.0005 },
  { type: 'pig-quarantine', label: 'Chuồng cách ly heo', icon: '🐷', atshZoneType: 'quarantine', defaultW: 0.00045, defaultH: 0.00055 },
  { type: 'gestation', label: 'Chuồng nái', icon: '🐖', atshZoneType: 'clean', defaultW: 0.0005, defaultH: 0.0006 },
  { type: 'farrowing', label: 'Chuồng đẻ', icon: '🐷', atshZoneType: 'clean', defaultW: 0.0005, defaultH: 0.0006 },
  { type: 'nursery', label: 'Chuồng cai sữa', icon: '🍼', atshZoneType: 'clean', defaultW: 0.00045, defaultH: 0.0005 },
  { type: 'finisher', label: 'Chuồng thịt', icon: '🥩', atshZoneType: 'clean', defaultW: 0.00045, defaultH: 0.0005 },
  { type: 'pig-export', label: 'Khu xuất bán', icon: '🚛', atshZoneType: 'buffer', defaultW: 0.0004, defaultH: 0.00045 },
  { type: 'camera', label: 'Camera', icon: '📷', atshZoneType: 'clean', defaultW: 0.00008, defaultH: 0.00008 },
]

export const LINKABLE_ZONE_TYPES = [
  'gate-in', 'gate-out', 'shower', 'feed', 'medicine', 'supply',
  'person-quarantine', 'pig-quarantine', 'gestation', 'farrowing',
  'nursery', 'finisher', 'pig-export',
]

const TYPE_LOOKUP = Object.fromEntries(FARM_OBJECT_TYPES.map((item) => [item.type, item]))

export function pctToLatLng(x, y, center = FARM_CENTER) {
  return [center[0] - (y - 50) * PCT_SCALE, center[1] + (x - 50) * PCT_SCALE]
}

export function getRotatedCorners(obj) {
  const { x: lat, y: lng, width, height, rotation } = obj
  const halfW = width / 2
  const halfH = height / 2
  const rad = (rotation * Math.PI) / 180
  const local = [[-halfW, -halfH], [halfW, -halfH], [halfW, halfH], [-halfW, halfH]]
  return local.map(([dw, dh]) => {
    const rx = dw * Math.cos(rad) - dh * Math.sin(rad)
    const ry = dw * Math.sin(rad) + dh * Math.cos(rad)
    return [lat + rx, lng + ry]
  })
}

export function offsetLatLng(lat, lng, bearingDeg, distance = 0.00022) {
  const rad = (bearingDeg * Math.PI) / 180
  const latRad = (lat * Math.PI) / 180
  return [lat + distance * Math.cos(rad), lng + (distance * Math.sin(rad)) / Math.cos(latRad)]
}

export function getCameraFovPolygon(obj) {
  const direction = obj.cameraDirection ?? 90
  const fov = obj.cameraFov ?? 60
  const half = fov / 2
  const points = [[obj.x, obj.y]]
  for (let angle = direction - half; angle <= direction + half; angle += 8) {
    points.push(offsetLatLng(obj.x, obj.y, angle))
  }
  return points
}

export function createObjectFromType(objectType, lat, lng) {
  const meta = TYPE_LOOKUP[objectType] || FARM_OBJECT_TYPES[0]
  const id = `MAP-${Date.now().toString(36).toUpperCase()}`
  const isCamera = objectType === 'camera'
  const cam = isCamera ? cameras[Math.floor(Math.random() * cameras.length)] : null

  return {
    id,
    objectType,
    name: isCamera ? cam.name : meta.label,
    zone: cam?.zone || '',
    description: '',
    x: lat,
    y: lng,
    width: meta.defaultW,
    height: meta.defaultH,
    rotation: 0,
    atshZoneType: meta.atshZoneType,
    atshLevel: 'green',
    linkedCameraId: isCamera ? cam.id : null,
    linkedZoneId: null,
    cameraDirection: isCamera ? 90 : null,
    cameraFov: isCamera ? 60 : null,
    status: isCamera ? cam.status : 'active',
  }
}

export function duplicateObject(obj) {
  return {
    ...obj,
    id: `MAP-${Date.now().toString(36).toUpperCase()}`,
    x: obj.x + 0.00008,
    y: obj.y + 0.00008,
    name: `${obj.name} (bản sao)`,
  }
}

export function getDefaultEditorState() {
  const objects = FARM_MAP_ZONES.map((zone) => {
    const type = TYPE_LOOKUP[zone.id] ? zone.id : 'gestation'
    const [lat, lng] = pctToLatLng(zone.x + zone.width / 2, zone.y + zone.height / 2)
    const meta = TYPE_LOOKUP[type]
    return {
      id: `obj-${zone.id}`,
      objectType: type,
      name: zone.name,
      zone: zone.name,
      description: `Khu vực ${zone.name}`,
      x: lat,
      y: lng,
      width: meta.defaultW,
      height: meta.defaultH,
      rotation: 0,
      atshZoneType: meta.atshZoneType,
      atshLevel: zone.risk === 'risk' ? 'red' : zone.risk === 'attention' ? 'yellow' : 'green',
      linkedCameraId: null,
      linkedZoneId: null,
      cameraDirection: null,
      cameraFov: null,
      status: 'active',
    }
  })

  cameras.slice(0, 4).forEach((cam, index) => {
    const anchor = objects[index % objects.length]
    objects.push({
      ...createObjectFromType('camera', anchor.x + 0.00006, anchor.y + 0.00006),
      id: `cam-${cam.id}`,
      name: cam.name,
      linkedCameraId: cam.id,
      linkedZoneId: anchor.id,
      cameraDirection: [45, 90, 135, 180][index % 4],
      status: cam.status,
    })
  })

  return {
    layout: {
      id: 'local',
      name: 'Bản đồ trang trại',
      centerLat: FARM_CENTER[0],
      centerLng: FARM_CENTER[1],
      zoom: FARM_ZOOM,
      baseLayer: 'satellite',
      isTemplate: false,
    },
    objects,
  }
}

export function loadLocalEditorState() {
  try {
    const raw = localStorage.getItem(GIS_STORAGE_KEY)
    if (!raw) return getDefaultEditorState()
    return JSON.parse(raw)
  } catch {
    return getDefaultEditorState()
  }
}

export function saveLocalEditorState(state) {
  localStorage.setItem(GIS_STORAGE_KEY, JSON.stringify(state))
}

export function saveLocalTemplate(state) {
  localStorage.setItem(TEMPLATE_STORAGE_KEY, JSON.stringify(state))
}

export function loadLocalTemplate() {
  try {
    const raw = localStorage.getItem(TEMPLATE_STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function createHistory(initialState) {
  return {
    past: [],
    present: structuredClone(initialState),
    future: [],
  }
}

export function historyCommit(history, nextPresent) {
  return {
    past: [...history.past, history.present],
    present: structuredClone(nextPresent),
    future: [],
  }
}

export function historyUndo(history) {
  if (!history.past.length) return history
  const previous = history.past[history.past.length - 1]
  return {
    past: history.past.slice(0, -1),
    present: previous,
    future: [history.present, ...history.future],
  }
}

export function historyRedo(history) {
  if (!history.future.length) return history
  const next = history.future[0]
  return {
    past: [...history.past, history.present],
    present: next,
    future: history.future.slice(1),
  }
}

export function exportEditorToPng(objects) {
  const canvas = document.createElement('canvas')
  canvas.width = 1600
  canvas.height = 900
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.fillStyle = '#1a3a1a'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  const project = (lat, lng) => {
    const x = ((lng - FARM_CENTER[1]) / PCT_SCALE + 50) / 100
    const y = (50 - (lat - FARM_CENTER[0]) / PCT_SCALE) / 100
    return [x * canvas.width, y * canvas.height]
  }

  objects.filter((o) => o.objectType !== 'camera').forEach((obj) => {
    const meta = ATSH_ZONE_TYPES[obj.atshZoneType] || ATSH_ZONE_TYPES.buffer
    const corners = getRotatedCorners(obj)
    ctx.beginPath()
    corners.forEach(([lat, lng], index) => {
      const [x, y] = project(lat, lng)
      if (index === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.closePath()
    ctx.fillStyle = meta.fill
    ctx.strokeStyle = meta.color
    ctx.lineWidth = 2
    ctx.fill()
    ctx.stroke()
    const [cx, cy] = project(obj.x, obj.y)
    ctx.fillStyle = '#fff'
    ctx.font = 'bold 12px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText(obj.name, cx, cy)
  })

  const link = document.createElement('a')
  link.download = 'ban-do-trang-trai.png'
  link.href = canvas.toDataURL('image/png')
  link.click()
}
