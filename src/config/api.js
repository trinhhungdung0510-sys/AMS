function resolveApiBaseUrl() {
  if (typeof window !== 'undefined') {
    const { hostname } = window.location
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      return `http://${hostname}:8000`
    }
  }

  const fromEnv = import.meta.env.VITE_API_URL?.replace(/\/$/, '')
  if (fromEnv && !fromEnv.includes('backend-abc.trycloudflare.com')) {
    return fromEnv
  }

  return 'http://127.0.0.1:8000'
}

export const API_BASE_URL = resolveApiBaseUrl()

export function getWebSocketBaseUrl() {
  if (API_BASE_URL.startsWith('https://')) {
    return API_BASE_URL.replace('https://', 'wss://')
  }
  return API_BASE_URL.replace('http://', 'ws://')
}
