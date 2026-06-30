/** Mirrors backend/app/core/roles.py */

export const SUPER_ADMIN = 'SUPER_ADMIN'
export const FARM_ADMIN = 'FARM_ADMIN'
export const VIEWER = 'VIEWER'

export const ROLE_ALIASES = {
  admin: SUPER_ADMIN,
  ADMIN: SUPER_ADMIN,
  super_admin: SUPER_ADMIN,
  farm_admin: FARM_ADMIN,
  viewer: VIEWER,
  'Quản trị viên': SUPER_ADMIN,
  'Chủ trại': FARM_ADMIN,
  'Farm Owner': FARM_ADMIN,
  'Chỉ xem': VIEWER,
}

export const PERMISSIONS = {
  [SUPER_ADMIN]: ['*'],
  [FARM_ADMIN]: [
    'farm.read',
    'farm.manage_own',
    'camera.read',
    'camera.manage',
    'zone.read',
    'zone.manage',
    'workflow.read',
    'workflow.manage',
    'uniform.read',
    'uniform.manage',
    'settings.read',
    'settings.write',
    'audit.read',
    'backup.read',
    'backup.write',
    'users.read',
    'users.manage_own_farm',
  ],
  [VIEWER]: [
    'farm.read',
    'camera.read',
    'zone.read',
    'workflow.read',
    'uniform.read',
    'settings.read',
    'audit.read',
  ],
}

export const ZONE_MANAGE_PERMISSION = 'zone.manage'
export const MANAGE_ZONE_PERMISSION = ZONE_MANAGE_PERMISSION
export const ZONE_READ_PERMISSION = 'zone.read'

export function normalizeRole(role) {
  if (!role) return VIEWER
  return ROLE_ALIASES[role] || role
}

export function roleHasPermission(role, permission) {
  const normalized = normalizeRole(role)
  const allowed = PERMISSIONS[normalized] || []
  return allowed.includes('*') || allowed.includes(permission)
}

export function canManageAtshZones(user) {
  if (!user?.role) return false
  return roleHasPermission(user.role, ZONE_MANAGE_PERMISSION)
}

/** Alias: MANAGE_ZONE permission required to draw/save/import/export zones. */
export const canManageZone = canManageAtshZones

export function canViewAtshZones(user) {
  if (!user?.role) return false
  return roleHasPermission(user.role, ZONE_READ_PERMISSION)
}

export function getAtshZoneRoleLabel(user) {
  if (!user?.role) return 'Khách'
  const role = normalizeRole(user.role)
  if (role === SUPER_ADMIN) return 'Quản trị hệ thống'
  if (role === FARM_ADMIN) return 'Chủ trại · Quản lý vùng ATSH'
  return 'Chỉ xem'
}
