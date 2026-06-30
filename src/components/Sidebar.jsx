import { useEffect, useState } from 'react'
import { APP_VERSION } from '../data/mockData'
import {
  Camera,
  ChevronDown,
  Gauge,
  ListChecks,
  Monitor,
  Settings,
  Shapes,
  ShieldAlert,
  Shirt,
} from 'lucide-react'
import { NavLink, useLocation } from 'react-router-dom'
import { BrandLogo } from './BrandLogo'
import { useDashboardBootstrap } from '../context/DashboardBootstrapStore'

const ICON_SIZE = 20

const menuGroups = [
  {
    title: 'TỔNG QUAN',
    items: [
      {
        to: '/bang-dieu-khien',
        label: 'Bảng điều khiển',
        icon: Gauge,
        activePaths: ['/bang-dieu-khien', '/dashboard'],
        children: [
          {
            to: '/thiet-ke-vung-atsh',
            label: 'Thiết kế vùng ATSH',
            icon: Shapes,
            activePaths: ['/thiet-ke-vung-atsh', '/settings/zones'],
          },
        ],
      },
    ],
  },
  {
    title: 'GIÁM SÁT',
    items: [
      {
        to: '/monitoring',
        label: 'Giám sát trực tiếp',
        icon: Monitor,
        activePaths: ['/monitoring'],
        excludePaths: ['/monitoring/compliance-center'],
        children: [
          {
            to: '/camera',
            label: 'Camera',
            icon: Camera,
            activePaths: ['/camera'],
          },
        ],
      },
    ],
  },
  {
    title: 'AN TOÀN SINH HỌC',
    items: [
      {
        to: '/quy-tac-atsh',
        label: 'Quy tắc ATSH',
        icon: ListChecks,
        activePaths: ['/quy-tac-atsh'],
        children: [
          {
            to: '/uniforms',
            label: 'Đồng phục',
            icon: Shirt,
            activePaths: ['/uniforms'],
          },
        ],
      },
      { to: '/vi-pham-atsh', label: 'Vi phạm ATSH', icon: ShieldAlert, activePaths: ['/vi-pham-atsh'] },
    ],
  },
  {
    title: 'HỆ THỐNG',
    items: [
      {
        to: '/settings',
        label: 'Cài đặt',
        icon: Settings,
        activePaths: ['/settings', '/setup', '/system-status', '/diagnostics'],
      },
    ],
  },
]

function isMenuItemActive(location, item) {
  const pathname = location.pathname
  const excluded = item.excludePaths ?? []

  if (excluded.some((path) => pathname === path || pathname.startsWith(`${path}/`))) {
    return false
  }

  return (item.activePaths ?? [item.to]).some((path) => {
    if (pathname === path) return true
    if (path === '/monitoring') {
      return pathname.startsWith('/monitoring/') && !pathname.startsWith('/monitoring/compliance-center')
    }
    if (path === '/vi-pham-atsh') {
      return pathname.startsWith('/vi-pham-atsh/')
    }
    return pathname.startsWith(`${path}/`)
  })
}

function isGroupExpanded(location, item, expandedGroups) {
  if (expandedGroups[item.to]) return true
  if (isMenuItemActive(location, item)) return true
  return (item.children ?? []).some((child) => isMenuItemActive(location, child))
}

function Sidebar() {
  const location = useLocation()
  const { data } = useDashboardBootstrap()
  const healthStatus = data?.systemHealth?.status
  const healthOk = healthStatus === 'ok' || healthStatus === 'degraded' || healthStatus == null
  const [expandedGroups, setExpandedGroups] = useState({})

  useEffect(() => {
    const nextExpanded = {}
    menuGroups.forEach((group) => {
      group.items.forEach((item) => {
        if (!item.children?.length) return
        const childActive = item.children.some((child) => isMenuItemActive(location, child))
        const parentActive = isMenuItemActive(location, item)
        if (childActive || parentActive) {
          nextExpanded[item.to] = true
        }
      })
    })

    if (Object.keys(nextExpanded).length) {
      setExpandedGroups((current) => ({ ...current, ...nextExpanded }))
    }
  }, [location.pathname])

  const toggleGroup = (itemTo) => {
    setExpandedGroups((current) => ({ ...current, [itemTo]: !current[itemTo] }))
  }

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
        {menuGroups.map((group, groupIndex) => (
          <div key={group.title} className="sidebar__group">
            {groupIndex > 0 ? <div className="sidebar__divider" aria-hidden="true" /> : null}
            <p className="sidebar__group-title">{group.title}</p>
            <ul className="sidebar__group-list">
              {group.items.map((item) => {
                const Icon = item.icon
                const hasChildren = (item.children ?? []).length > 0
                const expanded = hasChildren ? isGroupExpanded(location, item, expandedGroups) : false
                const parentActive = hasChildren
                  ? isMenuItemActive(location, item) && !item.children.some((child) => isMenuItemActive(location, child))
                  : isMenuItemActive(location, item)

                if (hasChildren) {
                  return (
                    <li key={item.to} className="sidebar__tree-item">
                      <div className={`sidebar__tree-row${expanded ? ' sidebar__tree-row--expanded' : ''}`}>
                        <NavLink
                          to={item.to}
                          end={item.to === '/monitoring' || item.to === '/quy-tac-atsh' || item.to === '/bang-dieu-khien'}
                          className={`sidebar__item${parentActive ? ' sidebar__item--active' : ''}`}
                        >
                          <span className="sidebar__icon">
                            <Icon size={ICON_SIZE} strokeWidth={2} />
                          </span>
                          {item.label}
                        </NavLink>
                        <button
                          type="button"
                          className="sidebar__tree-toggle"
                          aria-expanded={expanded}
                          aria-label={`${expanded ? 'Thu gọn' : 'Mở rộng'} ${item.label}`}
                          onClick={() => toggleGroup(item.to)}
                        >
                          <ChevronDown size={16} />
                        </button>
                      </div>
                      {expanded ? (
                        <ul className="sidebar__submenu">
                          {item.children.map((child) => {
                            const ChildIcon = child.icon
                            const childActive = isMenuItemActive(location, child)
                            return (
                              <li key={child.to}>
                                <NavLink
                                  to={child.to}
                                  className={`sidebar__item sidebar__item--child${childActive ? ' sidebar__item--active' : ''}`}
                                >
                                  <span className="sidebar__icon">
                                    <ChildIcon size={ICON_SIZE} strokeWidth={2} />
                                  </span>
                                  {child.label}
                                </NavLink>
                              </li>
                            )
                          })}
                        </ul>
                      ) : null}
                    </li>
                  )
                }

                return (
                  <li key={item.to}>
                    <NavLink
                      to={item.to}
                      className={`sidebar__item${parentActive ? ' sidebar__item--active' : ''}`}
                    >
                      <span className="sidebar__icon">
                        <Icon size={ICON_SIZE} strokeWidth={2} />
                      </span>
                      {item.label}
                    </NavLink>
                  </li>
                )
              })}
            </ul>
          </div>
        ))}
      </nav>

      <div className="sidebar__footer">
        <span className={`sidebar__status-dot${healthOk ? '' : ' sidebar__status-dot--warn'}`} />
        {healthOk ? 'Hệ thống hoạt động' : 'Cần kiểm tra hệ thống'}
      </div>
    </aside>
  )
}

export default Sidebar
