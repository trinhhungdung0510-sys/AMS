import { Navigate, Route, Routes, useParams } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import AtshRulesPage from '../pages/AtshRulesPage'
import CameraDetailPage from '../pages/CameraDetailPage'
import CameraPage from '../pages/CameraPage'
import ComplianceDashboardPage from '../pages/ComplianceDashboardPage'
import DashboardPage from '../pages/DashboardPage'
import EventsPage from '../pages/EventsPage'
import FarmControlDashboardPage from '../pages/FarmControlDashboardPage'
import LoginPage from '../pages/LoginPage'
import MonitoringPage from '../pages/MonitoringPage'
import SettingsPage from '../pages/SettingsPage'
import ViolationDetailPage from '../pages/ViolationDetailPage'
import ViolationsPage from '../pages/ViolationsPage'
import ZoneDesignerPage from '../pages/ZoneDesignerPage'

function ViolationLegacyRedirect() {
  const { id } = useParams()
  return <Navigate to={id ? `/vi-pham-atsh/${id}` : '/vi-pham-atsh'} replace />
}

function FarmMapRedirect() {
  return <Navigate to="/bang-dieu-khien?tab=ban-do" replace />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<AppLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/bang-dieu-khien" element={<FarmControlDashboardPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/compliance" element={<ComplianceDashboardPage />} />
        <Route path="/monitoring" element={<MonitoringPage />} />
        <Route path="/monitoring/:cameraId" element={<CameraDetailPage />} />
        <Route path="/camera" element={<CameraPage />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/vi-pham-atsh" element={<ViolationsPage />} />
        <Route path="/vi-pham-atsh/:id" element={<ViolationDetailPage />} />
        <Route path="/violations" element={<Navigate to="/vi-pham-atsh" replace />} />
        <Route path="/violations/:id" element={<ViolationLegacyRedirect />} />
        <Route path="/quy-tac-atsh" element={<AtshRulesPage />} />
        <Route path="/rules" element={<Navigate to="/quy-tac-atsh" replace />} />
        <Route path="/ban-do-trang-trai" element={<FarmMapRedirect />} />
        <Route path="/map" element={<FarmMapRedirect />} />
        <Route path="/thiet-ke-trang-trai" element={<FarmMapRedirect />} />
        <Route path="/thiet-ke-vung-atsh" element={<ZoneDesignerPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/settings/zones" element={<Navigate to="/thiet-ke-vung-atsh" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
