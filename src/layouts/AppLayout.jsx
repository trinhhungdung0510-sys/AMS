import { Outlet, useLocation } from 'react-router-dom'
import Header from '../components/Header'
import Sidebar from '../components/Sidebar'
import { getCameraById, pageMeta } from '../data/mockData'

function getPageMeta(pathname, search) {
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

  if (pathname === '/thiet-ke-vung-atsh' || pathname === '/settings/zones') {
    return {
      title: 'Thiết kế vùng ATSH',
      subtitle: 'Chỉnh sửa vùng an toàn sinh học trực tiếp trên hình ảnh camera',
    }
  }

  if (pathname.startsWith('/vi-pham-atsh/') || pathname.startsWith('/violations/')) {
    return {
      title: 'Chi tiết vi phạm ATSH',
      subtitle: 'Ảnh vi phạm, thông tin và timeline xử lý',
    }
  }

  if (pathname === '/vi-pham-atsh' || pathname === '/violations') {
    if (search.includes('tab=su-kien')) {
      return {
        title: 'Trung tâm vi phạm ATSH',
        subtitle: 'Bảng cảnh báo AI với tìm kiếm, lọc và xuất Excel',
      }
    }
    return pageMeta['vi-pham-atsh']
  }

  if (pathname === '/quy-tac-atsh' || pathname === '/rules') {
    return pageMeta['quy-tac-atsh']
  }

  if (pathname === '/bang-dieu-khien') {
    if (search.includes('tab=ban-do')) {
      return {
        title: 'Bảng điều khiển chủ trại',
        subtitle: 'Bản đồ trang trại — thiết kế sơ đồ ATSH trên nền vệ tinh',
      }
    }
    return pageMeta['bang-dieu-khien']
  }

  const key = pathname.split('/')[1] || 'dashboard'
  return pageMeta[key] ?? pageMeta.dashboard
}

function AppLayout() {
  const location = useLocation()
  const meta = getPageMeta(location.pathname, location.search)

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Header title={meta.title} subtitle={meta.subtitle} />
        <main className="page-content">
          <Outlet />
        </main>
        <footer className="app-footer">
          <p>© 2026 TIN NGHIA AMS</p>
          <p>AI Monitoring Technology Agriculture</p>
        </footer>
      </div>
    </div>
  )
}

export default AppLayout
