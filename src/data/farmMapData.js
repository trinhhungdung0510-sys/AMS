import { cameras } from './mockData'
import { FARM_MAP_ZONES, RISK_LABELS } from './farmControlDashboard'
import { atshViolations } from './atshViolations'

const ZONE_CAMERA_MAP = {
  'gate-in': ['CAM-001'],
  'gate-out': ['CAM-001'],
  'pig-export': ['CAM-004'],
  'person-quarantine': ['CAM-006'],
  'pig-quarantine': ['CAM-005'],
  gestation: ['CAM-002', 'CAM-003'],
  farrowing: ['CAM-003'],
  nursery: ['CAM-007'],
  finisher: ['CAM-007'],
  feed: ['CAM-008'],
  medicine: ['CAM-008'],
  shower: ['CAM-006'],
  guard: ['CAM-001'],
}

const ZONE_NAME_TO_CAMERA_ZONE = {
  'Cổng vào': 'Cổng trại',
  'Cổng ra': 'Cổng trại',
  'Khu xuất bán heo': 'Khu đực giống',
  'Khu cách ly người': 'Hành lang chính',
  'Chuồng cách ly heo': 'Khu cách ly',
  'Chuồng nái': 'Khu nái',
  'Chuồng đẻ': 'Khu nái',
  'Chuồng cai sữa': 'Khu con',
  'Chuồng thịt': 'Khu con',
  'Kho cám': 'Kho thức ăn',
  'Kho thuốc': 'Kho thức ăn',
  'Nhà tắm': 'Hành lang chính',
  'Nhà bảo vệ': 'Cổng trại',
}

export { FARM_MAP_ZONES, RISK_LABELS }

export function getZoneCameras(zone) {
  const ids = ZONE_CAMERA_MAP[zone.id] || []
  const mapped = ids.map((id) => cameras.find((item) => item.id === id)).filter(Boolean)
  if (mapped.length) return mapped

  const zoneLabel = ZONE_NAME_TO_CAMERA_ZONE[zone.name]
  return cameras.filter((item) => item.zone === zoneLabel).slice(0, 2)
}

export function getZoneViolations(zone) {
  const zoneLabel = ZONE_NAME_TO_CAMERA_ZONE[zone.name] || zone.name
  return atshViolations
    .filter((item) => item.zone === zoneLabel || item.zone.includes(zone.name.split(' ').pop()))
    .slice(0, 5)
}

export function getZoneHistory(zone) {
  const violations = getZoneViolations(zone)
  const base = violations.length
    ? violations.map((item) => ({
      id: item.id,
      time: `${item.date} ${item.time}`,
      label: item.typeLabel,
      severity: item.severity,
    }))
    : [
      { id: 'H-1', time: '2026-06-18 08:00', label: 'Kiểm tra ATSH định kỳ', severity: 'INFO' },
      { id: 'H-2', time: '2026-06-17 14:30', label: 'Vệ sinh khu vực hoàn tất', severity: 'INFO' },
      { id: 'H-3', time: '2026-06-16 09:15', label: 'Cập nhật quy trình vào khu', severity: 'INFO' },
    ]

  return base
}

export function countZoneViolations(zone) {
  return getZoneViolations(zone).length
}
