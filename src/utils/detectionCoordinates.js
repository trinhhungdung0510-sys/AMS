export function bboxToScreen(bbox, width, height) {
  if (!width || !height || !bbox) {
    return { x: 0, y: 0, width: 0, height: 0 }
  }

  return {
    x: bbox.x * width,
    y: bbox.y * height,
    width: bbox.w * width,
    height: bbox.h * height,
  }
}

export function formatDetectionLabel(label) {
  return String(label || '').trim().toUpperCase()
}

export function formatConfidence(confidence) {
  const value = Number(confidence)
  if (Number.isNaN(value)) return '0%'
  return `${Math.round(value * 100)}%`
}

export const DETECTION_LABEL_COLORS = {
  person: '#2563eb',
  dog: '#ea580c',
  pig: '#db2777',
  vehicle: '#16a34a',
}

export function getDetectionColor(label) {
  return DETECTION_LABEL_COLORS[String(label || '').toLowerCase()] || '#7c3aed'
}

export const DEMO_DETECTION = {
  label: 'person',
  confidence: 0.96,
  bbox: {
    x: 0.35,
    y: 0.2,
    w: 0.12,
    h: 0.28,
  },
}
