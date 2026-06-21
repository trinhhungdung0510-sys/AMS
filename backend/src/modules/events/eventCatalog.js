export const EVENT_CLASSIFICATIONS = {
  BIOSECURITY: 'BIOSECURITY',
  ANIMAL: 'ANIMAL',
  VEHICLE: 'VEHICLE',
  SYSTEM: 'SYSTEM',
}

export const EVENT_SEVERITIES = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
  CRITICAL: 'CRITICAL',
}

export const EVENT_TYPE_ALIASES = {
  PROCESS_VIOLATION: 'BIOSECURITY_PROCESS_VIOLATION',
}

export const EVENT_CATALOG = {
  UNIFORM_VIOLATION: {
    classification: 'BIOSECURITY',
    severity: 'MEDIUM',
    explanation: {
      title: 'Sai đồng phục vùng',
      description: 'Người đi vào vùng sạch nhưng không sử dụng đồng phục phù hợp.',
      recommendedAction: 'Kiểm tra quy trình thay đồ và sát trùng.',
    },
  },
  NO_HAND_SANITIZATION: {
    classification: 'BIOSECURITY',
    severity: 'HIGH',
    explanation: {
      title: 'Không sát trùng tay',
      description: 'Người bỏ qua bước rửa tay sát trùng trước khi vào vùng kiểm soát.',
      recommendedAction: 'Nhắc nhở và kiểm tra lại quy trình sát trùng tay tại điểm giám sát.',
    },
  },
  NO_BOOT_SANITIZATION: {
    classification: 'BIOSECURITY',
    severity: 'HIGH',
    explanation: {
      title: 'Không sát trùng ủng',
      description: 'Người bỏ qua bước sát trùng ủng trước khi vào vùng sạch.',
      recommendedAction: 'Kiểm tra khay sát trùng ủng và giám sát tuân thủ quy trình.',
    },
  },
  ZONE_INTRUSION: {
    classification: 'BIOSECURITY',
    severity: 'HIGH',
    explanation: {
      title: 'Xâm nhập vùng cấm',
      description: 'Người hoặc đối tượng đi vào vùng bị hạn chế hoặc cấm tuyệt đối.',
      recommendedAction: 'Xác minh danh tính, ghi nhận vi phạm và áp dụng biện pháp cách ly.',
    },
  },
  BIOSECURITY_PROCESS_VIOLATION: {
    classification: 'BIOSECURITY',
    severity: 'CRITICAL',
    explanation: {
      title: 'Vi phạm quy trình an toàn sinh học',
      description: 'Người bỏ qua một hoặc nhiều bước bắt buộc trong quy trình vào vùng sạch.',
      recommendedAction: 'Dừng di chuyển, đưa người vi phạm quay lại thực hiện đầy đủ quy trình.',
    },
  },
  ANIMAL_INTRUSION: {
    classification: 'ANIMAL',
    severity: 'HIGH',
    explanation: {
      title: 'Động vật xâm nhập',
      description: 'Động vật không được phép xuất hiện trong vùng sản xuất hoặc vùng sạch.',
      recommendedAction: 'Loại bỏ động vật khỏi vùng và kiểm tra rào chắn, cửa ra vào.',
    },
  },
  VEHICLE_INTRUSION: {
    classification: 'VEHICLE',
    severity: 'HIGH',
    explanation: {
      title: 'Xe vi phạm sát trùng',
      description: 'Phương tiện vào vùng kiểm soát mà chưa hoàn thành quy trình sát trùng.',
      recommendedAction: 'Dừng xe, yêu cầu sát trùng lại và ghi nhận biển số.',
    },
  },
  CAMERA_OFFLINE: {
    classification: 'SYSTEM',
    severity: 'MEDIUM',
    explanation: {
      title: 'Camera mất kết nối',
      description: 'Camera không gửi tín hiệu hoặc heartbeat trong thời gian quy định.',
      recommendedAction: 'Kiểm tra nguồn điện, mạng và thiết bị tại vị trí camera.',
    },
  },
}

export const CLASSIFICATION_LABELS = {
  BIOSECURITY: 'An toàn sinh học',
  ANIMAL: 'Động vật',
  VEHICLE: 'Phương tiện',
  SYSTEM: 'Hệ thống',
}

export const SEVERITY_LABELS = {
  LOW: 'Thông tin',
  MEDIUM: 'Cảnh báo',
  HIGH: 'Mức cao',
  CRITICAL: 'Nghiêm trọng',
}

export function normalizeEventType(eventType) {
  if (!eventType) return null
  const normalized = String(eventType).trim().toUpperCase()
  return EVENT_TYPE_ALIASES[normalized] || normalized
}

export function resolveEventClassification(eventType, category) {
  const normalized = normalizeEventType(eventType)
  if (normalized && EVENT_CATALOG[normalized]) {
    return EVENT_CATALOG[normalized].classification
  }
  if (category === 'animal_intrusion') return 'ANIMAL'
  if (category === 'camera_offline') return 'SYSTEM'
  return 'BIOSECURITY'
}

export function resolveEventSeverity(eventType, fallback) {
  const normalized = normalizeEventType(eventType)
  if (normalized && EVENT_CATALOG[normalized]) {
    return EVENT_CATALOG[normalized].severity
  }
  if (fallback) {
    const upper = String(fallback).toUpperCase()
    if (SEVERITY_LABELS[upper]) return upper
  }
  return 'MEDIUM'
}

export function buildEventExplanation(eventType, { ruleName, zoneName } = {}) {
  const normalized = normalizeEventType(eventType)
  const entry = EVENT_CATALOG[normalized]
  if (!entry) {
    return {
      title: ruleName || normalized || 'Vi phạm tuân thủ',
      description: `Sự kiện ${ruleName || normalized || 'vi phạm'} được ghi nhận bởi hệ thống AMS.`,
      recommendedAction: 'Kiểm tra camera, xác minh vi phạm và xử lý theo quy trình nội bộ.',
    }
  }

  const explanation = { ...entry.explanation }
  if (ruleName && normalized === 'BIOSECURITY_PROCESS_VIOLATION') {
    explanation.title = ruleName
  }
  if (zoneName) {
    explanation.description = `${explanation.description} Vùng: ${zoneName}.`
  }
  return explanation
}

export function enrichEventFields(raw = {}) {
  const eventType = raw.eventType || raw.event_type
  const normalized = normalizeEventType(eventType)
  const severity = resolveEventSeverity(normalized, raw.severity)
  const classification = resolveEventClassification(normalized, raw.category)
  const explanation = buildEventExplanation(normalized, {
    ruleName: raw.ruleName || raw.rule_name,
    zoneName: raw.zoneName || raw.zone_name || raw.zone,
  })

  return {
    eventType: normalized || eventType,
    classification,
    severity,
    severityLabel: SEVERITY_LABELS[severity] || severity,
    classificationLabel: CLASSIFICATION_LABELS[classification] || classification,
    title: raw.title || explanation.title,
    description: raw.description || explanation.description,
    recommendedAction: raw.recommendedAction || explanation.recommendedAction,
    explanation: raw.explanation || explanation,
  }
}
