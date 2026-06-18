export const ATSH_RULE_SEVERITY = {
  INFO: { label: 'Thông tin', tone: 'info' },
  WARNING: { label: 'Cảnh báo', tone: 'warning' },
  CRITICAL: { label: 'Nghiêm trọng', tone: 'critical' },
}

export const DEFAULT_ATSH_RULES = [
  {
    id: 'ATSH-R-001',
    code: 'FORBIDDEN_ZONE',
    name: 'Người vào vùng cấm',
    description: 'Phát hiện người xâm nhập khu vực ATSH bị cấm như kho cám, kho thuốc, chuồng heo.',
    severity: 'CRITICAL',
    zones: ['Kho cám', 'Kho thuốc', 'Chuồng nái', 'Chuồng đẻ'],
    enabled: true,
  },
  {
    id: 'ATSH-R-002',
    code: 'NO_SHOWER',
    name: 'Không tắm',
    description: 'Nhân sự vào trại sản xuất mà chưa hoàn tất bước tắm sát trùng bắt buộc.',
    severity: 'CRITICAL',
    zones: ['Nhà tắm', 'Chuồng nái', 'Chuồng đẻ', 'Chuồng cai sữa'],
    enabled: true,
  },
  {
    id: 'ATSH-R-003',
    code: 'NO_HAND_SANITIZE',
    name: 'Không sát trùng tay',
    description: 'Không thực hiện sát trùng tay tại điểm kiểm soát ATSH trước khi vào vùng sạch.',
    severity: 'WARNING',
    zones: ['Nhà tắm', 'Khu thay đồ', 'Cổng vào'],
    enabled: true,
  },
  {
    id: 'ATSH-R-004',
    code: 'NO_BOOT_SANITIZE',
    name: 'Không sát trùng chân',
    description: 'Không đi qua khay sát trùng ủng trước khi vào khu vực sản xuất sạch.',
    severity: 'WARNING',
    zones: ['Nhà tắm', 'Khay sát trùng ủng', 'Chuồng nái'],
    enabled: true,
  },
  {
    id: 'ATSH-R-005',
    code: 'WRONG_UNIFORM',
    name: 'Sai màu áo',
    description: 'Trang phục không đúng màu quy định cho khu vực ATSH hiện tại.',
    severity: 'WARNING',
    zones: ['Toàn trại', 'Chuồng nái', 'Chuồng đẻ'],
    enabled: true,
  },
  {
    id: 'ATSH-R-006',
    code: 'STRANGER_CONTACT',
    name: 'Tiếp xúc người lạ',
    description: 'Công nhân tiếp xúc trực tiếp với khách hoặc người lạ chưa qua quy trình ATSH.',
    severity: 'WARNING',
    zones: ['Cổng vào', 'Nhà bảo vệ', 'Khu tiếp khách'],
    enabled: true,
  },
  {
    id: 'ATSH-R-007',
    code: 'FEED_TRUCK_CONTACT',
    name: 'Tiếp xúc xe cám',
    description: 'Tiếp xúc xe vận chuyển cám tại khu kho cám mà chưa tuân thủ quy trình.',
    severity: 'WARNING',
    zones: ['Kho cám', 'Bãi đỗ xe', 'Khu sát trùng xe'],
    enabled: true,
  },
  {
    id: 'ATSH-R-008',
    code: 'PIG_TRUCK_CONTACT',
    name: 'Tiếp xúc xe bắt heo',
    description: 'Tiếp xúc xe vận chuyển heo tại khu xuất nhập mà chưa tuân thủ quy trình.',
    severity: 'WARNING',
    zones: ['Khu xuất bán heo', 'Khu sát trùng xe'],
    enabled: true,
  },
  {
    id: 'ATSH-R-009',
    code: 'VEHICLE_NOT_SANITIZED',
    name: 'Xe chưa sát trùng',
    description: 'Xe vào trại chưa hoàn tất quy trình sát trùng xe bắt buộc.',
    severity: 'CRITICAL',
    zones: ['Cổng vào', 'Khu sát trùng xe', 'Bãi đỗ xe'],
    enabled: true,
  },
  {
    id: 'ATSH-R-010',
    code: 'VEHICLE_FORBIDDEN',
    name: 'Xe vào vùng cấm',
    description: 'Phát hiện xe di chuyển vào khu vực ATSH bị cấm.',
    severity: 'CRITICAL',
    zones: ['Chuồng nái', 'Chuồng đẻ', 'Kho thuốc'],
    enabled: true,
  },
  {
    id: 'ATSH-R-011',
    code: 'ANIMAL_INTRUSION',
    name: 'Động vật xâm nhập',
    description: 'Phát hiện chó, mèo, chuột, chim xâm nhập khu vực sạch hoặc chuồng heo.',
    severity: 'CRITICAL',
    zones: ['Chuồng nái', 'Chuồng đẻ', 'Chuồng cai sữa', 'Chuồng thịt'],
    enabled: true,
  },
]

const severityFromApi = {
  'Thông tin': 'INFO',
  'Cảnh báo': 'WARNING',
  'Nghiêm trọng': 'CRITICAL',
  info: 'INFO',
  warning: 'WARNING',
  critical: 'CRITICAL',
}

export function mapApiRule(item, index) {
  const fallback = DEFAULT_ATSH_RULES[index] || DEFAULT_ATSH_RULES[0]
  return {
    id: item.id,
    code: item.ma_quy_tac || fallback.code,
    name: item.ten_vi_pham || fallback.name,
    description: item.mo_ta || fallback.description,
    severity: severityFromApi[item.muc_do] || fallback.severity,
    zones: fallback.zones,
    enabled: item.kich_hoat ?? true,
    fromApi: true,
  }
}

export function mergeRules(apiRules) {
  if (!apiRules?.length) return DEFAULT_ATSH_RULES
  const mapped = apiRules.map(mapApiRule)
  const ids = new Set(mapped.map((item) => item.name))
  const rest = DEFAULT_ATSH_RULES.filter((item) => !ids.has(item.name))
  return [...mapped, ...rest].slice(0, DEFAULT_ATSH_RULES.length)
}
