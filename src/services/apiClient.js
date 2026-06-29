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

  try {
    return await fetch(url, { ...options, headers })
  } catch (error) {
    const message = error?.message || 'Network error'
    if (message.includes('Failed to fetch') || message.includes('NetworkError')) {
      throw new Error(`Không kết nối được Backend (${url}). Kiểm tra AMS Backend đang chạy.`)
    }
    throw error
  }
}
