import { useMemo, useState } from 'react'
import { Bell } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { BrandLogo } from './BrandLogo'
import { useViolationProcessing } from '../context/ViolationProcessingContext'

function Header({ title, subtitle }) {
  const navigate = useNavigate()
  const { openMetrics } = useViolationProcessing()
  const [menuOpen, setMenuOpen] = useState(false)

  const today = new Date().toLocaleDateString('vi-VN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })

  const openCount = useMemo(() => {
    const total = Number(openMetrics?.openTotal ?? 0)
    return Number.isFinite(total) && total > 0 ? total : 0
  }, [openMetrics?.openTotal])

  const goToViolations = () => {
    setMenuOpen(false)
    navigate('/vi-pham-atsh')
  }

  const goToSettings = () => {
    setMenuOpen(false)
    navigate('/settings')
  }

  return (
    <header className="header">
      <div className="header__left">
        <BrandLogo height={48} showWordmark={false} to="/dashboard" className="header__brand brand-logo--horizontal" />
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
        <div className="header__alert-wrap">
          <button
            type="button"
            className="header__alert-btn"
            aria-label="Thông báo vi phạm"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <Bell size={20} />
            {openCount > 0 ? <span className="header__badge">{openCount > 99 ? '99+' : openCount}</span> : null}
          </button>
          {menuOpen ? (
            <div className="header__alert-menu panel" role="menu">
              <p className="header__alert-menu-title">Thông báo vi phạm ATSH</p>
              <p className="header__alert-menu-meta">
                {openCount > 0
                  ? `${openCount} vi phạm chưa xử lý cần theo dõi`
                  : 'Không có vi phạm mở — hệ thống đang ổn định'}
              </p>
              <div className="header__alert-menu-actions">
                <button type="button" className="btn btn--primary btn--sm" onClick={goToViolations}>
                  Mở trung tâm vi phạm
                </button>
                <button type="button" className="btn btn--outline btn--sm" onClick={goToSettings}>
                  Cài đặt thông báo
                </button>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </header>
  )
}

export default Header
