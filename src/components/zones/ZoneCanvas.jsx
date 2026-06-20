import { useCallback, useEffect, useRef, useState } from 'react'
import {
  getImageMetrics,
  getReferenceFromMetrics,
  normalizedToScreenPoint,
  pointsToSvgString,
  resolveNormalizedPoints,
  roundNormalizedPoint,
  screenToNormalizedPoint,
} from '../../utils/zoneGeometry'

const CLICK_DELAY_MS = 250

function ZoneCanvas({
  previewUrl,
  zones,
  selectedZoneId,
  draftPoints,
  draftColor,
  isDrawing,
  onCanvasClick,
  onCanvasDoubleClick,
  onSelectZone,
  onMetricsChange,
}) {
  const containerRef = useRef(null)
  const imageRef = useRef(null)
  const clickTimerRef = useRef(null)
  const [metrics, setMetrics] = useState(null)
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 })

  const syncMetrics = useCallback(() => {
    const container = containerRef.current
    const image = imageRef.current
    if (!container || !image) return

    const rect = container.getBoundingClientRect()
    const nextMetrics = getImageMetrics(image, rect.width, rect.height)
    setContainerSize({ width: rect.width, height: rect.height })
    setMetrics(nextMetrics)
    onMetricsChange?.(nextMetrics)
  }, [onMetricsChange])

  useEffect(() => {
    syncMetrics()

    const container = containerRef.current
    if (!container || typeof ResizeObserver === 'undefined') {
      window.addEventListener('resize', syncMetrics)
      return () => window.removeEventListener('resize', syncMetrics)
    }

    const observer = new ResizeObserver(syncMetrics)
    observer.observe(container)
    window.addEventListener('resize', syncMetrics)

    return () => {
      observer.disconnect()
      window.removeEventListener('resize', syncMetrics)
      if (clickTimerRef.current) {
        clearTimeout(clickTimerRef.current)
      }
    }
  }, [previewUrl, syncMetrics])

  const appendPoint = (event) => {
    if (!isDrawing || !metrics) return

    const rect = containerRef.current.getBoundingClientRect()
    const point = roundNormalizedPoint(
      screenToNormalizedPoint(event.clientX, event.clientY, rect, metrics),
    )
    onCanvasClick?.(point)
  }

  const handleClick = (event) => {
    if (!isDrawing || !metrics) return
    if (event.detail > 1) return

    if (clickTimerRef.current) clearTimeout(clickTimerRef.current)
    clickTimerRef.current = setTimeout(() => {
      appendPoint(event)
      clickTimerRef.current = null
    }, CLICK_DELAY_MS)
  }

  const handleDoubleClick = (event) => {
    if (!isDrawing || draftPoints.length < 3) return
    event.preventDefault()
    if (clickTimerRef.current) {
      clearTimeout(clickTimerRef.current)
      clickTimerRef.current = null
    }
    onCanvasDoubleClick?.()
  }

  const fallbackReference = metrics ? getReferenceFromMetrics(metrics) : null

  return (
    <div className="zone-canvas" ref={containerRef}>
      {!previewUrl ? (
        <div className="zone-canvas__empty">Chưa có ảnh preview. Chụp snapshot ở tab Live View hoặc Settings.</div>
      ) : (
        <>
          <img
            ref={imageRef}
            src={previewUrl}
            alt="Camera preview"
            className="zone-canvas__image"
            onLoad={syncMetrics}
          />
          {metrics && containerSize.width > 0 ? (
            <svg
              className="zone-canvas__svg"
              viewBox={`0 0 ${containerSize.width} ${containerSize.height}`}
              onClick={handleClick}
              onDoubleClick={handleDoubleClick}
            >
              {zones.map((zone) => {
                const normalizedPoints = resolveNormalizedPoints(zone, fallbackReference)
                return (
                  <polygon
                    key={zone.id}
                    points={pointsToSvgString(normalizedPoints, metrics)}
                    fill={zone.color}
                    fillOpacity={zone.id === selectedZoneId ? 0.35 : 0.2}
                    stroke={zone.color}
                    strokeWidth={zone.id === selectedZoneId ? 3 : 2}
                    style={{ cursor: isDrawing ? 'crosshair' : 'pointer' }}
                    onClick={(event) => {
                      event.stopPropagation()
                      if (!isDrawing) onSelectZone?.(zone)
                    }}
                  />
                )
              })}

              {draftPoints.length > 0 ? (
                <>
                  <polyline
                    points={pointsToSvgString(draftPoints, metrics)}
                    fill={`${draftColor}33`}
                    stroke={draftColor}
                    strokeWidth={2}
                  />
                  {draftPoints.map((point, index) => {
                    const screen = normalizedToScreenPoint(point, metrics)
                    return (
                      <circle key={`draft-${index}`} cx={screen.x} cy={screen.y} r={5} fill={draftColor} />
                    )
                  })}
                </>
              ) : null}
            </svg>
          ) : null}
        </>
      )}
    </div>
  )
}

export default ZoneCanvas
