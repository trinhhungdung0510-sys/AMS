import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useCameraZoneOverlay } from '../../hooks/useCameraZoneOverlay'
import { getRules } from '../../services/ruleService'
import {
  countZoneRules,
  getLiveZoneStatus,
} from '../../utils/zoneListUtils'
import {
  getZoneOverlayDisplay,
  truncateZoneLabel,
} from '../../utils/zoneOverlayLabels'
import {
  getImageMetricsCover,
  getReferenceFromMetrics,
  normalizedToScreenPoint,
  pointsToSvgString,
  polygonAreaNormalized,
  polygonCentroidNormalized,
  resolveNormalizedPoints,
} from '../../utils/zoneGeometry'

const LIVE_ZONE_FILL_OPACITY = 0.17
const TECHNICAL_ID_STORAGE_KEY = 'ams:zone-overlay-technical-id'

function readTechnicalIdEnabled() {
  try {
    return window.localStorage.getItem(TECHNICAL_ID_STORAGE_KEY) === 'true'
  } catch {
    return false
  }
}

function ZoneLiveOverlay({ cameraId, compact = false }) {
  const containerRef = useRef(null)
  const { zones } = useCameraZoneOverlay(cameraId)
  const [rules, setRules] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 })
  const [hoveredZoneId, setHoveredZoneId] = useState(null)
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 })
  const [showTechnicalId, setShowTechnicalId] = useState(readTechnicalIdEnabled)

  const loadRules = useCallback(async () => {
    if (!cameraId) return

    try {
      const ruleData = await getRules(cameraId)
      setRules(ruleData)
    } catch {
      setRules([])
    }
  }, [cameraId])

  useEffect(() => {
    loadRules()
  }, [loadRules])

  useEffect(() => {
    const syncTechnicalMode = () => {
      setShowTechnicalId(readTechnicalIdEnabled())
    }

    window.addEventListener('storage', syncTechnicalMode)
    return () => window.removeEventListener('storage', syncTechnicalMode)
  }, [])

  const syncMetrics = useCallback(() => {
    const container = containerRef.current
    if (!container) return

    const feed = container.closest('.camera-feed')
    const image = feed?.querySelector('.camera-feed__image')
    if (!image) return

    const rect = container.getBoundingClientRect()
    const nextMetrics = getImageMetricsCover(image, rect.width, rect.height)
    setContainerSize({ width: rect.width, height: rect.height })
    setMetrics(nextMetrics)
  }, [])

  useEffect(() => {
    syncMetrics()

    const container = containerRef.current
    if (!container) return undefined

    const feed = container.closest('.camera-feed')
    const image = feed?.querySelector('.camera-feed__image')

    const observer = typeof ResizeObserver !== 'undefined'
      ? new ResizeObserver(syncMetrics)
      : null

    observer?.observe(container)
    image?.addEventListener('load', syncMetrics)
    window.addEventListener('resize', syncMetrics)

    return () => {
      observer?.disconnect()
      image?.removeEventListener('load', syncMetrics)
      window.removeEventListener('resize', syncMetrics)
    }
  }, [syncMetrics, cameraId, zones.length])

  const fallbackReference = metrics ? getReferenceFromMetrics(metrics) : null
  const hoveredZone = zones.find((zone) => zone.id === hoveredZoneId) ?? null

  const hoveredDetails = useMemo(() => {
    if (!hoveredZone || !metrics) return null

    const points = resolveNormalizedPoints(hoveredZone, fallbackReference)
    const areaPercent = polygonAreaNormalized(points) * 100
    const labels = getZoneOverlayDisplay(hoveredZone)

    return {
      name: labels.name,
      typeLabel: labels.typeLabel,
      areaPercent: areaPercent.toFixed(1),
      ruleCount: countZoneRules(hoveredZone.id, rules),
      status: getLiveZoneStatus(hoveredZone, rules),
    }
  }, [fallbackReference, hoveredZone, metrics, rules])

  const handleZoneHover = (zone, event) => {
    const container = containerRef.current
    if (!container) return

    const rect = container.getBoundingClientRect()
    setHoveredZoneId(zone.id)
    setTooltipPos({
      x: event.clientX - rect.left + 12,
      y: event.clientY - rect.top + 12,
    })
  }

  return (
    <div className="zone-live-overlay" ref={containerRef}>
      {metrics && containerSize.width > 0 && zones.length > 0 ? (
        <svg
          className="zone-live-overlay__svg"
          viewBox={`0 0 ${containerSize.width} ${containerSize.height}`}
          aria-hidden="true"
        >
          {zones.map((zone) => {
            const normalizedPoints = resolveNormalizedPoints(zone, fallbackReference)
            if (normalizedPoints.length < 3) return null

            const centroid = polygonCentroidNormalized(normalizedPoints)
            const labelPoint = normalizedToScreenPoint(centroid, metrics)
            const labels = getZoneOverlayDisplay(zone)
            const primaryLabel = truncateZoneLabel(labels.name, compact ? 14 : 24)
            const labelClass = compact
              ? 'zone-live-overlay__label zone-live-overlay__label--compact'
              : 'zone-live-overlay__label'

            return (
              <g
                key={zone.id}
                className="zone-live-overlay__zone"
                onMouseEnter={(event) => handleZoneHover(zone, event)}
                onMouseMove={(event) => handleZoneHover(zone, event)}
                onMouseLeave={() => setHoveredZoneId(null)}
              >
                <polygon
                  points={pointsToSvgString(normalizedPoints, metrics)}
                  fill={zone.color}
                  fillOpacity={LIVE_ZONE_FILL_OPACITY}
                  stroke={zone.color}
                  strokeWidth={compact ? 2 : 2.5}
                />
                <text
                  x={labelPoint.x}
                  y={labelPoint.y}
                  className={labelClass}
                  textAnchor="middle"
                  dominantBaseline="middle"
                >
                  {primaryLabel}
                </text>
                {!compact && labels.typeLabel ? (
                  <text
                    x={labelPoint.x}
                    y={labelPoint.y + 14}
                    className="zone-live-overlay__label zone-live-overlay__label--type"
                    textAnchor="middle"
                    dominantBaseline="middle"
                  >
                    {truncateZoneLabel(labels.typeLabel, 20)}
                  </text>
                ) : null}
                {showTechnicalId ? (
                  <>
                    <text
                      x={labelPoint.x}
                      y={labelPoint.y + 14}
                      className="zone-live-overlay__label zone-live-overlay__label--id"
                      textAnchor="middle"
                      dominantBaseline="middle"
                    >
                      {zone.id} · {normalizedPoints.length} điểm
                    </text>
                    {normalizedPoints.map((point, index) => {
                      const vertex = normalizedToScreenPoint(point, metrics)
                      return (
                        <g key={`${zone.id}-vertex-${index}`}>
                          <circle
                            cx={vertex.x}
                            cy={vertex.y}
                            r={5}
                            fill={zone.color}
                            stroke="#ffffff"
                            strokeWidth={1.5}
                          />
                          <text
                            x={vertex.x}
                            y={vertex.y + 3}
                            className="zone-live-overlay__label zone-live-overlay__label--vertex"
                            textAnchor="middle"
                            dominantBaseline="middle"
                          >
                            {index + 1}
                          </text>
                        </g>
                      )
                    })}
                  </>
                ) : null}
              </g>
            )
          })}
        </svg>
      ) : null}

      {hoveredDetails ? (
        <div
          className="zone-live-overlay__tooltip"
          style={{ left: `${tooltipPos.x}px`, top: `${tooltipPos.y}px` }}
          role="tooltip"
        >
          <strong>{hoveredDetails.name}</strong>
          <dl>
            {hoveredDetails.typeLabel ? (
              <div><dt>Loại vùng</dt><dd>{hoveredDetails.typeLabel}</dd></div>
            ) : null}
            <div><dt>Diện tích</dt><dd>{hoveredDetails.areaPercent}%</dd></div>
            <div><dt>Số Rule</dt><dd>{hoveredDetails.ruleCount}</dd></div>
            <div><dt>Trạng thái</dt><dd>{hoveredDetails.status}</dd></div>
          </dl>
        </div>
      ) : null}
    </div>
  )
}

export default ZoneLiveOverlay
