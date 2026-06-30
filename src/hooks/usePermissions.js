import { useMemo } from 'react'
import { useAuth } from '../context/AuthContext'
import {
  canManageAtshZones,
  canViewAtshZones,
  getAtshZoneRoleLabel,
  roleHasPermission,
} from '../utils/permissions'

export function usePermissions() {
  const { user } = useAuth()

  return useMemo(() => ({
    user,
    role: user?.role ?? null,
    roleLabel: getAtshZoneRoleLabel(user),
    canManageAtshZones: canManageAtshZones(user),
    canViewAtshZones: canViewAtshZones(user),
    hasPermission: (permission) => roleHasPermission(user?.role, permission),
  }), [user])
}
