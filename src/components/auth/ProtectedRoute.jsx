import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { useDashboardBootstrap } from '../../context/DashboardBootstrapStore'
import { clearToken, getToken } from '../../services/authService'

export default function ProtectedRoute({ children }) {
  const navigate = useNavigate()
  const { user, loading, setUser } = useAuth()
  const { error, retry, loading: bootstrapLoading } = useDashboardBootstrap()

  const hasToken = Boolean(getToken())

  function handleReLogin() {
    clearToken()
    setUser(null)
    navigate('/login', { replace: true })
  }

  if (loading || bootstrapLoading) {
    return <div>Đang tải...</div>
  }

  if (!user) {
    if (hasToken && error) {
      const sessionExpired = /invalid or expired token/i.test(error)

      return (
        <div className="login-page">
          <div className="login-card">
            <p>Không tải được dữ liệu phiên làm việc.</p>
            <p>{sessionExpired ? 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.' : error}</p>
            <button
              type="button"
              className="btn btn--primary"
              onClick={sessionExpired ? handleReLogin : retry}
            >
              {sessionExpired ? 'Đăng nhập lại' : 'Thử lại'}
            </button>
          </div>
        </div>
      )
    }

    if (hasToken) {
      return <div>Đang tải...</div>
    }

    return <Navigate to="/login" replace />
  }

  return children
}
