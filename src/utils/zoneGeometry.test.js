import { describe, expect, it } from 'vitest'
import {
  denormalizePoint,
  normalizePoint,
  pointInPolygon,
  bboxCenter,
  polygonAreaNormalized,
  resolveNormalizedPoints,
  scalePolygonToNormalized,
} from './zoneGeometry'

describe('normalizePoint', () => {
  it('converts pixel coordinates to normalized 0-1', () => {
    expect(normalizePoint({ x: 192, y: 108 }, 1920, 1080)).toEqual({
      x: 0.1,
      y: 0.1,
    })
  })

  it('clamps values outside reference bounds', () => {
    expect(normalizePoint({ x: 2500, y: -10 }, 1920, 1080)).toEqual({
      x: 1,
      y: 0,
    })
  })

  it('returns zero when reference dimensions are missing', () => {
    expect(normalizePoint({ x: 100, y: 100 }, 0, 1080)).toEqual({ x: 0, y: 0 })
  })
})

describe('denormalizePoint', () => {
  it('converts normalized coordinates back to pixel space', () => {
    expect(denormalizePoint({ x: 0.25, y: 0.5 }, 1920, 1080)).toEqual({
      x: 480,
      y: 540,
    })
  })
})

describe('polygon scaling', () => {
  it('scalePolygonToNormalized converts all polygon vertices', () => {
    const polygon = [
      { x: 0, y: 0 },
      { x: 1920, y: 0 },
      { x: 960, y: 1080 },
    ]

    expect(scalePolygonToNormalized(polygon, 1920, 1080)).toEqual([
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 0.5, y: 1 },
    ])
  })

  it('resolveNormalizedPoints keeps normalized zones unchanged', () => {
    const zone = {
      points: [{ x: 0.2, y: 0.3 }],
      points_format: 'normalized',
      reference_width: 1920,
      reference_height: 1080,
    }

    expect(resolveNormalizedPoints(zone)).toEqual([{ x: 0.2, y: 0.3 }])
  })

  it('resolveNormalizedPoints converts legacy pixel zones using reference dimensions', () => {
    const zone = {
      points: [{ x: 960, y: 540 }],
      points_format: 'pixel',
      reference_width: 1920,
      reference_height: 1080,
    }

    expect(resolveNormalizedPoints(zone)).toEqual([{ x: 0.5, y: 0.5 }])
  })

  it('resolveNormalizedPoints converts legacy pixel zones using fallback reference', () => {
    const zone = {
      points: [{ x: 960, y: 540 }],
      points_format: 'pixel',
      reference_width: null,
      reference_height: null,
    }

    expect(resolveNormalizedPoints(zone, { width: 1920, height: 1080 })).toEqual([
      { x: 0.5, y: 0.5 },
    ])
  })
})

describe('pointInPolygon', () => {
  it('detects point inside unit square', () => {
    const square = [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 1, y: 1 },
      { x: 0, y: 1 },
    ]
    expect(pointInPolygon({ x: 0.5, y: 0.5 }, square)).toBe(true)
    expect(pointInPolygon({ x: 1.5, y: 0.5 }, square)).toBe(false)
  })
})

describe('bboxCenter', () => {
  it('returns center of normalized bbox', () => {
    expect(bboxCenter({ x: 0.2, y: 0.3, width: 0.4, height: 0.2 })).toEqual({
      x: 0.4,
      y: 0.4,
    })
  })
})

describe('polygonAreaNormalized', () => {
  it('returns normalized share of image area', () => {
    const half = [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 1, y: 0.5 },
      { x: 0, y: 0.5 },
    ]
    expect(polygonAreaNormalized(half)).toBeCloseTo(0.5, 4)
  })
})
