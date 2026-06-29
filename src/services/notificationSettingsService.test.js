import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  connectGmail,
  connectGmailNotification,
  testGmail,
  testGmailNotification,
  verifyGmail,
  verifyGmailNotification,
} from './notificationSettingsService'

function mockLocalStorage() {
  const store = new Map()
  vi.stubGlobal('localStorage', {
    getItem: (key) => store.get(key) ?? null,
    setItem: (key, value) => store.set(key, String(value)),
    removeItem: (key) => store.delete(key),
    clear: () => store.clear(),
  })
}

describe('notificationSettingsService gmail flow', () => {
  beforeEach(() => {
    mockLocalStorage()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('connectGmail calls POST /api/notification/gmail/connect with bearer token', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ connected: true, gmail_recipient: 'ops@example.com' }),
    })
    vi.stubGlobal('fetch', fetchMock)
    localStorage.setItem('ams_token', 'test-token')

    const result = await connectGmailNotification({ gmail_recipient: 'ops@example.com' })

    expect(result.connected).toBe(true)
    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, options] = fetchMock.mock.calls[0]
    expect(url).toMatch(/\/api\/notification\/gmail\/connect$/)
    expect(options.method).toBe('POST')
    expect(options.headers.Authorization).toBe('Bearer test-token')
    expect(JSON.parse(options.body)).toEqual({ gmail_recipient: 'ops@example.com' })
  })

  it('testGmail calls POST /api/notification/gmail/test', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, recipient: 'ops@example.com', error: null }),
    })
    vi.stubGlobal('fetch', fetchMock)
    localStorage.setItem('ams_token', 'test-token')

    await testGmailNotification()

    const [url, options] = fetchMock.mock.calls[0]
    expect(url).toMatch(/\/api\/notification\/gmail\/test$/)
    expect(options.method).toBe('POST')
    expect(options.headers.Authorization).toBe('Bearer test-token')
  })

  it('surfaces backend error detail instead of generic message', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Authentication failed — kiểm tra App Password Gmail' }),
    })
    vi.stubGlobal('fetch', fetchMock)
    localStorage.setItem('ams_token', 'test-token')

    await expect(connectGmail({ gmail_recipient: 'ops@example.com' })).rejects.toThrow(
      'Authentication failed — kiểm tra App Password Gmail',
    )
  })

  it('verifyGmail calls POST /api/notification/gmail/verify', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true, message: 'Kết nối SMTP Gmail thành công' }),
    })
    vi.stubGlobal('fetch', fetchMock)
    localStorage.setItem('ams_token', 'test-token')

    await verifyGmailNotification()

    const [url, options] = fetchMock.mock.calls[0]
    expect(url).toMatch(/\/api\/notification\/gmail\/verify$/)
    expect(options.method).toBe('POST')
  })

  it('testGmail alias matches testGmailNotification', () => {
    expect(testGmail).toBe(testGmailNotification)
    expect(connectGmail).toBe(connectGmailNotification)
    expect(verifyGmail).toBe(verifyGmailNotification)
  })
})
