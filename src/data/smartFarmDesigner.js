import {
  ATSH_LEVELS,
  ATSH_ZONE_TYPES,
  FARM_CENTER,
  FARM_OBJECT_TYPES,
  FARM_ZOOM,
  createHistory,
  createObjectFromType,
  duplicateObject,
  getDefaultEditorState,
  getRotatedCorners,
  historyCommit,
  historyRedo,
  historyUndo,
} from './farmGisMap'

export const DESIGNER_STORAGE_KEY = 'ams-smart-farm-designer-v1'
export const DESIGNER_TEMPLATE_KEY = 'ams-smart-farm-template-v1'

export {
  ATSH_LEVELS,
  ATSH_ZONE_TYPES,
  FARM_CENTER,
  FARM_OBJECT_TYPES,
  FARM_ZOOM,
  createHistory,
  createObjectFromType,
  duplicateObject,
  getRotatedCorners,
  historyCommit,
  historyRedo,
  historyUndo,
}

export const FLOW_TYPES = [
  { type: 'worker', label: 'Công nhân', color: '#0B6B1B' },
  { type: 'guest', label: 'Khách', color: '#2563eb' },
  { type: 'feed_truck', label: 'Xe cám', color: '#f97316' },
  { type: 'pig_truck', label: 'Xe bắt heo', color: '#9333ea' },
  { type: 'pig_export', label: 'Heo xuất bán', color: '#dc2626' },
]

export const HEATMAP_COLORS = {
  green: { label: 'An toàn', color: '#16a34a', fill: 'rgba(22,163,74,0.45)' },
  yellow: { label: 'Cần chú ý', color: '#eab308', fill: 'rgba(234,179,8,0.45)' },
  red: { label: 'Nguy cơ cao', color: '#dc2626', fill: 'rgba(220,38,38,0.5)' },
}

export const DEFAULT_LAYERS = {
  objects: true,
  cameras: true,
  atsh: true,
  routes: true,
  heatmap: false,
}

const BARN_TYPES = ['gestation', 'farrowing', 'nursery', 'finisher', 'pig-quarantine']
const R = 6371000

export function haversineMeters(lat1, lng1, lat2, lng2) {
  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLng = ((lng2 - lng1) * Math.PI) / 180
  const a = Math.sin(dLat / 2) ** 2
    + Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) * Math.sin(dLng / 2) ** 2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

export function polylineLengthMeters(points) {
  let total = 0
  for (let i = 1; i < points.length; i += 1) {
    total += haversineMeters(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])
  }
  return total
}

export function objectAreaSqMeters(obj) {
  const latM = obj.width * 111320
  const lngM = obj.height * 111320 * Math.cos((obj.x * Math.PI) / 180)
  return Math.abs(latM * lngM)
}

export function objectDimensionsMeters(obj) {
  return {
    lengthM: Math.round(obj.width * 111320),
    widthM: Math.round(obj.height * 111320 * Math.cos((obj.x * Math.PI) / 180)),
    areaM2: Math.round(objectAreaSqMeters(obj)),
  }
}

export function computeStats(objects, routes) {
  return {
    totalBarns: objects.filter((item) => BARN_TYPES.includes(item.objectType)).length,
    totalCameras: objects.filter((item) => item.objectType === 'camera').length,
    totalAtshZones: new Set(objects.map((item) => item.atshZoneType)).size,
    totalRoutes: routes.length,
  }
}

function pointInPolygon(point, polygon) {
  const [x, y] = point
  let inside = false
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i, i += 1) {
    const xi = polygon[i][0]
    const yi = polygon[i][1]
    const xj = polygon[j][0]
    const yj = polygon[j][1]
    const intersect = ((yi > y) !== (yj > y)) && (x < ((xj - xi) * (y - yi)) / (yj - yi + 1e-12) + xi)
    if (intersect) inside = !inside
  }
  return inside
}

export function evaluateAtsh(objects, routes) {
  let score = 100
  const risks = []
  const recommendations = []

  const zones = objects.filter((item) => item.objectType !== 'camera')
  const cameras = objects.filter((item) => item.objectType === 'camera')
  const cleanZones = zones.filter((item) => item.atshZoneType === 'clean')
  const dirtyZones = zones.filter((item) => item.atshZoneType === 'dirty')
  const forbiddenZones = zones.filter((item) => item.atshZoneType === 'forbidden')
  const sanitationZones = zones.filter((item) => item.atshZoneType === 'sanitation')
  const quarantineZones = zones.filter((item) => item.atshZoneType === 'quarantine')

  if (!sanitationZones.length) {
    score -= 18
    risks.push('Thiếu vùng sát trùng bắt buộc')
    recommendations.push('Bổ sung Nhà tắm / khu sát trùng trước khu sạch')
  }

  if (cleanZones.length && !cameras.some((cam) => cleanZones.some((zone) => cam.linkedZoneId === zone.id))) {
    score -= 10
    risks.push('Khu sạch chưa có camera giám sát')
    recommendations.push('Gắn camera vào chuồng nái, chuồng đẻ hoặc chuồng thịt')
  }

  if (quarantineZones.length && !cameras.some((cam) => quarantineZones.some((zone) => cam.linkedZoneId === zone.id))) {
    score -= 12
    risks.push('Khu cách ly chưa có camera')
    recommendations.push('Gắn camera giám sát chuồng cách ly heo')
  }

  routes.forEach((route) => {
    if (route.points.length < 2) return
    forbiddenZones.forEach((zone) => {
      const poly = getRotatedCorners(zone)
      const crosses = route.points.some((point) => pointInPolygon(point, poly))
      if (crosses) {
        score -= 15
        risks.push(`Luồng ${route.name} đi qua vùng cấm`)
        recommendations.push(`Điều chỉnh luồng ${route.name} tránh ${zone.name}`)
      }
    })

    if (route.routeType === 'worker') {
      const startsDirty = dirtyZones.some((zone) => pointInPolygon(route.points[0], getRotatedCorners(zone)))
      const endsClean = cleanZones.some((zone) => pointInPolygon(route.points[route.points.length - 1], getRotatedCorners(zone)))
      const passesSanitation = sanitationZones.some((zone) => {
        const poly = getRotatedCorners(zone)
        return route.points.some((point) => pointInPolygon(point, poly))
      })
      if (startsDirty && endsClean && !passesSanitation) {
        score -= 20
        risks.push('Luồng công nhân: bẩn → sạch không qua sát trùng')
        recommendations.push('Luồng công nhân: Nhà tắm → Thay đồ → Sát trùng → Chuồng')
      }
    }
  })

  dirtyZones.forEach((dirty) => {
    cleanZones.forEach((clean) => {
      const dist = haversineMeters(dirty.x, dirty.y, clean.x, clean.y)
      if (dist < 8 && !sanitationZones.some((san) => haversineMeters(san.x, san.y, dirty.x, dirty.y) < 12)) {
        score -= 8
        risks.push(`${dirty.name} quá gần ${clean.name} mà thiếu vùng trung gian/sát trùng`)
        recommendations.push(`Thêm vùng trung gian hoặc sát trùng giữa ${dirty.name} và ${clean.name}`)
      }
    })
  })

  const uniqueRisks = [...new Set(risks)]
  const uniqueRecs = [...new Set(recommendations)]

  return {
    score: Math.max(0, Math.min(100, score)),
    riskScore: Math.max(0, 100 - Math.max(0, Math.min(100, score))),
    risks: uniqueRisks.length ? uniqueRisks : ['Không phát hiện nguy cơ nghiêm trọng'],
    recommendations: uniqueRecs.length ? uniqueRecs : ['Duy trì quy trình ATSH hiện tại'],
  }
}

export function getDefaultDesignerState() {
  const base = getDefaultEditorState()
  return {
    layout: {
      ...base.layout,
      name: 'Sơ đồ trang trại AMS',
      address: 'Ấp Bình Minh, Xã Long Thành, Đồng Nai',
    },
    objects: base.objects,
    routes: [{
      id: 'route-worker-1',
      routeType: 'worker',
      name: 'Luồng công nhân',
      points: base.objects
        .filter((item) => ['shower', 'gestation'].includes(item.objectType))
        .map((item) => [item.x, item.y]),
      labels: ['Nhà tắm', 'Chuồng nái'],
      valid: true,
    }],
    layers: DEFAULT_LAYERS,
  }
}

export function loadDesignerState() {
  try {
    const raw = localStorage.getItem(DESIGNER_STORAGE_KEY)
    if (!raw) return getDefaultDesignerState()
    return JSON.parse(raw)
  } catch {
    return getDefaultDesignerState()
  }
}

export function saveDesignerState(state) {
  localStorage.setItem(DESIGNER_STORAGE_KEY, JSON.stringify(state))
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('ams-farm-map-updated', { detail: state }))
  }
}

export function saveDesignerTemplate(state) {
  localStorage.setItem(DESIGNER_TEMPLATE_KEY, JSON.stringify(state))
}

export async function geocodeAddress(address) {
  const query = encodeURIComponent(address)
  const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${query}`, {
    headers: { 'Accept-Language': 'vi' },
  })
  if (!res.ok) return null
  const data = await res.json()
  if (!data.length) return null
  return {
    lat: Number(data[0].lat),
    lng: Number(data[0].lon),
    label: data[0].display_name,
  }
}

export function exportDesignerPng(objects, routes) {
  const canvas = document.createElement('canvas')
  canvas.width = 1600
  canvas.height = 900
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.fillStyle = '#0f2912'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  const center = FARM_CENTER
  const scale = 0.00018
  const project = (lat, lng) => {
    const x = ((lng - center[1]) / scale + 50) / 100
    const y = (50 - (lat - center[0]) / scale) / 100
    return [x * canvas.width, y * canvas.height]
  }

  objects.filter((item) => item.objectType !== 'camera').forEach((obj) => {
    const heat = HEATMAP_COLORS[obj.atshLevel] || HEATMAP_COLORS.green
    const corners = getRotatedCorners(obj)
    ctx.beginPath()
    corners.forEach(([lat, lng], index) => {
      const [x, y] = project(lat, lng)
      if (index === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.closePath()
    ctx.fillStyle = heat.fill
    ctx.strokeStyle = heat.color
    ctx.lineWidth = 2
    ctx.fill()
    ctx.stroke()
  })

  routes.forEach((route) => {
    const meta = FLOW_TYPES.find((item) => item.type === route.routeType) || FLOW_TYPES[0]
    ctx.strokeStyle = meta.color
    ctx.lineWidth = 3
    ctx.beginPath()
    route.points.forEach(([lat, lng], index) => {
      const [x, y] = project(lat, lng)
      if (index === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.stroke()
  })

  const link = document.createElement('a')
  link.download = 'so-do-trang-trai-ams.png'
  link.href = canvas.toDataURL('image/png')
  link.click()
}
