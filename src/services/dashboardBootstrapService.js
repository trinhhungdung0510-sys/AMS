import { apiFetch } from './apiClient'

const BOOTSTRAP_TIMEOUT_MS = 45000

export async function fetchDashboardBootstrap() {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), BOOTSTRAP_TIMEOUT_MS)

  try {
    const response = await apiFetch('/dashboard/bootstrap', {
      signal: controller.signal,
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      const message = error.detail || `HTTP ${response.status}`
      const authError = new Error(typeof message === 'string' ? message : `HTTP ${response.status}`)
      authError.status = response.status
      throw authError
    }
    return response.json()
  } catch (err) {
    if (err instanceof Error && err.name === 'AbortError') {
      throw new Error('Bootstrap quá thời gian chờ. Kiểm tra backend và thử lại.')
    }
    throw err
  } finally {
    clearTimeout(timeoutId)
  }
}
