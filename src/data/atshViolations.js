import { cameras } from './mockData'

export const TODAY = '2026-06-18'

export const VI_PHAM_ATSH_ROUTE = '/vi-pham-atsh'

export const ATSH_SEVERITY = {
  INFO: { label: 'Thông tin', color: '#16a34a', tone: 'info' },
  WARNING: { label: 'Cảnh báo', color: '#f97316', tone: 'warning' },
  CRITICAL: { label: 'Nghiêm trọng', color: '#dc2626', tone: 'critical' },
}

export const ATSH_STATUS = {
  new: 'Mới',
  confirmed: 'Đang xử lý',
  resolved: 'Đã xử lý',
  dismissed: 'Bỏ qua',
}

export const ATSH_VIOLATION_TYPES = [
  { code: 'forbidden_intrusion', label: 'Người vào vùng cấm', severity: 'CRITICAL', group: 'human' },
  { code: 'dirty_to_clean', label: 'Đi từ vùng bẩn sang vùng sạch', severity: 'CRITICAL', group: 'movement' },
  { code: 'no_shower', label: 'Không tắm trước khi vào trại', severity: 'CRITICAL', group: 'sanitation' },
  { code: 'no_hand_sanitize', label: 'Không sát trùng tay', severity: 'WARNING', group: 'sanitation' },
  { code: 'no_boot_sanitize', label: 'Không sát trùng chân', severity: 'WARNING', group: 'sanitation' },
  { code: 'wrong_uniform', label: 'Sai màu quần áo', severity: 'WARNING', group: 'human' },
  { code: 'stranger_contact', label: 'Tiếp xúc người lạ', severity: 'WARNING', group: 'contact' },
  { code: 'pig_truck_contact', label: 'Tiếp xúc xe bắt heo', severity: 'WARNING', group: 'contact' },
  { code: 'feed_truck_contact', label: 'Tiếp xúc xe cám', severity: 'WARNING', group: 'contact' },
  { code: 'vehicle_not_sanitized', label: 'Xe chưa sát trùng', severity: 'CRITICAL', group: 'vehicle' },
  { code: 'animal_intrusion', label: 'Động vật xâm nhập', severity: 'CRITICAL', group: 'animal' },
]

const typeByCode = Object.fromEntries(ATSH_VIOLATION_TYPES.map((item) => [item.code, item]))

const DESCRIPTIONS = {
  forbidden_intrusion: 'Phát hiện người hoặc đối tượng xâm nhập khu vực ATSH bị cấm trên camera.',
  dirty_to_clean: 'Di chuyển trực tiếp từ khu bẩn sang khu sạch mà không qua quy trình ATSH.',
  no_shower: 'Nhân sự vào trại sản xuất mà chưa hoàn tất bước tắm sát trùng bắt buộc.',
  no_hand_sanitize: 'Không thực hiện sát trùng tay tại điểm kiểm soát ATSH.',
  no_boot_sanitize: 'Không đi qua khay sát trùng ủng trước khi vào vùng sạch.',
  wrong_uniform: 'Trang phục không đúng màu quy định cho khu vực ATSH hiện tại.',
  stranger_contact: 'Công nhân tiếp xúc trực tiếp với khách hoặc người lạ chưa qua ATSH.',
  pig_truck_contact: 'Tiếp xúc xe vận chuyển heo tại khu xuất nhập mà chưa tuân thủ quy trình.',
  feed_truck_contact: 'Tiếp xúc xe vận chuyển cám tại khu kho cám.',
  vehicle_not_sanitized: 'Xe vào trại chưa hoàn tất quy trình sát trùng xe.',
  animal_intrusion: 'Phát hiện động vật lạ xâm nhập khu vực sạch hoặc chuồng heo.',
}

const persons = ['Công nhân A', 'Công nhân B', 'Khách thăm trại', 'Nhân viên thuê ngoài', 'Tài xế xe cám']
const animals = ['Chó', 'Mèo', 'Chuột', 'Chim']
const statuses = ['new', 'confirmed', 'resolved', 'dismissed']
const timelineHours = [8, 8, 8, 9, 9, 10, 10, 11, 12, 13, 14, 15, 16]

export const atshViolations = Array.from({ length: 44 }, (_, index) => {
  const typeDef = ATSH_VIOLATION_TYPES[index % ATSH_VIOLATION_TYPES.length]
  const camera = cameras[index % cameras.length]
  const hour = timelineHours[index % timelineHours.length]
  const minute = (index * 5 + 3) % 60
  const isToday = index < 24
  const date = isToday ? TODAY : `2026-06-${String(17 - (index % 5)).padStart(2, '0')}`
  const time = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`
  const status = statuses[index % statuses.length]

  return {
    id: `ATSH-${String(index + 1).padStart(4, '0')}`,
    type: typeDef.code,
    typeLabel: typeDef.label,
    typeGroup: typeDef.group,
    cameraId: camera.id,
    cameraName: camera.name,
    zone: camera.zone,
    severity: typeDef.severity,
    confidence: Math.min(99, 78 + ((index * 9) % 22)),
    date,
    time,
    datetime: `${date}T${time}:00`,
    status,
    handler: status === 'new' ? 'Chưa phân công' : 'Trần Bảo Long',
    person: typeDef.group !== 'animal' ? persons[index % persons.length] : null,
    animal: typeDef.group === 'animal' ? animals[index % animals.length] : null,
    description: DESCRIPTIONS[typeDef.code],
    snapshotTone: typeDef.severity === 'CRITICAL' ? 'critical' : typeDef.severity === 'WARNING' ? 'warning' : 'info',
  }
})

export function getViolationById(id) {
  return atshViolations.find((item) => item.id === id)
}

export function getViolationTimeline(violation) {
  if (!violation) return []
  return atshViolations
    .filter((item) => item.date === violation.date)
    .sort((a, b) => a.time.localeCompare(b.time))
}

export function computeAtshKpis(items) {
  const todayItems = items.filter((item) => item.date === TODAY)

  return {
    totalToday: todayItems.length,
    critical: todayItems.filter((item) => item.severity === 'CRITICAL').length,
    processing: todayItems.filter((item) => item.status === 'confirmed').length,
    resolved: todayItems.filter((item) => item.status === 'resolved').length,
  }
}

export function mapApiEventToViolation(event) {
  const title = event.ten_vi_pham || event.title || event.event_type || event.eventType
  const matched = ATSH_VIOLATION_TYPES.find((item) =>
    title?.toLowerCase().includes(item.label.toLowerCase().slice(0, 6)),
  )
  const typeDef = matched || typeByCode.forbidden_intrusion
  const occurred = event.thoi_gian || event.started_at || event.occurred_at || ''
  const [datePart, timePart] = occurred.split('T')
  const time = timePart ? timePart.slice(0, 5) : '00:00'

  let status = 'new'
  const rawStatus = event.trang_thai || event.status || ''
  if (rawStatus === 'Đã xử lý' || rawStatus === 'resolved' || rawStatus === 'RESOLVED') status = 'resolved'
  else if (rawStatus === 'Đang xử lý' || rawStatus === 'processing') status = 'confirmed'

  const severityRaw = event.muc_do || event.severityLabel || event.severity || 'INFO'

  return {
    id: event.id,
    type: typeDef.code,
    typeLabel: title || typeDef.label,
    typeGroup: typeDef.group,
    cameraId: event.camera_id || event.cameraId || '',
    cameraName: event.ten_camera || event.camera_name || event.cameraName,
    zone: event.ten_vung || event.zone_name || event.zoneName,
    severity: severityRaw?.includes('Nghiêm') || severityRaw === 'CRITICAL'
      ? 'CRITICAL'
      : severityRaw?.includes('Cảnh') || severityRaw === 'WARNING'
        ? 'WARNING'
        : 'INFO',
    confidence: event.do_tin_cay ?? (event.confidence != null ? Math.round(Number(event.confidence) * (Number(event.confidence) <= 1 ? 100 : 1)) : 90),
    date: datePart || TODAY,
    time,
    datetime: occurred || `${TODAY}T${time}:00`,
    status,
    handler: event.nguoi_xu_ly || 'Chưa phân công',
    person: null,
    animal: null,
    description: DESCRIPTIONS[typeDef.code],
    snapshotTone: 'critical',
    fromApi: true,
  }
}

export const zoneOptions = [...new Set(cameras.map((item) => item.zone))].map((zone) => ({
  value: zone,
  label: zone,
}))

export const cameraOptions = cameras.map((item) => ({
  value: item.id,
  label: item.name,
}))

export const dateFilterOptions = [
  { value: 'all', label: 'Tất cả ngày' },
  { value: 'today', label: 'Hôm nay' },
  { value: 'week', label: '7 ngày qua' },
  { value: 'month', label: '30 ngày qua' },
]

export const severityFilterOptions = [
  { value: 'all', label: 'Tất cả mức độ' },
  { value: 'INFO', label: 'Thông tin' },
  { value: 'WARNING', label: 'Cảnh báo' },
  { value: 'CRITICAL', label: 'Nghiêm trọng' },
]
