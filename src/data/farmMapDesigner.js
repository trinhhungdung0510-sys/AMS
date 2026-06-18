import { cameras } from './mockData'
import { FARM_MAP_ZONES } from './farmControlDashboard'

export const STORAGE_KEY = 'ams-farm-map-design-v1'

export const ATSH_LEVELS = {
  green: { label: 'An toàn', color: '#16a34a', tone: 'green' },
  yellow: { label: 'Cần chú ý', color: '#eab308', tone: 'yellow' },
  orange: { label: 'Nguy cơ', color: '#f97316', tone: 'orange' },
  red: { label: 'Nguy cơ cao', color: '#dc2626', tone: 'red' },
}

export const PALETTE_ITEMS = [
  { type: 'gate-in', label: 'Cổng vào', category: 'zone', atshLevel: 'yellow', w: 12, h: 10 },
  { type: 'gate-out', label: 'Cổng ra', category: 'zone', atshLevel: 'yellow', w: 12, h: 10 },
  { type: 'guard', label: 'Nhà bảo vệ', category: 'zone', atshLevel: 'yellow', w: 12, h: 10 },
  { type: 'shower', label: 'Nhà tắm', category: 'zone', atshLevel: 'yellow', w: 12, h: 10 },
  { type: 'cafeteria', label: 'Nhà ăn', category: 'zone', atshLevel: 'yellow', w: 12, h: 10 },
  { type: 'person-quarantine', label: 'Khu cách ly người', category: 'zone', atshLevel: 'orange', w: 14, h: 12 },
  { type: 'pig-quarantine', label: 'Chuồng cách ly heo', category: 'zone', atshLevel: 'red', w: 16, h: 12 },
  { type: 'gestation', label: 'Chuồng nái', category: 'zone', atshLevel: 'green', w: 16, h: 14 },
  { type: 'farrowing', label: 'Chuồng đẻ', category: 'zone', atshLevel: 'green', w: 16, h: 14 },
  { type: 'nursery', label: 'Chuồng cai sữa', category: 'zone', atshLevel: 'green', w: 14, h: 12 },
  { type: 'finisher', label: 'Chuồng heo thịt', category: 'zone', atshLevel: 'green', w: 14, h: 12 },
  { type: 'feed', label: 'Kho cám', category: 'zone', atshLevel: 'orange', w: 12, h: 10 },
  { type: 'medicine', label: 'Kho thuốc', category: 'zone', atshLevel: 'red', w: 12, h: 10 },
  { type: 'supply', label: 'Kho vật tư', category: 'zone', atshLevel: 'yellow', w: 12, h: 10 },
  { type: 'pig-export', label: 'Khu xuất bán heo', category: 'zone', atshLevel: 'orange', w: 14, h: 10 },
  { type: 'camera', label: 'Camera', category: 'camera', atshLevel: 'green', w: 4, h: 4 },
]

export const FLOW_TYPES = [
  { type: 'worker', label: 'Luồng công nhân', color: '#0B6B1B' },
  { type: 'guest', label: 'Luồng khách', color: '#2563eb' },
  { type: 'feed_truck', label: 'Luồng xe cám', color: '#f97316' },
  { type: 'pig_truck', label: 'Luồng xe bắt heo', color: '#9333ea' },
  { type: 'pig_export', label: 'Luồng heo xuất bán', color: '#dc2626' },
]

export const MAP_PRESETS = {
  '300': { label: 'Trại 300 nái', scale: 0.85 },
  '600': { label: 'Trại 600 nái', scale: 1 },
  '1200': { label: 'Trại 1200 nái', scale: 1.15 },
  boar: { label: 'Trại đực giống', scale: 0.9 },
  semen: { label: 'Trại sản xuất tinh', scale: 0.95 },
}

const RISK_TO_ATSH = { safe: 'green', attention: 'yellow', risk: 'red' }

function zoneToObject(zone, index) {
  return {
    id: `obj-${zone.id}`,
    type: zone.id,
    name: zone.name,
    category: 'zone',
    description: `Khu vực ${zone.name}`,
    atshLevel: RISK_TO_ATSH[zone.risk] || 'green',
    linkedCameraId: '',
    x: zone.x,
    y: zone.y,
    width: zone.width,
    height: zone.height,
    rotation: 0,
  }
}

export function createDefaultObjects() {
  return FARM_MAP_ZONES.map(zoneToObject)
}

export function createDefaultFlows() {
  return [{
    id: 'flow-worker-default',
    flowType: 'worker',
    name: 'Luồng công nhân ATSH',
    points: [[22, 78], [22, 62], [30, 62], [36, 20]],
    labels: ['Nhà tắm', 'Thay đồ', 'Sát trùng', 'Chuồng nái'],
    valid: true,
  }]
}

export function createDefaultCamerasOnMap() {
  return cameras.slice(0, 6).map((cam, index) => ({
    id: `cam-obj-${cam.id}`,
    type: 'camera',
    name: cam.name,
    category: 'camera',
    description: `Camera giám sát ${cam.zone}`,
    atshLevel: 'green',
    linkedCameraId: cam.id,
    cameraId: cam.id,
    direction: [0, 45, 90, 135, 180, 270][index % 6],
    fov: 60,
    status: cam.status,
    x: 8 + (index * 14) % 80,
    y: 8 + Math.floor(index / 5) * 20,
    width: 4,
    height: 4,
    rotation: 0,
  }))
}

export function getDefaultMapState() {
  return {
    objects: [...createDefaultObjects(), ...createDefaultCamerasOnMap()],
    flows: createDefaultFlows(),
  }
}

export function loadMapState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return getDefaultMapState()
    return JSON.parse(raw)
  } catch {
    return getDefaultMapState()
  }
}

export function saveMapState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}

export function applyPreset(presetKey) {
  const preset = MAP_PRESETS[presetKey]
  const base = getDefaultMapState()
  const scale = preset?.scale || 1
  return {
    objects: base.objects.map((obj) => ({
      ...obj,
      x: Math.min(88, obj.x * scale),
      y: Math.min(88, obj.y * scale),
      width: Math.min(24, obj.width * scale),
      height: Math.min(24, obj.height * scale),
    })),
    flows: base.flows,
    preset: presetKey,
  }
}

export function paletteMeta(type) {
  return PALETTE_ITEMS.find((item) => item.type === type) || PALETTE_ITEMS[0]
}

export function createObjectFromPalette(type, x, y) {
  const meta = paletteMeta(type)
  const id = `obj-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`

  if (type === 'camera') {
    const cam = cameras[Math.floor(Math.random() * cameras.length)]
    return {
      id,
      type: 'camera',
      name: cam.name,
      category: 'camera',
      description: '',
      atshLevel: 'green',
      linkedCameraId: cam.id,
      cameraId: cam.id,
      direction: 90,
      fov: 60,
      status: cam.status,
      x: Math.max(0, Math.min(94, x - 2)),
      y: Math.max(0, Math.min(94, y - 2)),
      width: meta.w,
      height: meta.h,
      rotation: 0,
    }
  }

  return {
    id,
    type,
    name: meta.label,
    category: 'zone',
    description: '',
    atshLevel: meta.atshLevel,
    linkedCameraId: '',
    x: Math.max(0, Math.min(90, x - meta.w / 2)),
    y: Math.max(0, Math.min(90, y - meta.h / 2)),
    width: meta.w,
    height: meta.h,
    rotation: 0,
  }
}

export function exportMapToPng(objects, flows) {
  const canvas = document.createElement('canvas')
  canvas.width = 1600
  canvas.height = 900
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.fillStyle = '#f7fbf8'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  objects.forEach((obj) => {
    const level = ATSH_LEVELS[obj.atshLevel] || ATSH_LEVELS.green
    const x = (obj.x / 100) * canvas.width
    const y = (obj.y / 100) * canvas.height
    const w = (obj.width / 100) * canvas.width
    const h = (obj.height / 100) * canvas.height
    ctx.save()
    ctx.translate(x + w / 2, y + h / 2)
    ctx.rotate((obj.rotation || 0) * Math.PI / 180)
    ctx.fillStyle = `${level.color}33`
    ctx.strokeStyle = level.color
    ctx.lineWidth = 3
    ctx.fillRect(-w / 2, -h / 2, w, h)
    ctx.strokeRect(-w / 2, -h / 2, w, h)
    ctx.fillStyle = '#0f172a'
    ctx.font = 'bold 14px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText(obj.name, 0, 4)
    ctx.restore()
  })

  flows.forEach((flow) => {
    const flowMeta = FLOW_TYPES.find((item) => item.type === flow.flowType) || FLOW_TYPES[0]
    ctx.strokeStyle = flowMeta.color
    ctx.lineWidth = 4
    ctx.beginPath()
    flow.points.forEach(([px, py], index) => {
      const x = (px / 100) * canvas.width
      const y = (py / 100) * canvas.height
      if (index === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.stroke()
  })

  const link = document.createElement('a')
  link.download = 'ban-do-trang-trai.png'
  link.href = canvas.toDataURL('image/png')
  link.click()
}
