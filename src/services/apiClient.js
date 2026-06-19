import { API_BASE_URL } from '../config/api'

const TOKEN_KEY = 'ams_token'

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY)
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`
  }

  const url = path.startsWith('http') ? path : `${API_BASE_URL}/api${path}`
  return fetch(url, { ...options, headers })
}
