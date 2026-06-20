export const CAMERA_ZONE_TYPES = [
  { value: 'monitoring', label: 'Giám sát' },
  { value: 'restricted', label: 'Vùng cấm' },
  { value: 'clean', label: 'Vùng sạch' },
  { value: 'dirty', label: 'Vùng bẩn' },
  { value: 'warning', label: 'Cảnh báo' },
  { value: 'entry', label: 'Lối vào' },
  { value: 'transition', label: 'Chuyển tiếp' },
]

export const DEFAULT_ZONE_COLOR = '#ff0000'

export const CAMERA_DETAIL_TABS = [
  { id: 'live', label: 'Live View' },
  { id: 'zones', label: 'Zones' },
  { id: 'events', label: 'Events' },
  { id: 'ai-rules', label: 'AI Rules' },
  { id: 'settings', label: 'Settings' },
]

export function getZoneTypeLabel(type) {
  return CAMERA_ZONE_TYPES.find((item) => item.value === type)?.label || type
}
