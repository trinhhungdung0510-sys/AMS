import { getWebSocketBaseUrl } from '../config/api'

const DEFAULT_RECONNECT_MS = 3000
const MAX_RECONNECT_MS = 30000

export class WsClient {
  constructor(path = '/ws/events', { onMessage, onConnect, onDisconnect } = {}) {
    this.path = path
    this.onMessage = onMessage
    this.onConnect = onConnect
    this.onDisconnect = onDisconnect
    this.socket = null
    this.reconnectMs = DEFAULT_RECONNECT_MS
    this.shouldReconnect = true
    this.listeners = new Set()
  }

  get url() {
    return `${getWebSocketBaseUrl()}${this.path}`
  }

  connect() {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return
    }

    this.shouldReconnect = true

    try {
      this.socket = new WebSocket(this.url)
    } catch {
      this.scheduleReconnect()
      return
    }

    this.socket.onopen = () => {
      this.reconnectMs = DEFAULT_RECONNECT_MS
      this.onConnect?.()
      this.listeners.forEach((listener) => listener.onConnect?.())
    }

    this.socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data)
        this.onMessage?.(payload)
        this.listeners.forEach((listener) => listener.onMessage?.(payload))
      } catch {
        // ignore malformed payloads
      }
    }

    this.socket.onclose = () => {
      this.onDisconnect?.()
      this.listeners.forEach((listener) => listener.onDisconnect?.())
      this.scheduleReconnect()
    }

    this.socket.onerror = () => {
      this.socket?.close()
    }
  }

  scheduleReconnect() {
    if (!this.shouldReconnect) return
    setTimeout(() => {
      this.reconnectMs = Math.min(this.reconnectMs * 2, MAX_RECONNECT_MS)
      this.connect()
    }, this.reconnectMs)
  }

  subscribe(listener) {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  disconnect() {
    this.shouldReconnect = false
    this.socket?.close()
    this.socket = null
  }
}

let sharedClient = null

export function getSharedWsClient() {
  if (!sharedClient) {
    sharedClient = new WsClient('/ws/events')
    sharedClient.connect()
  }
  return sharedClient
}

export function subscribeWsEvents(handlers) {
  const client = getSharedWsClient()
  return client.subscribe(handlers)
}
