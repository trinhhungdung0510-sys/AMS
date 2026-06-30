export const CAMERA_ZONE_TYPES = [
  { value: 'clean', label: 'Vùng sạch' },
  { value: 'dirty', label: 'Vùng bẩn' },
  { value: 'transition', label: 'Vùng trung gian' },
  { value: 'restricted', label: 'Vùng cấm / Khu hạn chế' },
  { value: 'entry', label: 'Lối vào / Lối đi' },
  { value: 'monitoring', label: 'Giám sát / Khu vực chung' },
  { value: 'warning', label: 'Cảnh báo' },
]

export const ZONE_NAME_SUGGESTIONS = [
  'Vùng sạch',
  'Vùng bẩn',
  'Vùng trung gian',
  'Phòng thay đồ',
  'Khu sát trùng',
  'Khu rửa tay',
  'Lối đi',
  'Kho thuốc',
  'Kho cám',
  'Chuồng nái',
  'Chuồng cai sữa',
  'Chuồng hậu bị',
  'Kho lạnh',
  'Khu khách',
]

export const ZONE_LIST_SORT_OPTIONS = [
  { value: 'name-asc', label: 'Tên A → Z' },
  { value: 'name-desc', label: 'Tên Z → A' },
  { value: 'type-asc', label: 'Loại A → Z' },
  { value: 'type-desc', label: 'Loại Z → A' },
  { value: 'points-desc', label: 'Nhiều điểm nhất' },
  { value: 'points-asc', label: 'Ít điểm nhất' },
  { value: 'created-desc', label: 'Mới nhất' },
  { value: 'created-asc', label: 'Cũ nhất' },
]

export const ZONE_LIST_LEVEL_FILTERS = [
  { value: 'all', label: 'Tất cả cấp' },
  { value: 'root', label: 'Vùng chính' },
  { value: 'subzone', label: 'SubZone' },
]

export const ZONE_LIST_STATUS_FILTERS = [
  { value: 'all', label: 'Mọi trạng thái' },
  { value: 'active', label: 'Hoạt động' },
  { value: 'incomplete', label: 'Thiếu điểm' },
  { value: 'selected', label: 'Đang chọn' },
  { value: 'editing', label: 'Đang chỉnh sửa' },
]

export const DEFAULT_ZONE_COLOR = '#ff0000'

export const CAMERA_DETAIL_TABS = [
  { id: 'overview', label: 'Tổng quan' },
  { id: 'live', label: 'Live Camera' },
  { id: 'biosecurity', label: 'Vùng an toàn sinh học' },
  { id: 'ai', label: 'AI' },
  { id: 'events', label: 'Sự kiện' },
  { id: 'journal', label: 'Nhật ký' },
  { id: 'settings', label: 'Cài đặt' },
]

export function getZoneTypeLabel(type) {
  return CAMERA_ZONE_TYPES.find((item) => item.value === type)?.label || type
}
