export const APP_VERSION = 'v2.0'

export const alertTypes = {
  dress: 'Người không đúng trang phục',
  intrusion: 'Người và động vật xâm nhập vùng cấm',
  fever: 'Heo sốt bất thường',
  immobile: 'Heo nằm bất động kéo dài',
  disconnect: 'Camera mất kết nối',
}

export const alertTypeOptions = Object.entries(alertTypes).map(([value, label]) => ({
  value,
  label,
}))

export const severityLabels = {
  low: 'Thông tin',
  info: 'Thông tin',
  warning: 'Cảnh báo',
  medium: 'Cảnh báo',
  danger: 'Mức cao',
  high: 'Mức cao',
  critical: 'Nghiêm trọng',
}

export const statusLabels = {
  new: 'Mới',
  processing: 'Đang xử lý',
  resolved: 'Đã xử lý',
}

export const pageMeta = {
  dashboard: {
    title: 'Tổng quan',
    subtitle: 'Tổng quan giám sát AI và an toàn sinh học trại heo',
  },
  'bang-dieu-khien': {
    title: 'Bảng điều khiển chủ trại',
    subtitle: 'Điểm ATSH, bản đồ trang trại và vi phạm — cập nhật thời gian thực',
  },
  compliance: {
    title: 'Tuân thủ ATSH',
    subtitle: 'Điểm tuân thủ, xu hướng vi phạm và khu vực rủi ro',
  },
  monitoring: {
    title: 'Giám sát',
    subtitle: 'Lưới camera và cảnh báo AI thời gian thực',
  },
  'compliance-center': {
    title: 'Compliance Center',
    subtitle: 'Trung tâm bằng chứng vi phạm tuân thủ — ảnh, vị trí, thời gian',
  },
  camera: {
    title: 'Camera',
    subtitle: 'Danh sách và cấu hình camera trong trang trại',
  },
  cameraDetail: {
    title: 'Chi tiết camera',
    subtitle: 'Luồng video, thông tin thiết bị và cảnh báo AI',
  },
  events: {
    title: 'Sự kiện',
    subtitle: 'Bảng cảnh báo AI với tìm kiếm, lọc và xuất Excel',
  },
  violations: {
    title: 'Trung tâm vi phạm ATSH',
    subtitle: 'Giám sát và xử lý vi phạm an toàn sinh học theo thời gian thực',
  },
  'vi-pham-atsh': {
    title: 'Vi phạm ATSH',
    subtitle: 'Trung tâm quản lý vi phạm — chưa xử lý, đã xử lý và xử lý realtime',
  },
  rules: {
    title: 'Quy tắc ATSH',
    subtitle: 'Danh sách quy tắc an toàn sinh học — bật hoặc tắt theo nhu cầu',
  },
  'quy-tac-atsh': {
    title: 'Quy tắc ATSH',
    subtitle: 'Danh sách quy tắc an toàn sinh học — bật hoặc tắt theo nhu cầu',
  },
  map: {
    title: 'Bản đồ trang trại',
    subtitle: 'Bản đồ vận hành ATSH theo khu vực',
  },
  'ban-do-trang-trai': {
    title: 'Bản đồ trang trại',
    subtitle: 'Xem và thiết kế sơ đồ trại trên vệ tinh — khu vực, camera, ATSH, luồng di chuyển',
  },
  settings: {
    title: 'Cài đặt',
    subtitle: 'Người dùng, phân quyền, camera và kênh nhận cảnh báo',
  },
  'thiet-ke-vung-atsh': {
    title: 'Thiết kế vùng ATSH',
    subtitle: 'Chỉnh sửa vùng an toàn sinh học trực tiếp trên hình ảnh camera',
  },
}

export const cameras = [
  {
    id: 'CAM-001',
    name: 'Camera Cổng trại',
    zone: 'Cổng trại',
    ip: '192.168.10.11',
    status: 'online',
    resolution: '1080p',
    uptime: 99.8,
    fps: 30,
    alertsToday: 6,
    risk: 'danger',
    mapX: 14,
    mapY: 70,
  },
  {
    id: 'CAM-002',
    name: 'Camera Khu nái 01',
    zone: 'Khu nái',
    ip: '192.168.10.12',
    status: 'online',
    resolution: '2K',
    uptime: 99.3,
    fps: 25,
    alertsToday: 4,
    risk: 'warning',
    mapX: 43,
    mapY: 33,
  },
  {
    id: 'CAM-003',
    name: 'Camera Khu nái 02',
    zone: 'Khu nái',
    ip: '192.168.10.13',
    status: 'online',
    resolution: '1080p',
    uptime: 98.7,
    fps: 25,
    alertsToday: 2,
    risk: 'warning',
    mapX: 58,
    mapY: 33,
  },
  {
    id: 'CAM-004',
    name: 'Camera Khu đực giống',
    zone: 'Khu đực giống',
    ip: '192.168.10.14',
    status: 'online',
    resolution: '1080p',
    uptime: 97.9,
    fps: 24,
    alertsToday: 3,
    risk: 'danger',
    mapX: 80,
    mapY: 34,
  },
  {
    id: 'CAM-005',
    name: 'Camera Khu cách ly',
    zone: 'Khu cách ly',
    ip: '192.168.10.15',
    status: 'offline',
    resolution: '1080p',
    uptime: 82.1,
    fps: 0,
    alertsToday: 1,
    risk: 'offline',
    mapX: 78,
    mapY: 73,
  },
  {
    id: 'CAM-006',
    name: 'Camera Hành lang chính',
    zone: 'Hành lang chính',
    ip: '192.168.10.16',
    status: 'online',
    resolution: '720p',
    uptime: 99.1,
    fps: 20,
    alertsToday: 0,
    risk: 'online',
    mapX: 50,
    mapY: 58,
  },
  {
    id: 'CAM-007',
    name: 'Camera Khu con',
    zone: 'Khu con',
    ip: '192.168.10.17',
    status: 'online',
    resolution: '1080p',
    uptime: 98.4,
    fps: 24,
    alertsToday: 2,
    risk: 'warning',
    mapX: 27,
    mapY: 34,
  },
  {
    id: 'CAM-008',
    name: 'Camera Kho thức ăn',
    zone: 'Kho thức ăn',
    ip: '192.168.10.18',
    status: 'online',
    resolution: '1080p',
    uptime: 99.6,
    fps: 25,
    alertsToday: 0,
    risk: 'online',
    mapX: 25,
    mapY: 72,
  },
  {
    id: 'CAM-009',
    name: 'Camera Bể xử lý nước',
    zone: 'Xử lý nước',
    ip: '192.168.10.19',
    status: 'online',
    resolution: '720p',
    uptime: 96.5,
    fps: 20,
    alertsToday: 1,
    risk: 'warning',
    mapX: 91,
    mapY: 58,
  },
]

export const users = [
  { id: 'USR-001', name: 'Nguyễn Minh An', email: 'an.nguyen@ams.vn', role: 'Quản trị viên', status: 'active' },
  { id: 'USR-002', name: 'Trần Bảo Long', email: 'long.tran@ams.vn', role: 'Giám sát ca', status: 'active' },
  { id: 'USR-003', name: 'Lê Hoài Nam', email: 'nam.le@ams.vn', role: 'Kỹ thuật camera', status: 'active' },
  { id: 'USR-004', name: 'Phạm Thu Hà', email: 'ha.pham@ams.vn', role: 'Thú y', status: 'active' },
  { id: 'USR-005', name: 'Đặng Quốc Việt', email: 'viet.dang@ams.vn', role: 'Chỉ xem', status: 'inactive' },
]

const eventSeed = [
  ['dress', 'CAM-001', 'warning'],
  ['intrusion', 'CAM-001', 'danger'],
  ['fever', 'CAM-002', 'danger'],
  ['immobile', 'CAM-003', 'critical'],
  ['disconnect', 'CAM-005', 'critical'],
  ['dress', 'CAM-004', 'warning'],
  ['intrusion', 'CAM-007', 'danger'],
  ['fever', 'CAM-009', 'warning'],
  ['immobile', 'CAM-002', 'danger'],
  ['dress', 'CAM-008', 'low'],
]

export const events = Array.from({ length: 50 }, (_, index) => {
  const [type, cameraId, severity] = eventSeed[index % eventSeed.length]
  const camera = cameras.find((item) => item.id === cameraId)
  const day = 17 - (index % 10)
  const hour = 6 + ((index * 3) % 17)
  const minute = (index * 11) % 60
  const user = users[index % users.length]
  const status = ['new', 'processing', 'resolved'][index % 3]

  return {
    id: `EVT-${String(index + 1).padStart(3, '0')}`,
    date: `2026-06-${String(day).padStart(2, '0')}`,
    time: `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`,
    type,
    typeLabel: alertTypes[type],
    cameraId,
    cameraName: camera.name,
    zone: camera.zone,
    severity,
    status,
    handler: status === 'new' ? 'Chưa phân công' : user.name,
    confidence: Math.min(99, 82 + ((index * 7) % 18)),
  }
})

export const violationImages = Array.from({ length: 20 }, (_, index) => {
  const event = events[index]
  return {
    id: `IMG-${String(index + 1).padStart(3, '0')}`,
    eventId: event.id,
    type: event.type,
    typeLabel: event.typeLabel,
    cameraId: event.cameraId,
    cameraName: event.cameraName,
    zone: event.zone,
    time: `${event.date} ${event.time}`,
    confidence: event.confidence,
    severity: event.severity,
    resolved: index % 4 === 0,
  }
})

export const alertTrend = [
  { day: '11/06', alerts: 18 },
  { day: '12/06', alerts: 23 },
  { day: '13/06', alerts: 19 },
  { day: '14/06', alerts: 31 },
  { day: '15/06', alerts: 28 },
  { day: '16/06', alerts: 34 },
  { day: '17/06', alerts: 42 },
]

export const alertDistribution = alertTypeOptions.map((item) => ({
  name: item.label,
  value: events.filter((event) => event.type === item.value).length,
}))

export const farmZones = [
  { id: 'gate', name: 'Cổng trại', x: 5, y: 58, width: 22, height: 30, risk: 'danger' },
  { id: 'sow', name: 'Khu nái', x: 34, y: 18, width: 34, height: 28, risk: 'warning' },
  { id: 'boar', name: 'Khu đực giống', x: 70, y: 18, width: 24, height: 28, risk: 'danger' },
  { id: 'isolation', name: 'Khu cách ly', x: 66, y: 58, width: 28, height: 30, risk: 'offline' },
  { id: 'feed', name: 'Kho thức ăn', x: 18, y: 58, width: 20, height: 30, risk: 'online' },
  { id: 'nursery', name: 'Khu con', x: 18, y: 18, width: 18, height: 28, risk: 'warning' },
]

export const alertSettings = [
  { id: 'SET-001', name: alertTypes.dress, enabled: true, severity: 'warning', threshold: '>= 85%' },
  { id: 'SET-002', name: alertTypes.intrusion, enabled: true, severity: 'danger', threshold: '>= 90%' },
  { id: 'SET-003', name: alertTypes.fever, enabled: true, severity: 'danger', threshold: '>= 88%' },
  { id: 'SET-004', name: alertTypes.immobile, enabled: true, severity: 'critical', threshold: '>= 92%' },
  { id: 'SET-005', name: alertTypes.disconnect, enabled: true, severity: 'critical', threshold: '30 giây' },
]

export const onlineCameraCount = cameras.filter((camera) => camera.status === 'online').length

export function getCameraById(cameraId) {
  return cameras.find((camera) => camera.id === cameraId)
}

export function getEventsByCamera(cameraId) {
  return events.filter((event) => event.cameraId === cameraId)
}

export function getViolationImagesByCamera(cameraId) {
  return violationImages.filter((image) => image.cameraId === cameraId)
}

export function getTopCameras(limit = 5) {
  return cameras
    .map((camera) => ({
      ...camera,
      totalEvents: events.filter((event) => event.cameraId === camera.id).length,
    }))
    .sort((a, b) => b.totalEvents - a.totalEvents)
    .slice(0, limit)
}

export function getTopZones(limit = 5) {
  const zones = cameras.reduce((acc, camera) => {
    const total = events.filter((event) => event.zone === camera.zone).length
    acc[camera.zone] = Math.max(acc[camera.zone] ?? 0, total)
    return acc
  }, {})

  return Object.entries(zones)
    .map(([zone, totalEvents]) => ({ zone, totalEvents }))
    .sort((a, b) => b.totalEvents - a.totalEvents)
    .slice(0, limit)
}
