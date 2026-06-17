import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import CameraDetailPage from '../pages/CameraDetailPage'
import CameraPage from '../pages/CameraPage'
import ComplianceDashboardPage from '../pages/ComplianceDashboardPage'
import DashboardPage from '../pages/DashboardPage'
import EventsPage from '../pages/EventsPage'
import FarmMapPage from '../pages/FarmMapPage'
import MonitoringPage from '../pages/MonitoringPage'
import RuleManagementPage from '../pages/RuleManagementPage'
import SettingsPage from '../pages/SettingsPage'
import ZoneDesignerPage from '../pages/ZoneDesignerPage'

function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/compliance" element={<ComplianceDashboardPage />} />
        <Route path="/monitoring" element={<MonitoringPage />} />
        <Route path="/monitoring/:cameraId" element={<CameraDetailPage />} />
        <Route path="/camera" element={<CameraPage />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/rules" element={<RuleManagementPage />} />
        <Route path="/map" element={<FarmMapPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/settings/zones" element={<ZoneDesignerPage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
