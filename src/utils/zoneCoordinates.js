export function normalizedToScreen(point, width, height) {
  return {
    x: point.x * width,
    y: point.y * height,
  }
}

export function screenToNormalized(point, width, height) {
  if (!width || !height) {
    return { x: 0, y: 0 }
  }

  return {
    x: Math.min(1, Math.max(0, point.x / width)),
    y: Math.min(1, Math.max(0, point.y / height)),
  }
}

export function pointsToSvgString(points, width, height) {
  return points
    .map((point) => {
      const screen = normalizedToScreen(point, width, height)
      return `${screen.x},${screen.y}`
    })
    .join(' ')
}
