export const DEFAULT_ZONE_OPACITY = 0.3

export function toPoints(points) {
  return points.map(([x, y]) => `${x},${y}`).join(' ')
}

export function rectFromCorners(start, end) {
  const [x1, y1] = start
  const [x2, y2] = end
  return [
    [Math.min(x1, x2), Math.min(y1, y2)],
    [Math.max(x1, x2), Math.min(y1, y2)],
    [Math.max(x1, x2), Math.max(y1, y2)],
    [Math.min(x1, x2), Math.max(y1, y2)],
  ]
}

export function polygonCentroid(points) {
  if (!points.length) return [0, 0]
  const sum = points.reduce(
    (acc, [x, y]) => [acc[0] + x, acc[1] + y],
    [0, 0],
  )
  return [Math.round(sum[0] / points.length), Math.round(sum[1] / points.length)]
}

export function translatePoints(points, dx, dy) {
  return points.map(([x, y]) => [
    Math.max(0, Math.min(1280, Math.round(x + dx))),
    Math.max(0, Math.min(720, Math.round(y + dy))),
  ])
}

export function edgeMidpoint(a, b) {
  return [Math.round((a[0] + b[0]) / 2), Math.round((a[1] + b[1]) / 2)]
}

export function distance(a, b) {
  return Math.hypot(a[0] - b[0], a[1] - b[1])
}

export function closestEdgeIndex(point, polygon) {
  let bestIndex = 0
  let bestDistance = Infinity
  polygon.forEach((start, index) => {
    const end = polygon[(index + 1) % polygon.length]
    const mid = edgeMidpoint(start, end)
    const d = distance(point, mid)
    if (d < bestDistance) {
      bestDistance = d
      bestIndex = index
    }
  })
  return bestIndex
}

export function insertPointOnEdge(polygon, edgeIndex, point) {
  const next = [...polygon]
  next.splice(edgeIndex + 1, 0, point)
  return next
}

export function removePointAtIndex(polygon, index) {
  if (polygon.length <= 3) return polygon
  return polygon.filter((_, itemIndex) => itemIndex !== index)
}

export function duplicatePoints(points, offset = [24, 24]) {
  return translatePoints(points, offset[0], offset[1])
}

export function clampPoint(point, width = 1280, height = 720) {
  return [
    Math.max(0, Math.min(width, Math.round(point[0]))),
    Math.max(0, Math.min(height, Math.round(point[1]))),
  ]
}

export function getCanvasPoint(event, canvasRef, zoom, pan, width, height) {
  const rect = canvasRef.current.getBoundingClientRect()
  const x = ((event.clientX - rect.left) / rect.width) * width
  const y = ((event.clientY - rect.top) / rect.height) * height
  return clampPoint([
    (x - pan.x) / zoom,
    (y - pan.y) / zoom,
  ], width, height)
}

export function moveEdgePoints(polygon, edgeIndex, delta) {
  const next = polygon.map((point) => [...point])
  const startIndex = edgeIndex
  const endIndex = (edgeIndex + 1) % polygon.length
  next[startIndex] = clampPoint([next[startIndex][0] + delta[0], next[startIndex][1] + delta[1]])
  next[endIndex] = clampPoint([next[endIndex][0] + delta[0], next[endIndex][1] + delta[1]])
  return next
}
