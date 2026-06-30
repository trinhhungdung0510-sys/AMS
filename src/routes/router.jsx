import { createBrowserRouter, Navigate, useParams } from 'react-router-dom'
import ProtectedRoute from '../components/auth/ProtectedRoute'
import AppLayout from '../layouts/AppLayout'
import AtshRulesPage from '../pages/AtshRulesPage'
import CameraDetailPage from '../pages/CameraDetailPage'
import CameraPage from '../pages/CameraPage'
import ComplianceCenterPage from '../pages/ComplianceCenterPage'
import ComplianceDashboardPage from '../pages/ComplianceDashboardPage'
import DashboardPage from '../pages/DashboardPage'
import DiagnosticsPage from '../pages/DiagnosticsPage'
import EventsPage from '../pages/EventsPage'
import FarmControlDashboardPage from '../pages/FarmControlDashboardPage'
import LoginPage from '../pages/LoginPage'
import MonitoringPage from '../pages/MonitoringPage'
import SettingsPage from '../pages/SettingsPage'
import SetupWizardPage from '../pages/SetupWizardPage'
import SnapshotBrowserPage from '../pages/SnapshotBrowserPage'
import SystemStatusPage from '../pages/SystemStatusPage'
import UniformsPage from '../pages/UniformsPage'
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

function ProtectedAppLayout() {
  return (
    <ProtectedRoute>
      <AppLayout />
    </ProtectedRoute>
  )
}

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: <ProtectedAppLayout />,
    children: [
      { index: true, element: <Navigate to="/bang-dieu-khien" replace /> },
      { path: 'bang-dieu-khien', element: <FarmControlDashboardPage /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'compliance', element: <ComplianceDashboardPage /> },
      { path: 'monitoring', element: <MonitoringPage /> },
      { path: 'monitoring/compliance-center', element: <ComplianceCenterPage /> },
      { path: 'monitoring/:cameraId', element: <CameraDetailPage /> },
      { path: 'camera', element: <CameraPage /> },
      { path: 'events', element: <EventsPage /> },
      { path: 'vi-pham-atsh', element: <ViolationsPage /> },
      { path: 'vi-pham-atsh/:id', element: <ViolationDetailPage /> },
      { path: 'violations', element: <Navigate to="/vi-pham-atsh" replace /> },
      { path: 'violations/:id', element: <ViolationLegacyRedirect /> },
      { path: 'quy-tac-atsh', element: <AtshRulesPage /> },
      { path: 'rules', element: <Navigate to="/quy-tac-atsh" replace /> },
      { path: 'ban-do-trang-trai', element: <FarmMapRedirect /> },
      { path: 'map', element: <FarmMapRedirect /> },
      { path: 'thiet-ke-trang-trai', element: <FarmMapRedirect /> },
      { path: 'thiet-ke-vung-atsh', element: <ZoneDesignerPage /> },
      { path: 'setup', element: <SetupWizardPage /> },
      { path: 'system-status', element: <SystemStatusPage /> },
      { path: 'diagnostics', element: <DiagnosticsPage /> },
      { path: 'evidence', element: <SnapshotBrowserPage /> },
      { path: 'uniforms', element: <UniformsPage /> },
      { path: 'settings', element: <SettingsPage /> },
      { path: 'settings/zones', element: <Navigate to="/thiet-ke-vung-atsh" replace /> },
      { path: '*', element: <Navigate to="/bang-dieu-khien" replace /> },
    ],
  },
])
