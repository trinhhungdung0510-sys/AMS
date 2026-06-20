import { bboxCenter, pointInPolygon, resolveNormalizedPoints } from '../utils/zoneGeometry'

/**
 * Map observation objects to camera zones/subzones using point-in-polygon.
 *
 * @param {object} observation
 * @param {Array<object>} zones
 * @returns {Array<{ objectId: string, zones: string[], subzones: string[] }>}
 */
export function mapObservationToZones(observation, zones) {
  const objects = observation?.objects || []
  const zoneList = zones || []

  return objects.map((objectItem) => {
    const trackId = objectItem.trackId || objectItem.track_id
    const center = bboxCenter(objectItem.bbox)
    const zonesMatched = []
    const subzonesMatched = []

    zoneList.forEach((zone) => {
      const polygon = resolveNormalizedPoints(zone, {
        width: observation.frame_width || observation.frameWidth,
        height: observation.frame_height || observation.frameHeight,
      })

      if (!pointInPolygon(center, polygon)) return

      if (zone.parent_zone_id) {
        subzonesMatched.push(zone.id)
      } else {
        zonesMatched.push(zone.id)
      }
    })

    return {
      objectId: trackId,
      zones: zonesMatched,
      subzones: subzonesMatched,
    }
  })
}

/**
 * Flat list of all zone ids (root + subzone) containing an object.
 */
export function getMatchedZoneIds(mapping) {
  return [...(mapping?.zones || []), ...(mapping?.subzones || [])]
}

export function findMappingForObject(mappings, trackId) {
  return mappings.find((item) => item.objectId === trackId) || null
}

export function objectInZone(mapping, zoneId) {
  if (!mapping || !zoneId) return false
  return mapping.zones.includes(zoneId) || mapping.subzones.includes(zoneId)
}
