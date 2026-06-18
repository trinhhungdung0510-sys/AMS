import { cameras, onlineCameraCount } from './mockData'
import { TODAY, atshViolations, computeAtshKpis } from './atshViolations'

export const FARM_MAP_ZONES = [
  { id: 'gate-in', name: 'Cổng vào', x: 4, y: 72, width: 14, height: 18, risk: 'safe' },
  { id: 'gate-out', name: 'Cổng ra', x: 82, y: 72, width: 14, height: 18, risk: 'attention' },
  { id: 'pig-export', name: 'Khu xuất bán heo', x: 62, y: 72, width: 16, height: 18, risk: 'attention' },
  { id: 'person-quarantine', name: 'Khu cách ly người', x: 4, y: 48, width: 14, height: 20, risk: 'safe' },
  { id: 'pig-quarantine', name: 'Chuồng cách ly heo', x: 78, y: 48, width: 18, height: 20, risk: 'risk' },
  { id: 'gestation', name: 'Chuồng nái', x: 28, y: 14, width: 18, height: 22, risk: 'safe' },
  { id: 'farrowing', name: 'Chuồng đẻ', x: 48, y: 14, width: 18, height: 22, risk: 'attention' },
  { id: 'nursery', name: 'Chuồng cai sữa', x: 22, y: 40, width: 16, height: 18, risk: 'safe' },
  { id: 'finisher', name: 'Chuồng thịt', x: 42, y: 40, width: 16, height: 18, risk: 'safe' },
  { id: 'feed', name: 'Kho cám', x: 4, y: 14, width: 14, height: 18, risk: 'attention' },
  { id: 'medicine', name: 'Kho thuốc', x: 68, y: 14, width: 14, height: 18, risk: 'safe' },
  { id: 'shower', name: 'Nhà tắm', x: 20, y: 72, width: 14, height: 18, risk: 'safe' },
  { id: 'guard', name: 'Nhà bảo vệ', x: 38, y: 72, width: 14, height: 18, risk: 'safe' },
]

export const ATSH_DEDUCTIONS = [
  { key: 'no_shower', label: 'Không tắm', points: 8 },
  { key: 'no_sanitize', label: 'Không sát trùng', points: 6 },
  { key: 'vehicle_not_sanitized', label: 'Xe chưa sát trùng', points: 10 },
  { key: 'forbidden_intrusion', label: 'Vào vùng cấm', points: 12 },
  { key: 'wrong_uniform', label: 'Sai màu áo', points: 5 },
  { key: 'vehicle_forbidden', label: 'Xe vào vùng cấm', points: 12 },
  { key: 'animal_intrusion', label: 'Động vật xâm nhập', points: 15 },
]

const DEDUCTION_TYPE_MAP = {
  no_shower: 'no_shower',
  no_hand_sanitize: 'no_sanitize',
  no_boot_sanitize: 'no_sanitize',
  vehicle_not_sanitized: 'vehicle_not_sanitized',
  forbidden_intrusion: 'forbidden_intrusion',
  wrong_uniform: 'wrong_uniform',
  animal_intrusion: 'animal_intrusion',
}

export function countDeductions(violations = atshViolations) {
  const today = violations.filter((item) => item.date === TODAY)
  const counts = Object.fromEntries(ATSH_DEDUCTIONS.map((item) => [item.key, 0]))

  today.forEach((item) => {
    const key = DEDUCTION_TYPE_MAP[item.type]
    if (key) counts[key] += 1
    if (item.type === 'forbidden_intrusion' && item.typeLabel?.includes('xe')) {
      counts.vehicle_forbidden += 1
    }
  })

  return ATSH_DEDUCTIONS.map((rule) => ({
    ...rule,
    count: counts[rule.key] || 0,
    total: (counts[rule.key] || 0) * rule.points,
  }))
}

export function computeFarmAtshScore(violations = atshViolations) {
  const deductions = countDeductions(violations)
  const penalty = deductions.reduce((sum, item) => sum + item.total, 0)
  return Math.max(0, Math.min(100, 100 - penalty))
}

export function computeDiseaseRisk(violations = atshViolations) {
  const today = violations.filter((item) => item.date === TODAY)
  const critical = today.filter((item) => item.severity === 'CRITICAL').length
  const animal = today.filter((item) => item.typeGroup === 'animal').length
  const score = critical * 18 + animal * 25

  if (score >= 60) return { label: 'Cao', tone: 'risk', value: Math.min(100, score) }
  if (score >= 25) return { label: 'Trung bình', tone: 'attention', value: score }
  return { label: 'Thấp', tone: 'safe', value: Math.max(8, score) }
}

export function buildTopZones(violations = atshViolations) {
  const map = {}
  violations.forEach((item) => {
    map[item.zone] = (map[item.zone] || 0) + 1
  })
  return Object.entries(map)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}

export function buildTopCameras(violations = atshViolations) {
  const map = {}
  violations.forEach((item) => {
    map[item.cameraName] = (map[item.cameraName] || 0) + 1
  })
  return Object.entries(map)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}

export function buildTopRules(violations = atshViolations) {
  const map = {}
  violations.forEach((item) => {
    map[item.typeLabel] = (map[item.typeLabel] || 0) + 1
  })
  return Object.entries(map)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}

export const CHART_DATA = {
  day: [
    { label: '08:00', value: 2 },
    { label: '10:00', value: 4 },
    { label: '12:00', value: 3 },
    { label: '14:00', value: 6 },
    { label: '16:00', value: 5 },
    { label: '18:00', value: 2 },
  ],
  week: [
    { label: 'T2', value: 12 },
    { label: 'T3', value: 18 },
    { label: 'T4', value: 9 },
    { label: 'T5', value: 15 },
    { label: 'T6', value: 21 },
    { label: 'T7', value: 8 },
    { label: 'CN', value: 6 },
  ],
  month: [
    { label: 'T1', value: 42 },
    { label: 'T2', value: 38 },
    { label: 'T3', value: 51 },
    { label: 'T4', value: 47 },
    { label: 'T5', value: 55 },
    { label: 'T6', value: 39 },
  ],
}

export function getDefaultDashboardState() {
  const kpis = computeAtshKpis(atshViolations)
  return {
    atshScore: computeFarmAtshScore(),
    violationsToday: kpis.totalToday,
    diseaseRisk: computeDiseaseRisk(),
    activeCameras: onlineCameraCount,
    totalCameras: cameras.length,
    deductions: countDeductions(),
    topZones: buildTopZones(),
    topCameras: buildTopCameras(),
    topRules: buildTopRules(),
  }
}

export const RISK_LABELS = {
  safe: 'An toàn',
  attention: 'Cần chú ý',
  risk: 'Nguy cơ',
}
