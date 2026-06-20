import { describe, expect, it, vi } from 'vitest'
import { WsClient } from '../services/wsClient'

describe('WsClient', () => {
  it('builds websocket url from api base', () => {
    const client = new WsClient('/ws/events')
    expect(client.url).toContain('/ws/events')
  })

  it('registers and removes listeners', () => {
    const client = new WsClient('/ws/events')
    const handler = { onMessage: vi.fn() }
    const unsubscribe = client.subscribe(handler)
    client.listeners.forEach((listener) => listener.onMessage?.({ type: 'heartbeat' }))
    expect(handler.onMessage).toHaveBeenCalled()
    unsubscribe()
    expect(client.listeners.size).toBe(0)
  })
})
