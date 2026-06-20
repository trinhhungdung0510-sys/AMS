import { describe, expect, it } from 'vitest'
import {
  pointInPolygon,
  bboxCenter,
} from '../utils/zoneGeometry'

describe('pointInPolygon (zoneGeometry)', () => {
  const triangle = [
    { x: 0, y: 0 },
    { x: 1, y: 0 },
    { x: 0.5, y: 1 },
  ]

  it('detects interior point', () => {
    expect(pointInPolygon({ x: 0.4, y: 0.3 }, triangle)).toBe(true)
  })

  it('rejects exterior point', () => {
    expect(pointInPolygon({ x: 0.9, y: 0.9 }, triangle)).toBe(false)
  })
})

describe('bboxCenter (zoneGeometry)', () => {
  it('returns normalized center', () => {
    expect(bboxCenter({ x: 0.1, y: 0.2, width: 0.2, height: 0.4 })).toEqual({
      x: 0.2,
      y: 0.4,
    })
  })
})
