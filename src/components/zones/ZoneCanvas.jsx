import { useCallback, useEffect, useRef, useState } from 'react'
import { CANVAS_TOOLS } from './ZoneCanvasToolbar'
import {
  getImageMetrics,
  getReferenceFromMetrics,
  normalizedToScreenPoint,
  pointsToSvgString,
  polygonCentroidNormalized,
  rectFromNormalizedCorners,
  resolveNormalizedPoints,
  roundNormalizedPoint,
  screenToNormalizedPoint,
} from '../../utils/zoneGeometry'

const CLICK_DELAY_MS = 250
const MIN_ZOOM = 0.5
const MAX_ZOOM = 3

function ZoneCanvas({
  previewUrl,
  zones,
  selectedZoneId,
  draftPoints,
  draftColor,
  isDrawing,
  drawShape,
  activeTool,
  zoom,
  pan,
  showZoneNames,
  hideZones,
  onCanvasClick,
  onCanvasDoubleClick,
  onDraftPointsSet,
  onSelectZone,
  onPanChange,
  onZoomChange,
  onMetricsChange,
}) {
  const viewportRef = useRef(null)
  const containerRef = useRef(null)
  const imageRef = useRef(null)
  const clickTimerRef = useRef(null)
  const [metrics, setMetrics] = useState(null)
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 })
  const [rectStart, setRectStart] = useState(null)
  const [rectPreview, setRectPreview] = useState([])
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })

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
  }, [previewUrl, syncMetrics, zoom, pan.x, pan.y])

  useEffect(() => {
    if (drawShape !== 'rect') {
      setRectStart(null)
      setRectPreview([])
    }
  }, [drawShape, isDrawing])

  const readNormalizedPoint = useCallback((event) => {
    if (!metrics || !containerRef.current) return null

    const rect = containerRef.current.getBoundingClientRect()
    return roundNormalizedPoint(
      screenToNormalizedPoint(event.clientX, event.clientY, rect, metrics),
    )
  }, [metrics])

  const appendPoint = useCallback((event) => {
    if (!isDrawing || drawShape !== 'polygon' || !metrics) return

    const point = readNormalizedPoint(event)
    if (!point) return
    onCanvasClick?.(point)
  }, [drawShape, isDrawing, metrics, onCanvasClick, readNormalizedPoint])

  const handleClick = (event) => {
    if (activeTool === CANVAS_TOOLS.PAN) return

    if (isDrawing && drawShape === 'rect' && metrics) {
      const point = readNormalizedPoint(event)
      if (!point) return

      if (!rectStart) {
        setRectStart(point)
        setRectPreview(rectFromNormalizedCorners(point, point))
        return
      }

      const corners = rectFromNormalizedCorners(rectStart, point)
      onDraftPointsSet?.(corners)
      setRectStart(null)
      setRectPreview([])
      return
    }

    if (!isDrawing || drawShape !== 'polygon' || !metrics) return
    if (event.detail > 1) return

    if (clickTimerRef.current) clearTimeout(clickTimerRef.current)
    clickTimerRef.current = setTimeout(() => {
      appendPoint(event)
      clickTimerRef.current = null
    }, CLICK_DELAY_MS)
  }

  const handleDoubleClick = (event) => {
    if (!isDrawing || drawShape !== 'polygon' || draftPoints.length < 3) return
    event.preventDefault()
    if (clickTimerRef.current) {
      clearTimeout(clickTimerRef.current)
      clickTimerRef.current = null
    }
    onCanvasDoubleClick?.()
  }

  const handleMove = (event) => {
    if (isPanning && activeTool === CANVAS_TOOLS.PAN) {
      onPanChange?.({
        x: event.clientX - panStart.x,
        y: event.clientY - panStart.y,
      })
      return
    }

    if (!isDrawing || drawShape !== 'rect' || !rectStart || !metrics) return

    const point = readNormalizedPoint(event)
    if (!point) return
    setRectPreview(rectFromNormalizedCorners(rectStart, point))
  }

  const handlePointerDown = (event) => {
    if (activeTool !== CANVAS_TOOLS.PAN) return
    setIsPanning(true)
    setPanStart({ x: event.clientX - pan.x, y: event.clientY - pan.y })
  }

  const stopPanning = () => {
    setIsPanning(false)
  }

  const handleWheel = (event) => {
    event.preventDefault()
    const delta = event.deltaY > 0 ? -0.1 : 0.1
    const nextZoom = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, zoom + delta))
    onZoomChange?.(nextZoom)
  }

  const fallbackReference = metrics ? getReferenceFromMetrics(metrics) : null
  const previewPoints = rectPreview.length > 0 ? rectPreview : draftPoints
  const cursorClass = activeTool === CANVAS_TOOLS.PAN
    ? 'zone-editor-viewport--pan'
    : isDrawing
      ? 'zone-editor-viewport--draw'
      : 'zone-editor-viewport--select'

  return (
    <div
      ref={viewportRef}
      className={`zone-editor-viewport ${cursorClass}`}
      onWheel={handleWheel}
      onPointerDown={handlePointerDown}
      onPointerMove={handleMove}
      onPointerUp={stopPanning}
      onPointerLeave={stopPanning}
    >
      <div
        className="zone-editor-viewport__inner"
        style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})` }}
      >
        <div className="zone-canvas" ref={containerRef}>
          {!previewUrl ? (
            <div className="zone-canvas__empty">
              Chưa có ảnh preview. Chụp snapshot ở tab Live Camera hoặc Cài đặt.
            </div>
          ) : (
            <>
              <img
                ref={imageRef}
                src={previewUrl}
                alt="Camera preview"
                className="zone-canvas__image"
                draggable={false}
                onLoad={syncMetrics}
              />
              {metrics && containerSize.width > 0 ? (
                <svg
                  className="zone-canvas__svg"
                  viewBox={`0 0 ${containerSize.width} ${containerSize.height}`}
                  onClick={handleClick}
                  onDoubleClick={handleDoubleClick}
                >
                  <defs>
                    <filter id="zone-highlight-glow" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#ffffff" floodOpacity="0.85" />
                    </filter>
                  </defs>

                  {!hideZones && zones.map((zone) => {
                    const normalizedPoints = resolveNormalizedPoints(zone, fallbackReference)
                    const centroid = polygonCentroidNormalized(normalizedPoints)
                    const labelPoint = normalizedToScreenPoint(centroid, metrics)

                    return (
                      <g key={zone.id}>
                        <polygon
                          points={pointsToSvgString(normalizedPoints, metrics)}
                          fill={zone.color}
                          fillOpacity={zone.id === selectedZoneId ? 0.42 : 0.18}
                          stroke={zone.color}
                          strokeWidth={zone.id === selectedZoneId ? 3.5 : 2}
                          filter={zone.id === selectedZoneId ? 'url(#zone-highlight-glow)' : undefined}
                          style={{ cursor: activeTool === CANVAS_TOOLS.SELECT ? 'pointer' : 'default' }}
                          onClick={(event) => {
                            event.stopPropagation()
                            if (activeTool === CANVAS_TOOLS.SELECT && !isDrawing) {
                              onSelectZone?.(zone)
                            }
                          }}
                        />
                        {showZoneNames && !hideZones ? (
                          <text
                            x={labelPoint.x}
                            y={labelPoint.y}
                            className="zone-canvas__label"
                            textAnchor="middle"
                            dominantBaseline="middle"
                          >
                            {zone.name}
                          </text>
                        ) : null}
                      </g>
                    )
                  })}

                  {previewPoints.length > 0 ? (
                    <>
                      <polygon
                        points={pointsToSvgString(previewPoints, metrics)}
                        fill={`${draftColor}33`}
                        stroke={draftColor}
                        strokeWidth={2}
                        strokeDasharray={rectPreview.length > 0 ? '6 4' : undefined}
                      />
                      {previewPoints.map((point, index) => {
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
      </div>
    </div>
  )
}

export default ZoneCanvas
