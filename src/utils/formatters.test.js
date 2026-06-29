import { describe, expect, it } from 'vitest'
import { formatDateTime } from './formatters.js'

describe('formatDateTime', () => {
  it('formats valid date and time', () => {
    expect(formatDateTime('2026-06-18', '08:30')).toBe('08:30 · 18/06/2026')
  })

  it('does not throw when date is missing', () => {
    expect(formatDateTime(undefined, '08:30')).toBe('08:30')
    expect(formatDateTime(null, undefined)).toBe('--:--')
  })

  it('handles malformed date strings safely', () => {
    expect(formatDateTime('invalid', '09:00')).toBe('09:00')
  })
})
