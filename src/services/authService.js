import { apiFetch } from './apiClient'

const TOKEN_KEY = 'ams_token'

export function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export async function login(email, password) {
  const response = await apiFetch('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
    }),
  })

  if (!response.ok) {
    throw new Error('Login failed')
  }

  const data = await response.json()

  saveToken(data.access_token)

  return data
}

export async function getCurrentUser() {
  const response = await apiFetch('/auth/me')

  if (!response.ok) {
    throw new Error('Unable to load user')
  }

  return response.json()
}

export function logout() {
  clearToken()
}
