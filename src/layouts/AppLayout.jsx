import { Outlet, useLocation } from 'react-router-dom'
import Header from '../components/Header'
import Sidebar from '../components/Sidebar'
import { getCameraById, pageMeta } from '../data/mockData'

function getPageMeta(pathname) {
  if (pathname.startsWith('/monitoring/')) {
    const cameraId = pathname.split('/')[2]
    const camera = getCameraById(cameraId)
    return {
      title: camera?.name ?? 'Chi tiết camera',
      subtitle: camera
        ? `${camera.zone} · ${camera.id} · Giám sát AI thời gian thực`
        : pageMeta.cameraDetail.subtitle,
    }
  }

  if (pathname === '/settings/zones') {
    return {
      title: 'Zone Designer',
      subtitle: 'Thiết kế vùng biosecurity cho camera và lưu polygon xuống backend',
    }
  }

  const key = pathname.split('/')[1] || 'dashboard'
  return pageMeta[key] ?? pageMeta.dashboard
}

function AppLayout() {
  const location = useLocation()
  const meta = getPageMeta(location.pathname)

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Header title={meta.title} subtitle={meta.subtitle} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppLayout
