import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  Copy,
  Download,
  Expand,
  Hand,
  MousePointer2,
  PenLine,
  Plus,
  Redo2,
  RotateCcw,
  Save,
  Search,
  Shapes,
  Square,
  Trash2,
  ZoomIn,
  ZoomOut,
} from 'lucide-react'
import {
  CANVAS_HEIGHT,
  CANVAS_WIDTH,
  DESIGNER_CAMERAS,
  FARMS,
  RISK_LEVELS,
  RULE_OPTIONS,
  ZONE_CATEGORIES,
  categoryMeta,
  defaultRulesForCategory,
  mapZoneFromApi,
} from '../data/zoneDesignerPro'
import {
  DEFAULT_ZONE_OPACITY,
  closestEdgeIndex,
  duplicatePoints,
  edgeMidpoint,
  getCanvasPoint,
  insertPointOnEdge,
  moveEdgePoints,
  polygonCentroid,
  rectFromCorners,
  removePointAtIndex,
  toPoints,
  translatePoints,
} from '../data/zoneDesignerGeometry'
import { cameras } from '../data/mockData'

const API_BASE_URL = 'http://127.0.0.1:8000'

function ZoneDesignerPage() {
  const canvasRef = useRef(null)
  const viewportRef = useRef(null)
  const [farmFilter, setFarmFilter] = useState('all')
  const [cameraSearch, setCameraSearch] = useState('')
  const [selectedCameraId, setSelectedCameraId] = useState(DESIGNER_CAMERAS[0].id)
  const [zones, setZones] = useState([])
  const [flows, setFlows] = useState([])
  const [selectedZoneId, setSelectedZoneId] = useState(null)
  const [selectedFlowId, setSelectedFlowId] = useState(null)
  const [selectedVertexIndex, setSelectedVertexIndex] = useState(null)
  const [draftPoints, setDraftPoints] = useState([])
  const [draftLinePoints, setDraftLinePoints] = useState([])
  const [rectStart, setRectStart] = useState(null)
  const [rectPreview, setRectPreview] = useState(null)
  const [zoneName, setZoneName] = useState('Vùng ATSH mới')
  const [zoneCategory, setZoneCategory] = useState('intermediate')
  const [riskLevel, setRiskLevel] = useState('yellow')
  const [zoneColor, setZoneColor] = useState(categoryMeta('intermediate').color)
  const [zoneOpacity, setZoneOpacity] = useState(DEFAULT_ZONE_OPACITY)
  const [zoneDescription, setZoneDescription] = useState('')
  const [zoneRules, setZoneRules] = useState(defaultRulesForCategory('intermediate'))
  const [mode, setMode] = useState('select')
  const [dragState, setDragState] = useState(null)
  const [apiStatus, setApiStatus] = useState('Thiết kế vùng ATSH · Sẵn sàng')
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [historyPast, setHistoryPast] = useState([])
  const [historyFuture, setHistoryFuture] = useState([])
  const [frameTick, setFrameTick] = useState(0)

  const selectedCamera = useMemo(
    () => DESIGNER_CAMERAS.find((item) => item.id === selectedCameraId) ?? DESIGNER_CAMERAS[0],
    [selectedCameraId],
  )

  const cameraMeta = useMemo(
    () => cameras.find((item) => item.id === selectedCameraId) ?? cameras[0],
    [selectedCameraId],
  )

  const filteredCameras = useMemo(() => {
    const query = cameraSearch.trim().toLowerCase()
    return DESIGNER_CAMERAS.filter((camera) => {
      const matchFarm = farmFilter === 'all' || camera.farmId === farmFilter
      const matchSearch =
        query === ''
        || camera.name.toLowerCase().includes(query)
        || camera.zone.toLowerCase().includes(query)
        || camera.id.toLowerCase().includes(query)
      return matchFarm && matchSearch
    })
  }, [cameraSearch, farmFilter])

  const selectedZone = useMemo(
    () => zones.find((zone) => zone.id === selectedZoneId),
    [selectedZoneId, zones],
  )

  const selectedCategory = categoryMeta(zoneCategory)
  const frameUrl = `${API_BASE_URL}/api/cameras/${selectedCameraId}/frame?t=${frameTick}`

  const makeSnapshot = useCallback(
    () => ({ zones, flows }),
    [zones, flows],
  )

  const pushHistory = useCallback(() => {
    setHistoryPast((prev) => [...prev.slice(-30), makeSnapshot()])
    setHistoryFuture([])
  }, [makeSnapshot])

  const loadZones = useCallback(async (cameraId) => {
    try {
      setApiStatus('Đang tải vùng ATSH...')
      const response = await fetch(`${API_BASE_URL}/api/zones?camera_id=${encodeURIComponent(cameraId)}`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      const cameraZones = data.map(mapZoneFromApi)
      setZones(cameraZones)
      setSelectedZoneId(cameraZones[0]?.id ?? null)
      setSelectedVertexIndex(null)
      setApiStatus(`${cameraZones.length} vùng trên camera`)
    } catch (error) {
      setZones([])
      setApiStatus(`Không tải được vùng: ${error.message}`)
    }
  }, [])

  useEffect(() => {
    loadZones(selectedCameraId)
    setDraftPoints([])
    setDraftLinePoints([])
    setRectStart(null)
    setRectPreview(null)
    setMode('select')
    setHistoryPast([])
    setHistoryFuture([])
    setFrameTick(Date.now())
  }, [selectedCameraId, loadZones])

  useEffect(() => {
    if (cameraMeta.status !== 'online') return undefined
    const timer = setInterval(() => setFrameTick(Date.now()), 15000)
    return () => clearInterval(timer)
  }, [cameraMeta.status, selectedCameraId])

  useEffect(() => {
    if (!selectedZone) return
    setZoneName(selectedZone.zone_name)
    setZoneCategory(selectedZone.category || 'intermediate')
    setRiskLevel(selectedZone.riskLevel || selectedZone.biosecurity_level || 'yellow')
    setZoneColor(selectedZone.color || categoryMeta(selectedZone.category).color)
    setZoneOpacity(selectedZone.opacity ?? DEFAULT_ZONE_OPACITY)
    setZoneDescription(selectedZone.description || '')
    setZoneRules(selectedZone.rules || defaultRulesForCategory(selectedZone.category))
    setSelectedVertexIndex(null)
  }, [selectedZone])

  useEffect(() => {
    if (selectedZone) return
    const meta = categoryMeta(zoneCategory)
    setZoneColor(meta.color)
    setZoneRules(defaultRulesForCategory(zoneCategory))
    setRiskLevel(meta.level)
  }, [zoneCategory, selectedZone])

  const resetDraft = () => {
    setDraftPoints([])
    setDraftLinePoints([])
    setRectStart(null)
    setRectPreview(null)
  }

  const setTool = (tool) => {
    setMode(tool)
    resetDraft()
    setSelectedVertexIndex(null)
  }

  const readPoint = (event) => getCanvasPoint(event, canvasRef, zoom, pan, CANVAS_WIDTH, CANVAS_HEIGHT)

  const updateSelectedZonePoints = (points) => {
    if (!selectedZone) return
    setZones((prev) => prev.map((zone) =>
      zone.id === selectedZone.id ? { ...zone, polygon_points: points } : zone,
    ))
  }

  const handleCanvasClick = (event) => {
    const point = readPoint(event)

    if (mode === 'polygon') {
      setDraftPoints((prev) => [...prev, point])
      return
    }

    if (mode === 'rect') {
      if (!rectStart) {
        setRectStart(point)
        setRectPreview(rectFromCorners(point, point))
        return
      }
      setDraftPoints(rectFromCorners(rectStart, point))
      setRectStart(null)
      setRectPreview(null)
      return
    }

    if (mode === 'line') {
      setDraftLinePoints((prev) => [...prev, point])
      return
    }

    if (mode === 'select' && selectedZone && event.detail === 2) {
      const edgeIndex = closestEdgeIndex(point, selectedZone.polygon_points)
      pushHistory()
      updateSelectedZonePoints(insertPointOnEdge(selectedZone.polygon_points, edgeIndex, point))
      setApiStatus('Đã thêm điểm điều khiển')
    }
  }

  const handleCanvasMove = (event) => {
    if (mode === 'rect' && rectStart) {
      setRectPreview(rectFromCorners(rectStart, readPoint(event)))
      return
    }

    if (!dragState || !selectedZone) return
    const point = readPoint(event)

    if (dragState.type === 'vertex') {
      const nextPoints = selectedZone.polygon_points.map((item, index) =>
        index === dragState.index ? point : item,
      )
      updateSelectedZonePoints(nextPoints)
      return
    }

    if (dragState.type === 'edge') {
      const delta = [point[0] - dragState.last[0], point[1] - dragState.last[1]]
      updateSelectedZonePoints(moveEdgePoints(dragState.basePoints, dragState.index, delta))
      setDragState((prev) => ({ ...prev, last: point }))
      return
    }

    if (dragState.type === 'zone') {
      const delta = [point[0] - dragState.start[0], point[1] - dragState.start[1]]
      updateSelectedZonePoints(translatePoints(dragState.basePoints, delta[0], delta[1]))
    }
  }

  const finishLine = () => {
    if (draftLinePoints.length < 2) return
    pushHistory()
    const newFlow = {
      id: `flow-${Date.now()}`,
      name: 'Luồng di chuyển',
      points: draftLinePoints,
    }
    setFlows((prev) => [...prev, newFlow])
    setSelectedFlowId(newFlow.id)
    resetDraft()
    setMode('select')
    setApiStatus('Đã thêm đường')
  }

  const buildPayload = (points) => {
    const meta = categoryMeta(zoneCategory)
    return {
      farm_id: selectedCamera.farmId,
      camera_id: selectedCameraId,
      zone_name: zoneName,
      zone_type: meta.zoneType,
      biosecurity_level: riskLevel || meta.level,
      color: zoneColor || meta.color,
      opacity: zoneOpacity,
      description: zoneDescription,
      polygon_points: points,
      active: true,
    }
  }

  const saveDraft = async () => {
    if (draftPoints.length < 3) {
      setApiStatus('Cần tối thiểu 3 điểm để lưu vùng')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/zones`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(buildPayload(draftPoints)),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const created = {
        ...mapZoneFromApi(await response.json()),
        category: zoneCategory,
        riskLevel,
        description: zoneDescription,
        rules: zoneRules,
      }
      pushHistory()
      setZones((prev) => [created, ...prev])
      setSelectedZoneId(created.id)
      resetDraft()
      setMode('select')
      setApiStatus(`Đã lưu ${created.zone_name}`)
    } catch (error) {
      setApiStatus(`Không lưu được: ${error.message}`)
    }
  }

  const saveSelectedZone = async () => {
    if (!selectedZone) return
    const meta = categoryMeta(zoneCategory)

    try {
      const response = await fetch(`${API_BASE_URL}/api/zones/${selectedZone.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          zone_name: zoneName,
          zone_type: meta.zoneType,
          biosecurity_level: riskLevel || meta.level,
          color: zoneColor || meta.color,
          opacity: zoneOpacity,
          description: zoneDescription,
          polygon_points: selectedZone.polygon_points,
        }),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const updated = {
        ...mapZoneFromApi(await response.json()),
        category: zoneCategory,
        riskLevel,
        description: zoneDescription,
        rules: zoneRules,
      }
      setZones((prev) => prev.map((zone) => (zone.id === updated.id ? updated : zone)))
      setApiStatus(`Đã cập nhật ${updated.zone_name}`)
    } catch (error) {
      setApiStatus(`Không cập nhật được: ${error.message}`)
    }
  }

  const saveAll = async () => {
    if (selectedZone) await saveSelectedZone()
    else if (draftPoints.length >= 3) await saveDraft()
    else setApiStatus('Chọn vùng hoặc vẽ vùng trước khi lưu')
  }

  const deleteSelected = async () => {
    if (selectedZone) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/zones/${selectedZone.id}`, { method: 'DELETE' })
        if (!response.ok && response.status !== 404) throw new Error(`HTTP ${response.status}`)
        pushHistory()
        setZones((prev) => prev.filter((zone) => zone.id !== selectedZone.id))
        setSelectedZoneId(null)
        setSelectedVertexIndex(null)
        setApiStatus('Đã xóa vùng')
      } catch (error) {
        setApiStatus(`Không xóa được: ${error.message}`)
      }
      return
    }

    if (selectedFlowId) {
      pushHistory()
      setFlows((prev) => prev.filter((flow) => flow.id !== selectedFlowId))
      setSelectedFlowId(null)
      setApiStatus('Đã xóa đường')
    }
  }

  const duplicateSelectedZone = async () => {
    if (!selectedZone) {
      setApiStatus('Chọn vùng để nhân bản')
      return
    }

    const points = duplicatePoints(selectedZone.polygon_points)
    try {
      const response = await fetch(`${API_BASE_URL}/api/zones`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...buildPayload(points),
          zone_name: `${zoneName} (bản sao)`,
        }),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const created = {
        ...mapZoneFromApi(await response.json()),
        category: zoneCategory,
        riskLevel,
        description: zoneDescription,
        rules: zoneRules,
      }
      pushHistory()
      setZones((prev) => [created, ...prev])
      setSelectedZoneId(created.id)
      setApiStatus(`Đã nhân bản ${created.zone_name}`)
    } catch (error) {
      setApiStatus(`Không nhân bản được: ${error.message}`)
    }
  }

  const deleteSelectedVertex = () => {
    if (!selectedZone || selectedVertexIndex === null) return
    if (selectedZone.polygon_points.length <= 3) {
      setApiStatus('Đa giác cần tối thiểu 3 điểm')
      return
    }
    pushHistory()
    updateSelectedZonePoints(removePointAtIndex(selectedZone.polygon_points, selectedVertexIndex))
    setSelectedVertexIndex(null)
    setApiStatus('Đã xóa điểm điều khiển')
  }

  const undo = () => {
    if (!historyPast.length) return
    const previous = historyPast[historyPast.length - 1]
    setHistoryFuture((prev) => [makeSnapshot(), ...prev])
    setHistoryPast((prev) => prev.slice(0, -1))
    setZones(previous.zones)
    setFlows(previous.flows)
    setApiStatus('Đã hoàn tác')
  }

  const redo = () => {
    if (!historyFuture.length) return
    const next = historyFuture[0]
    setHistoryPast((prev) => [...prev, makeSnapshot()])
    setHistoryFuture((prev) => prev.slice(1))
    setZones(next.zones)
    setFlows(next.flows)
    setApiStatus('Đã làm lại')
  }

  const toggleRule = (listKey, ruleId) => {
    setZoneRules((prev) => {
      const list = prev[listKey]
      const nextList = list.includes(ruleId) ? list.filter((id) => id !== ruleId) : [...list, ruleId]
      const nextRules = { ...prev, [listKey]: nextList }
      if (selectedZone) {
        setZones((zoneList) => zoneList.map((zone) =>
          zone.id === selectedZone.id ? { ...zone, rules: nextRules } : zone,
        ))
      }
      return nextRules
    })
  }

  const exportPdf = () => window.print()

  const handleWheel = (event) => {
    event.preventDefault()
    setZoom((prev) => Math.max(0.5, Math.min(3, prev + (event.deltaY < 0 ? 0.08 : -0.08))))
  }

  const toggleFullscreen = () => {
    if (!viewportRef.current) return
    if (document.fullscreenElement) document.exitFullscreen()
    else viewportRef.current.requestFullscreen()
  }

  const refreshFrame = () => setFrameTick(Date.now())

  return (
    <div className="zone-designer-pro">
      <header className="zone-designer-pro__hero">
        <div>
          <span className="zone-designer-pro__eyebrow">Thiết kế vùng ATSH</span>
          <h1>Thiết kế vùng ATSH</h1>
          <p>Chỉnh sửa vùng an toàn sinh học trực tiếp trên hình ảnh camera thực tế.</p>
        </div>
        <div className="zone-designer-pro__hero-actions">
          <button type="button" className="btn btn--outline zone-btn-soft" onClick={saveSelectedZone} disabled={!selectedZone}>
            <Save size={16} /> Lưu
          </button>
          <button type="button" className="btn btn--outline zone-btn-soft" onClick={saveAll}>
            <Save size={16} /> Lưu tất cả
          </button>
          <button type="button" className="btn btn--primary zone-btn-soft" onClick={exportPdf}>
            <Download size={16} /> Xuất PDF
          </button>
        </div>
      </header>

      <div className="zone-designer-pro__layout">
        <aside className="zone-designer-pro__cameras panel">
          <div className="zone-panel-head">
            <h2>Danh sách camera</h2>
            <p>{filteredCameras.length} camera</p>
          </div>

          <div className="zone-camera-filters">
            <label className="zone-camera-search">
              <Search size={14} />
              <input
                type="search"
                placeholder="Tìm camera, khu vực..."
                value={cameraSearch}
                onChange={(e) => setCameraSearch(e.target.value)}
              />
            </label>
            <label>
              <span>Lọc theo trại</span>
              <select value={farmFilter} onChange={(e) => setFarmFilter(e.target.value)}>
                <option value="all">Tất cả trại</option>
                {FARMS.map((farm) => (
                  <option key={farm.id} value={farm.id}>{farm.name}</option>
                ))}
              </select>
            </label>
          </div>

          <div className="zone-camera-list">
            {filteredCameras.map((camera) => {
              const meta = cameras.find((item) => item.id === camera.id)
              const online = meta?.status === 'online'
              return (
                <button
                  type="button"
                  key={camera.id}
                  className={`zone-camera-item${selectedCameraId === camera.id ? ' zone-camera-item--active' : ''}`}
                  onClick={() => setSelectedCameraId(camera.id)}
                >
                  <span className={`zone-camera-item__dot zone-camera-item__dot--${online ? 'online' : 'offline'}`} />
                  <span>
                    <strong>{camera.name}</strong>
                    <small>{camera.zone}</small>
                    <small className="zone-camera-item__status">{online ? '● Đang hoạt động' : '● Ngắt kết nối'}</small>
                  </span>
                </button>
              )
            })}
          </div>
        </aside>

        <section className="zone-designer-pro__canvas panel">
          <div className="zone-canvas-toolbar">
            {[
              ['select', 'Chọn vùng', MousePointer2],
              ['pan', 'Kéo ảnh', Hand],
              ['polygon', 'Đa giác', Shapes],
              ['rect', 'Hình chữ nhật', Square],
              ['line', 'Đường', PenLine],
            ].map(([tool, label, Icon]) => (
              <button
                key={tool}
                type="button"
                className={`zone-tool-btn${mode === tool ? ' zone-tool-btn--active' : ''}`}
                onClick={() => setTool(tool)}
              >
                <Icon size={16} /> {label}
              </button>
            ))}
            <button type="button" className="zone-tool-btn" onClick={duplicateSelectedZone} disabled={!selectedZone}>
              <Copy size={16} /> Nhân bản
            </button>
            <button type="button" className="zone-tool-btn" onClick={deleteSelectedVertex} disabled={selectedVertexIndex === null}>
              <Plus size={16} style={{ transform: 'rotate(45deg)' }} /> Xóa điểm
            </button>
            <button type="button" className="zone-tool-btn" onClick={deleteSelected}>
              <Trash2 size={16} /> Xóa vùng
            </button>
            <button type="button" className="zone-tool-btn" onClick={undo} disabled={!historyPast.length}>
              <RotateCcw size={16} /> Hoàn tác
            </button>
            <button type="button" className="zone-tool-btn" onClick={redo} disabled={!historyFuture.length}>
              <Redo2 size={16} /> Làm lại
            </button>
            <button type="button" className="zone-tool-btn zone-tool-btn--save" onClick={saveAll}>
              <Save size={16} /> Lưu
            </button>
            <div className="zone-canvas-toolbar__zoom">
              <button type="button" className="zone-tool-btn" onClick={() => setZoom((z) => Math.max(0.5, z - 0.1))}>
                <ZoomOut size={16} />
              </button>
              <span>{Math.round(zoom * 100)}%</span>
              <button type="button" className="zone-tool-btn" onClick={() => setZoom((z) => Math.min(3, z + 0.1))}>
                <ZoomIn size={16} />
              </button>
              <button type="button" className="zone-tool-btn" onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }) }}>
                1:1
              </button>
              <button type="button" className="zone-tool-btn" onClick={refreshFrame}>
                Frame
              </button>
              <button type="button" className="zone-tool-btn" onClick={toggleFullscreen}>
                <Expand size={16} />
              </button>
            </div>
          </div>

          <div className="zone-canvas-meta">
            <span className={`zone-status-pill zone-status-pill--${cameraMeta.status}`}>
              {cameraMeta.status === 'online' ? '● Frame mới nhất' : '● Camera offline'}
            </span>
            <strong>{selectedCamera.name}</strong>
            <span>{selectedCamera.zone} · {cameraMeta.resolution}</span>
            <span className="zone-canvas-meta__status">{apiStatus}</span>
          </div>

          <div
            ref={viewportRef}
            className="zone-viewport"
            onWheel={handleWheel}
            onPointerDown={(event) => {
              if (mode === 'pan' || (mode === 'select' && event.target === viewportRef.current)) {
                setIsPanning(true)
                setPanStart({ x: event.clientX - pan.x, y: event.clientY - pan.y })
              }
            }}
            onPointerMove={(event) => {
              handleCanvasMove(event)
              if (isPanning) {
                setPan({ x: event.clientX - panStart.x, y: event.clientY - panStart.y })
              }
            }}
            onPointerUp={() => {
              setDragState(null)
              setIsPanning(false)
            }}
            onPointerLeave={() => {
              setDragState(null)
              setIsPanning(false)
            }}
          >
            <div
              className="zone-viewport__inner"
              style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})` }}
            >
              <div className="zone-canvas">
                <img
                  src={frameUrl}
                  alt={selectedCamera.name}
                  className="zone-canvas__image"
                  draggable={false}
                />
                <svg
                  ref={canvasRef}
                  className="zone-svg"
                  viewBox={`0 0 ${CANVAS_WIDTH} ${CANVAS_HEIGHT}`}
                  onClick={handleCanvasClick}
                >
                  {zones.map((zone) => {
                    const [labelX, labelY] = polygonCentroid(zone.polygon_points)
                    const opacity = zone.opacity ?? DEFAULT_ZONE_OPACITY
                    return (
                      <g key={zone.id} className="zone-shape">
                        <polygon
                          points={toPoints(zone.polygon_points)}
                          fill={zone.color}
                          fillOpacity={opacity}
                          stroke={zone.color}
                          strokeWidth={zone.id === selectedZoneId ? 4 : 2}
                          onClick={(event) => {
                            event.stopPropagation()
                            setSelectedZoneId(zone.id)
                            setSelectedFlowId(null)
                          }}
                          onPointerDown={(event) => {
                            if (mode !== 'select' || zone.id !== selectedZoneId) return
                            event.stopPropagation()
                            pushHistory()
                            setDragState({
                              type: 'zone',
                              start: readPoint(event),
                              basePoints: zone.polygon_points.map((point) => [...point]),
                            })
                          }}
                        />
                        <text
                          x={labelX}
                          y={labelY}
                          textAnchor="middle"
                          dominantBaseline="middle"
                          fill="#ffffff"
                          className="zone-svg__label"
                        >
                          {zone.zone_name}
                        </text>
                      </g>
                    )
                  })}

                  {flows.map((flow) => (
                    <g key={flow.id} className="zone-flow">
                      <polyline
                        points={toPoints(flow.points)}
                        fill="none"
                        stroke="var(--brand-orange)"
                        strokeWidth="4"
                        strokeLinecap="round"
                        onClick={(event) => {
                          event.stopPropagation()
                          setSelectedFlowId(flow.id)
                          setSelectedZoneId(null)
                        }}
                      />
                    </g>
                  ))}

                  {(draftPoints.length > 0 || rectPreview) && (
                    <g>
                      <polygon
                        points={toPoints(rectPreview || draftPoints)}
                        fill={zoneColor}
                        fillOpacity={zoneOpacity}
                        stroke={zoneColor}
                        strokeDasharray="8 6"
                        strokeWidth="3"
                      />
                      {(rectPreview ? [] : draftPoints).map(([x, y], index) => (
                        <circle key={`draft-${index}`} cx={x} cy={y} r="7" fill={zoneColor} />
                      ))}
                    </g>
                  )}

                  {draftLinePoints.length > 0 && (
                    <polyline
                      points={toPoints(draftLinePoints)}
                      fill="none"
                      stroke="var(--brand-orange)"
                      strokeDasharray="8 6"
                      strokeWidth="4"
                    />
                  )}

                  {mode === 'select' && selectedZone?.polygon_points.map(([x, y], index) => (
                    <circle
                      key={`${selectedZone.id}-v-${index}`}
                      cx={x}
                      cy={y}
                      r="10"
                      className={`zone-svg__handle${selectedVertexIndex === index ? ' zone-svg__handle--active' : ''}`}
                      onPointerDown={(event) => {
                        event.stopPropagation()
                        pushHistory()
                        setSelectedVertexIndex(index)
                        setDragState({ type: 'vertex', index })
                      }}
                    />
                  ))}

                  {mode === 'select' && selectedZone?.polygon_points.map((start, index) => {
                    const end = selectedZone.polygon_points[(index + 1) % selectedZone.polygon_points.length]
                    const [mx, my] = edgeMidpoint(start, end)
                    return (
                      <rect
                        key={`${selectedZone.id}-e-${index}`}
                        x={mx - 8}
                        y={my - 8}
                        width="16"
                        height="16"
                        rx="4"
                        className="zone-svg__edge-handle"
                        onPointerDown={(event) => {
                          event.stopPropagation()
                          pushHistory()
                          setDragState({
                            type: 'edge',
                            index,
                            last: readPoint(event),
                            basePoints: selectedZone.polygon_points.map((point) => [...point]),
                          })
                        }}
                      />
                    )
                  })}
                </svg>
              </div>
            </div>
          </div>

          {mode === 'line' && draftLinePoints.length >= 2 && (
            <div className="zone-inline-actions">
              <button type="button" className="btn btn--primary" onClick={finishLine}>
                Hoàn tất đường ({draftLinePoints.length} điểm)
              </button>
            </div>
          )}

          {(mode === 'polygon' || mode === 'rect') && draftPoints.length >= 3 && (
            <div className="zone-inline-actions">
              <button type="button" className="btn btn--primary" onClick={saveDraft}>
                Lưu vùng ({draftPoints.length} điểm)
              </button>
            </div>
          )}
        </section>

        <aside className="zone-designer-pro__info panel">
          <div className="zone-panel-head">
            <h2>Thuộc tính vùng</h2>
            <p>{selectedZone ? 'Chỉnh sửa vùng đã chọn' : 'Thuộc tính vùng mới'}</p>
          </div>

          <div className="zone-info-form">
            <label>
              <span>Tên vùng</span>
              <input value={zoneName} onChange={(e) => setZoneName(e.target.value)} />
            </label>
            <label>
              <span>Loại vùng</span>
              <select
                value={zoneCategory}
                onChange={(e) => {
                  const next = e.target.value
                  setZoneCategory(next)
                  setZoneColor(categoryMeta(next).color)
                  setZoneRules(defaultRulesForCategory(next))
                  setRiskLevel(categoryMeta(next).level)
                }}
              >
                {ZONE_CATEGORIES.map((item) => (
                  <option key={item.value} value={item.value}>{item.label}</option>
                ))}
              </select>
            </label>
            <label>
              <span>Mức rủi ro ATSH</span>
              <select value={riskLevel} onChange={(e) => setRiskLevel(e.target.value)}>
                {RISK_LEVELS.map((item) => (
                  <option key={item.value} value={item.value}>{item.label}</option>
                ))}
              </select>
            </label>
            <label>
              <span>Màu sắc</span>
              <div className="zone-color-row">
                <input type="color" value={zoneColor} onChange={(e) => setZoneColor(e.target.value)} />
                <input value={zoneColor} onChange={(e) => setZoneColor(e.target.value)} />
              </div>
            </label>
            <label>
              <span>Độ mờ vùng ({Math.round(zoneOpacity * 100)}%)</span>
              <input
                type="range"
                min="0.1"
                max="0.8"
                step="0.05"
                value={zoneOpacity}
                onChange={(e) => setZoneOpacity(Number(e.target.value))}
              />
            </label>
            <label>
              <span>Mô tả</span>
              <textarea
                rows={3}
                value={zoneDescription}
                onChange={(e) => setZoneDescription(e.target.value)}
                placeholder="Mô tả quy tắc và mục đích vùng..."
              />
            </label>
          </div>

          <div className="zone-rules-panel">
            <h3>Quy tắc ATSH · {selectedCategory.label}</h3>
            <div className="zone-rules-section">
              <strong>Được phép</strong>
              <div className="zone-rules-chips">
                {RULE_OPTIONS.allowed.map((rule) => (
                  <label key={rule.id} className="zone-rule-chip zone-rule-chip--allowed">
                    <input
                      type="checkbox"
                      checked={zoneRules.allowed.includes(rule.id)}
                      onChange={() => toggleRule('allowed', rule.id)}
                    />
                    <span>{rule.label}</span>
                  </label>
                ))}
              </div>
            </div>
            <div className="zone-rules-section">
              <strong>Bị cấm</strong>
              <div className="zone-rules-chips">
                {RULE_OPTIONS.blocked.map((rule) => (
                  <label key={rule.id} className="zone-rule-chip zone-rule-chip--blocked">
                    <input
                      type="checkbox"
                      checked={zoneRules.blocked.includes(rule.id)}
                      onChange={() => toggleRule('blocked', rule.id)}
                    />
                    <span>{rule.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div className="zone-type-legend">
            <h3>Loại vùng</h3>
            {ZONE_CATEGORIES.map((item) => (
              <div key={item.value} className="zone-type-legend__item">
                <span style={{ background: item.color, opacity: 0.7 }} />
                <div>
                  <strong>{item.label}</strong>
                  <small>{item.color} · 30%</small>
                </div>
              </div>
            ))}
          </div>
        </aside>
      </div>
    </div>
  )
}

export default ZoneDesignerPage
