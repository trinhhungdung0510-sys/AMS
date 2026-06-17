import { APP_VERSION } from '../data/mockData'
import { Camera, LayoutDashboard, ListChecks, Map, Monitor, Settings, ShieldCheck, Siren } from 'lucide-react'
import { NavLink } from 'react-router-dom'

const menuItems = [
  { to: '/dashboard', label: 'Tổng quan', icon: LayoutDashboard },
  { to: '/monitoring', label: 'Giám sát', icon: Monitor },
  { to: '/compliance', label: 'Tuân thủ ATSH', icon: ShieldCheck },
  { to: '/camera', label: 'Camera', icon: Camera },
  { to: '/events', label: 'Sự kiện', icon: Siren },
  { to: '/rules', label: 'Quy tắc ATSH', icon: ListChecks },
  { to: '/map', label: 'Bản đồ', icon: Map },
  { to: '/settings', label: 'Cài đặt', icon: Settings },
]

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <div className="sidebar__logo-row">
          <div className="sidebar__logo">AMS</div>
          <span className="sidebar__version">{APP_VERSION}</span>
        </div>
        <span className="sidebar__subtitle">Trại heo</span>
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
