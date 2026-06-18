import { Link } from 'react-router-dom'
import { LOGO_SRC } from '../components/BrandLogo'

function LoginPage() {
  return (
    <div className="login-page">
      <div className="login-card">
        <img src={LOGO_SRC} alt="TIN NGHIA AMS" className="login-page__logo-image" />
        <p className="login-page__tagline">AI GIÁM SÁT AN TOÀN SINH HỌC TRANG TRẠI HEO</p>

        <form className="login-form" onSubmit={(event) => event.preventDefault()}>
          <label className="login-form__field">
            <span>Email</span>
            <input type="email" placeholder="admin@ams.local" defaultValue="admin@ams.local" />
          </label>
          <label className="login-form__field">
            <span>Mật khẩu</span>
            <input type="password" placeholder="••••••••" defaultValue="admin123" />
          </label>
          <Link to="/dashboard" className="btn btn--primary login-form__submit">
            Đăng nhập
          </Link>
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
