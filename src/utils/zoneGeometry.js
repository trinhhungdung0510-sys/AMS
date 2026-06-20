/**
 * Zone geometry v1.2 — normalized coordinates (0–1) with reference dimensions.
 * Legacy v1.1 zones (pixel points) remain readable via resolveNormalizedPoints().
 */

export const POINTS_FORMAT_PIXEL = 'pixel'
export const POINTS_FORMAT_NORMALIZED = 'normalized'

function clamp(value, lower = 0, upper = 1) {
  return Math.min(upper, Math.max(lower, value))
}

export function normalizePoint(point, referenceWidth, referenceHeight) {
  if (!referenceWidth || !referenceHeight) {
    return { x: 0, y: 0 }
  }

  return {
    x: clamp(point.x / referenceWidth),
    y: clamp(point.y / referenceHeight),
  }
}

export function denormalizePoint(point, referenceWidth, referenceHeight) {
  return {
    x: point.x * referenceWidth,
    y: point.y * referenceHeight,
  }
}

export function scalePolygonToNormalized(points, referenceWidth, referenceHeight) {
  return points.map((point) => normalizePoint(point, referenceWidth, referenceHeight))
}

export function isLegacyPixelZone(zoneOrPoints, pointsFormat) {
  const points = Array.isArray(zoneOrPoints) ? zoneOrPoints : zoneOrPoints?.points || []
  const format = pointsFormat ?? (Array.isArray(zoneOrPoints) ? null : zoneOrPoints?.points_format)

  if (format === POINTS_FORMAT_NORMALIZED) return false
  if (format === POINTS_FORMAT_PIXEL) return true
  return points.some((point) => point.x > 1 || point.y > 1)
}

export function resolveNormalizedPoints(zone, fallbackReference = null) {
  const points = zone?.points || []
  if (!isLegacyPixelZone(zone)) {
    return points.map((point) => ({ x: point.x, y: point.y }))
  }

  const refW = zone.reference_width || fallbackReference?.width
  const refH = zone.reference_height || fallbackReference?.height

  if (!refW || !refH) {
    if (fallbackReference?.width && fallbackReference?.height) {
      return scalePolygonToNormalized(points, fallbackReference.width, fallbackReference.height)
    }
    return points.map((point) => ({ x: point.x, y: point.y }))
  }

  return scalePolygonToNormalized(points, refW, refH)
}

export function getImageMetrics(imageElement, containerWidth, containerHeight) {
  if (!imageElement || !containerWidth || !containerHeight) {
    return {
      naturalWidth: 0,
      naturalHeight: 0,
      displayWidth: 0,
      displayHeight: 0,
      offsetX: 0,
      offsetY: 0,
      scaleX: 1,
      scaleY: 1,
    }
  }

  const naturalWidth = imageElement.naturalWidth || containerWidth
  const naturalHeight = imageElement.naturalHeight || containerHeight
  const imageRatio = naturalWidth / naturalHeight
  const containerRatio = containerWidth / containerHeight

  let displayWidth = containerWidth
  let displayHeight = containerHeight

  if (imageRatio > containerRatio) {
    displayHeight = containerWidth / imageRatio
  } else {
    displayWidth = containerHeight * imageRatio
  }

  const offsetX = (containerWidth - displayWidth) / 2
  const offsetY = (containerHeight - displayHeight) / 2

  return {
    naturalWidth,
    naturalHeight,
    displayWidth,
    displayHeight,
    offsetX,
    offsetY,
    scaleX: displayWidth / naturalWidth,
    scaleY: displayHeight / naturalHeight,
  }
}

export function imagePixelToScreenPoint(point, metrics) {
  return {
    x: metrics.offsetX + point.x * metrics.scaleX,
    y: metrics.offsetY + point.y * metrics.scaleY,
  }
}

export function normalizedToScreenPoint(point, metrics) {
  const pixel = denormalizePoint(point, metrics.naturalWidth, metrics.naturalHeight)
  return imagePixelToScreenPoint(pixel, metrics)
}

export function screenToImagePixel(clientX, clientY, rect, metrics) {
  const localX = clientX - rect.left - metrics.offsetX
  const localY = clientY - rect.top - metrics.offsetY

  return {
    x: clamp(localX / metrics.scaleX, 0, metrics.naturalWidth),
    y: clamp(localY / metrics.scaleY, 0, metrics.naturalHeight),
  }
}

export function screenToNormalizedPoint(clientX, clientY, rect, metrics) {
  const pixel = screenToImagePixel(clientX, clientY, rect, metrics)
  return normalizePoint(pixel, metrics.naturalWidth, metrics.naturalHeight)
}

export function pointsToSvgString(normalizedPoints, metrics) {
  return normalizedPoints
    .map((point) => {
      const screen = normalizedToScreenPoint(point, metrics)
      return `${screen.x},${screen.y}`
    })
    .join(' ')
}

export function roundNormalizedPoint(point) {
  return {
    x: Math.round(point.x * 10000) / 10000,
    y: Math.round(point.y * 10000) / 10000,
  }
}

export function getReferenceFromMetrics(metrics) {
  if (!metrics?.naturalWidth || !metrics?.naturalHeight) {
    return { width: null, height: null }
  }

  return {
    width: Math.round(metrics.naturalWidth),
    height: Math.round(metrics.naturalHeight),
  }
}
