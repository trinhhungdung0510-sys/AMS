import { APP_VERSION } from '../data/mockData'
import { Camera, Gauge, LayoutDashboard, ListChecks, Monitor, Settings, ShieldAlert, ShieldCheck } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { BrandLogo } from './BrandLogo'

const menuItems = [
  { to: '/dashboard', label: 'Tổng quan', icon: LayoutDashboard },
  { to: '/bang-dieu-khien', label: 'Bảng điều khiển', icon: Gauge },
  { to: '/monitoring', label: 'Giám sát', icon: Monitor },
  { to: '/compliance', label: 'Tuân thủ ATSH', icon: ShieldCheck },
  { to: '/vi-pham-atsh', label: 'Vi phạm ATSH', icon: ShieldAlert },
  { to: '/camera', label: 'Camera', icon: Camera },
  { to: '/quy-tac-atsh', label: 'Quy tắc ATSH', icon: ListChecks },
  { to: '/settings', label: 'Cài đặt', icon: Settings },
]

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <BrandLogo
          height={56}
          showWordmark={false}
          onDark
          className="sidebar__brand-logo brand-logo--horizontal brand-logo--sidebar"
        />
        <span className="sidebar__version">{APP_VERSION}</span>
      </div>

      <nav className="sidebar__nav">
        {menuItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `sidebar__item${isActive ? ' sidebar__item--active' : ''}`
              }
            >
              <span className="sidebar__icon">
                <Icon size={20} />
              </span>
              {item.label}
            </NavLink>
          )
        })}
      </nav>

      <div className="sidebar__footer">
        <span className="sidebar__status-dot" />
        Hệ thống hoạt động
      </div>
    </aside>
  )
}

export default Sidebar
