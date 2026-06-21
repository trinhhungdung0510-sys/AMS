import { APP_VERSION } from '../data/mockData'
import { Camera, FileImage, Gauge, LayoutDashboard, ListChecks, Monitor, Rocket, Settings, ShieldAlert, ShieldCheck, Shirt, Stethoscope } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { BrandLogo } from './BrandLogo'
import { useEffect, useState } from 'react'
import { fetchApiHealth } from '../services/deploymentService'

const menuItems = [
  { to: '/dashboard', label: 'Tổng quan', icon: LayoutDashboard },
  { to: '/bang-dieu-khien', label: 'Bảng điều khiển', icon: Gauge },
  { to: '/monitoring', label: 'Giám sát', icon: Monitor },
  { to: '/monitoring/compliance-center', label: 'Compliance Center', icon: FileImage },
  { to: '/compliance', label: 'Tuân thủ ATSH', icon: ShieldCheck },
  { to: '/vi-pham-atsh', label: 'Vi phạm ATSH', icon: ShieldAlert },
  { to: '/camera', label: 'Camera', icon: Camera },
  { to: '/uniforms', label: 'Đồng phục', icon: Shirt },
  { to: '/quy-tac-atsh', label: 'Quy tắc ATSH', icon: ListChecks },
  { to: '/setup', label: 'Setup Wizard', icon: Rocket },
  { to: '/system-status', label: 'System Status', icon: Gauge },
  { to: '/diagnostics', label: 'Diagnostics', icon: Stethoscope },
  { to: '/evidence', label: 'Evidence', icon: FileImage },
  { to: '/settings', label: 'Cài đặt', icon: Settings },
]

function Sidebar() {
  const [healthOk, setHealthOk] = useState(true)

  useEffect(() => {
    fetchApiHealth()
      .then((data) => setHealthOk(data.status === 'ok' || data.status === 'degraded'))
      .catch(() => setHealthOk(false))
  }, [])
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
        <span className={`sidebar__status-dot${healthOk ? '' : ' sidebar__status-dot--warn'}`} />
        {healthOk ? 'Hệ thống hoạt động' : 'Cần kiểm tra hệ thống'}
      </div>
    </aside>
  )
}

export default Sidebar
