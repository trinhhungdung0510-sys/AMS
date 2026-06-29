import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { LOGO_SRC } from '../components/BrandLogo'
import { useAuth } from '../context/AuthContext'
import { login as authLogin, getToken } from '../services/authService'
import { useDashboardBootstrap } from '../context/DashboardBootstrapStore'

function LoginPage() {
  const navigate = useNavigate()
  const { user, loading, setUser } = useAuth()
  const { refreshBootstrap, loading: bootstrapLoading } = useDashboardBootstrap()
  const [email, setEmail] = useState('admin@ams.local')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if ((loading || bootstrapLoading) && getToken() && !user) {
    return <div className="login-page farm-gis-map__loading">Đang tải…</div>
  }

  if (user) {
    return <Navigate to="/dashboard" replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    setError('')

    try {
      const session = await authLogin(email, password)
      if (session?.user) {
        setUser(session.user)
      }
      void refreshBootstrap()
      navigate('/dashboard', { replace: true })
    } catch {
      setError('Email hoặc mật khẩu không đúng')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <img src={LOGO_SRC} alt="TIN NGHIA AMS" className="login-page__logo-image" />
        <p className="login-page__tagline">AI GIÁM SÁT AN TOÀN SINH HỌC TRANG TRẠI HEO</p>

        <form className="login-form" onSubmit={handleSubmit}>
          <label className="login-form__field">
            <span>Email</span>
            <input
              type="email"
              placeholder="admin@ams.local"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              autoComplete="username"
              required
            />
          </label>
          <label className="login-form__field">
            <span>Mật khẩu</span>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
              required
            />
          </label>
          {error ? <p className="login-form__error">{error}</p> : null}
          <button type="submit" className="btn btn--primary login-form__submit" disabled={submitting}>
            {submitting ? 'Đang đăng nhập…' : 'Đăng nhập'}
          </button>
        </form>
      </div>

      <footer className="app-footer login-page__footer">
        <p>© 2026 TIN NGHIA AMS</p>
        <p>AI Monitoring Technology Agriculture</p>
      </footer>
    </div>
  )
}

export default LoginPage
