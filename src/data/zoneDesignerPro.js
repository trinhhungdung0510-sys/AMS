import { cameras } from './mockData'

export const CANVAS_WIDTH = 1280
export const CANVAS_HEIGHT = 720

export const FARMS = [
  { id: 'FARM-001', name: 'Trại TIN NGHIA · Long An' },
  { id: 'FARM-002', name: 'Trại TIN NGHIA · Đồng Nai' },
]

export const ZONE_CATEGORIES = [
  { value: 'clean', label: 'Vùng sạch', color: '#16a34a', level: 'green', zoneType: 'internal_road' },
  { value: 'intermediate', label: 'Vùng trung gian', color: '#eab308', level: 'yellow', zoneType: 'shower_room' },
  { value: 'dirty', label: 'Vùng bẩn', color: '#f97316', level: 'orange', zoneType: 'worker_housing' },
  { value: 'forbidden', label: 'Vùng cấm', color: '#dc2626', level: 'red', zoneType: 'feed_storage' },
  { value: 'disinfection', label: 'Vùng sát trùng', color: '#ea580c', level: 'yellow', zoneType: 'person_disinfection_zone' },
  { value: 'isolation', label: 'Vùng cách ly', color: '#9333ea', level: 'red', zoneType: 'quarantine_barn' },
]

export const RISK_LEVELS = [
  { value: 'green', label: 'Thấp · Xanh' },
  { value: 'yellow', label: 'Trung bình · Vàng' },
  { value: 'orange', label: 'Cao · Cam' },
  { value: 'red', label: 'Nghiêm trọng · Đỏ' },
]

export const RULE_OPTIONS = {
  allowed: [
    { id: 'worker', label: 'Công nhân (Worker)' },
    { id: 'green_uniform', label: 'Áo xanh (Green Uniform)' },
    { id: 'supervisor', label: 'Giám sát (Supervisor)' },
    { id: 'vet', label: 'Thú y (Veterinarian)' },
  ],
  blocked: [
    { id: 'visitor', label: 'Khách (Visitor)' },
    { id: 'vehicle', label: 'Xe (Vehicle)' },
    { id: 'dog', label: 'Chó (Dog)' },
    { id: 'cat', label: 'Mèo (Cat)' },
    { id: 'bird', label: 'Chim (Bird)' },
    { id: 'rat', label: 'Chuột (Rat)' },
  ],
}

export const DEFAULT_ZONE_RULES = {
  clean: {
    allowed: ['worker', 'green_uniform'],
    blocked: ['visitor', 'vehicle', 'dog', 'cat', 'bird', 'rat'],
  },
  intermediate: {
    allowed: ['worker', 'supervisor'],
    blocked: ['visitor', 'vehicle', 'dog', 'cat', 'bird', 'rat'],
  },
  dirty: {
    allowed: ['worker'],
    blocked: ['visitor', 'vehicle', 'dog', 'cat', 'bird', 'rat', 'green_uniform'],
  },
  forbidden: {
    allowed: [],
    blocked: ['visitor', 'vehicle', 'worker', 'dog', 'cat', 'bird', 'rat'],
  },
  disinfection: {
    allowed: ['worker'],
    blocked: ['visitor', 'vehicle', 'dog', 'cat', 'bird', 'rat'],
  },
  isolation: {
    allowed: ['vet', 'supervisor'],
    blocked: ['visitor', 'vehicle', 'worker', 'dog', 'cat', 'bird', 'rat'],
  },
}

const SCENE_BY_CAMERA = {
  'CAM-001': 'gate',
  'CAM-006': 'shower',
  'CAM-008': 'feed',
  'CAM-005': 'quarantine',
  'CAM-002': 'gestation',
  'CAM-003': 'farrowing',
  'CAM-007': 'nursery',
}

export const DESIGNER_CAMERAS = cameras.map((camera, index) => ({
  id: camera.id,
  name: camera.name,
  zone: camera.zone,
  farmId: index < 6 ? 'FARM-001' : 'FARM-002',
  scene: SCENE_BY_CAMERA[camera.id] || 'gate',
}))

export function categoryMeta(category) {
  return ZONE_CATEGORIES.find((item) => item.value === category) || ZONE_CATEGORIES[1]
}

export function inferCategory(color, level) {
  const match = ZONE_CATEGORIES.find((item) => item.color === color || item.level === level)
  return match?.value || 'intermediate'
}

export function defaultRulesForCategory(category) {
  return DEFAULT_ZONE_RULES[category] || DEFAULT_ZONE_RULES.intermediate
}

export function mapZoneFromApi(item) {
  const category = inferCategory(item.mau_sac, item.cap_atsh)
  return {
    id: item.id,
    camera_id: item.camera_id,
    zone_name: item.ten_vung,
    zone_type: item.ma_vung,
    zone_type_label: item.ten_loai_vung,
    biosecurity_level: item.cap_atsh,
    color: item.mau_sac,
    opacity: item.do_mo ?? 0.3,
    polygon_points: item.diem_polygon,
    description: item.mo_ta || '',
    category,
    riskLevel: item.cap_atsh || categoryMeta(category).level,
    rules: defaultRulesForCategory(category),
    active: item.dang_hoat_dong,
  }
}
