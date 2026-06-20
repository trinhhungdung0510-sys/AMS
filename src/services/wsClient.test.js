import { describe, expect, it, vi } from 'vitest'
import { WsClient } from '../services/wsClient'

describe('WsClient', () => {
  it('builds websocket url from api base', () => {
    const client = new WsClient('/ws/events')
    expect(client.url).toContain('/ws/events')
  })

  it('registers and removes listeners and replays connect state', () => {
    const client = new WsClient('/ws/events')
    const handler = { onConnect: vi.fn(), onMessage: vi.fn() }
    client.socket = { readyState: WebSocket.OPEN }
    const unsubscribe = client.subscribe(handler)
    expect(handler.onConnect).toHaveBeenCalled()
    client.listeners.forEach((listener) => listener.onMessage?.({ type: 'heartbeat' }))
    expect(handler.onMessage).toHaveBeenCalled()
    unsubscribe()
    expect(client.listeners.size).toBe(0)
  })
})
