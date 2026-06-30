import { getZoneTypeLabel } from '../config/cameraZones'

function normalizeText(value) {
  return String(value || '').trim()
}

function looksLikeTechnicalCode(value) {
  const text = normalizeText(value)
  if (!text) return false
  return /^[a-z0-9_]+$/i.test(text) && text.includes('_')
}

export function resolveZoneTypeLabel(zone) {
  const typeLabel = normalizeText(zone?.typeLabel)
  const zoneType = normalizeText(zone?.type)

  if (typeLabel && !looksLikeTechnicalCode(typeLabel)) {
    return typeLabel
  }

  if (zoneType) {
    const mapped = getZoneTypeLabel(zoneType)
    if (mapped && mapped !== zoneType) {
      return mapped
    }
  }

  return typeLabel || zoneType || ''
}

export function getZoneOverlayDisplay(zone) {
  const name = normalizeText(zone?.name) || 'Vùng ATSH'
  const typeLabel = resolveZoneTypeLabel(zone)
  const showType = Boolean(typeLabel) && typeLabel.toLowerCase() !== name.toLowerCase()

  return {
    name,
    typeLabel: showType ? typeLabel : '',
  }
}

export function truncateZoneLabel(text, maxLength = 22) {
  const value = normalizeText(text)
  if (value.length <= maxLength) return value
  return `${value.slice(0, maxLength - 1)}…`
}
