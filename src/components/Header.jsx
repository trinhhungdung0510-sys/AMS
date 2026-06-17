import { Bell } from 'lucide-react'

function Header({ title, subtitle }) {
  const today = new Date().toLocaleDateString('vi-VN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })

  return (
    <header className="header">
      <div className="header__left">
        <div className="header__logo">AMS</div>
        <div className="header__title-group">
          <div className="header__breadcrumb">
            <span>Hệ thống giám sát AI</span>
            <span className="header__breadcrumb-separator">/</span>
            <span className="header__breadcrumb-current">{title}</span>
          </div>
          <h1 className="header__title">{title}</h1>
          <p className="header__subtitle">{subtitle}</p>
        </div>
      </div>

      <div className="header__right">
        <span className="header__date">{today}</span>
        <button type="button" className="header__alert-btn" aria-label="Thông báo">
          <Bell size={20} />
          <span className="header__badge">12</span>
        </button>
      </div>
    </header>
  )
}

export default Header
