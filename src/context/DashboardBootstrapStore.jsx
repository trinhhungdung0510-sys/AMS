import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { useAuth } from './AuthContext'
import { clearToken, getToken } from '../services/authService'
import { fetchDashboardBootstrap } from '../services/dashboardBootstrapService'

const DashboardBootstrapContext = createContext(null)

export function DashboardBootstrapProvider({ children }) {
  const { user, setUser, setLoading: setAuthLoading } = useAuth()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const loadVersionRef = useRef(0)
  const initialSessionRef = useRef(Boolean(getToken()))

  const loadBootstrap = useCallback(async () => {
    const token = getToken()
    if (!token) {
      setData(null)
      setError(null)
      if (initialSessionRef.current) {
        setAuthLoading(false)
        initialSessionRef.current = false
      }
      return null
    }

    const version = loadVersionRef.current + 1
    loadVersionRef.current = version
    setLoading(true)
    setError(null)
    const blockAuth = initialSessionRef.current
    if (blockAuth) {
      setAuthLoading(true)
    }

    try {
      const payload = await fetchDashboardBootstrap()
      if (loadVersionRef.current !== version) {
        return null
      }
      setData(payload)
      setUser(payload.user)
      return payload
    } catch (err) {
      if (loadVersionRef.current === version) {
        const status = err && typeof err === 'object' ? err.status : undefined
        const message = err instanceof Error ? err.message : 'Không tải được bootstrap dashboard'
        const sessionExpired =
          status === 401 || /invalid or expired token/i.test(message)

        if (sessionExpired) {
          clearToken()
          setUser(null)
          setData(null)
          setError(null)
          return null
        }

        setError(message)
        setData(null)
      }
      throw err
    } finally {
      if (loadVersionRef.current === version) {
        setLoading(false)
        if (blockAuth) {
          setAuthLoading(false)
          initialSessionRef.current = false
        }
      }
    }
  }, [setUser, setAuthLoading])

  const retry = useCallback(() => loadBootstrap().catch(() => {}), [loadBootstrap])

  useEffect(() => {
    loadBootstrap().catch(() => {})
  }, [loadBootstrap])

  useEffect(() => {
    if (!user && !getToken()) {
      setData(null)
      setError(null)
      setLoading(false)
    }
  }, [user])

  const value = useMemo(
    () => ({
      data,
      loading,
      error,
      retry,
      refreshBootstrap: loadBootstrap,
      ready: Boolean(data) && !loading,
    }),
    [data, loading, error, retry, loadBootstrap],
  )

  return (
    <DashboardBootstrapContext.Provider value={value}>
      {children}
    </DashboardBootstrapContext.Provider>
  )
}

export function useDashboardBootstrap() {
  const context = useContext(DashboardBootstrapContext)
  if (!context) {
    throw new Error('useDashboardBootstrap must be used within DashboardBootstrapProvider')
  }
  return context
}
