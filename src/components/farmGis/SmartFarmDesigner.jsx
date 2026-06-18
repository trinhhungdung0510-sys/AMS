import { lazy, Suspense, useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  BarChart3,
  Copy,
  FileText,
  Flame,
  Image,
  MapPin,
  Move,
  PenLine,
  Plus,
  Redo2,
  RotateCw,
  Ruler,
  Save,
  Search,
  ShieldCheck,
  Trash2,
  Undo2,
} from 'lucide-react'
import 'leaflet/dist/leaflet.css'
import {
  ATSH_ZONE_TYPES,
  DEFAULT_LAYERS,
  FLOW_TYPES,
  FARM_OBJECT_TYPES,
  HEATMAP_COLORS,
  computeStats,
  createHistory,
  createObjectFromType,
  duplicateObject,
  evaluateAtsh,
  exportDesignerPng,
  geocodeAddress,
  historyCommit,
  historyRedo,
  historyUndo,
  loadDesignerState,
  objectDimensionsMeters,
  polylineLengthMeters,
  saveDesignerState,
  saveDesignerTemplate,
} from '../../data/smartFarmDesigner'
import { LINKABLE_ZONE_TYPES, TILE_LAYERS } from '../../data/farmGisMap'
import { cameras } from '../../data/mockData'
import {
  fetchSmartFarmDesigner,
  fromApiResponse,
  saveSmartFarmDesigner,
  toApiPayload,
} from '../../services/smartFarmApi'

const FarmGisMap = lazy(() => import('./FarmGisMap'))

const EDIT_TOOLS = [
  { id: 'move', label: 'Di chuyển', icon: Move },
  { id: 'resize', label: 'Đổi kích thước', icon: Ruler },
  { id: 'rotate', label: 'Xoay', icon: RotateCw },
  { id: 'route', label: 'Luồng di chuyển', icon: PenLine },
  { id: 'ruler', label: 'Thước đo', icon: Ruler },
]

function SmartFarmDesigner({ embedded = false }) {
  const [history, setHistory] = useState(() => createHistory(loadDesignerState()))
  const [tool, setTool] = useState('move')
  const [pendingAddType, setPendingAddType] = useState(null)
  const [selectedId, setSelectedId] = useState(null)
  const [routeType, setRouteType] = useState('worker')
  const [draftRoute, setDraftRoute] = useState([])
  const [rulerPoints, setRulerPoints] = useState([])
  const [address, setAddress] = useState('')
  const [gpsLat, setGpsLat] = useState('')
  const [gpsLng, setGpsLng] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [flyToTarget, setFlyToTarget] = useState(null)
  const [atshReport, setAtshReport] = useState(null)
  const [status, setStatus] = useState('AMS Smart Farm Designer · Sẵn sàng')
  const [loading, setLoading] = useState(true)

  const { layout, objects, routes, layers } = history.present
  const layerState = { ...DEFAULT_LAYERS, ...layers }

  const selected = useMemo(
    () => objects.find((item) => item.id === selectedId) || null,
    [objects, selectedId],
  )

  const stats = useMemo(() => computeStats(objects, routes), [objects, routes])
  const linkableZones = useMemo(
    () => objects.filter((item) => LINKABLE_ZONE_TYPES.includes(item.objectType)),
    [objects],
  )

  const rulerDistance = useMemo(
    () => (rulerPoints.length >= 2 ? Math.round(polylineLengthMeters(rulerPoints)) : 0),
    [rulerPoints],
  )

  const selectedDims = useMemo(
    () => (selected && selected.objectType !== 'camera' ? objectDimensionsMeters(selected) : null),
    [selected],
  )

  const commit = useCallback((nextPresent, message) => {
    setHistory((prev) => historyCommit(prev, nextPresent))
    if (message) setStatus(message)
  }, [])

  const updateObject = useCallback((id, patch) => {
    setHistory((prev) => historyCommit(prev, {
      ...prev.present,
      objects: prev.present.objects.map((item) => (item.id === id ? { ...item, ...patch } : item)),
    }))
  }, [])

  const setLayers = useCallback((patch) => {
    setHistory((prev) => historyCommit(prev, {
      ...prev.present,
      layers: { ...prev.present.layers, ...patch },
    }))
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => saveDesignerState(history.present), 400)
    return () => clearTimeout(timer)
  }, [history.present])

  useEffect(() => {
    let active = true
    fetchSmartFarmDesigner()
      .then((data) => {
        if (!active) return
        const parsed = fromApiResponse(data)
        if (parsed) {
          setHistory(createHistory(parsed))
          setAddress(parsed.layout.address || '')
          setStatus('Đã tải sơ đồ từ database')
        }
      })
      .catch(() => {
        if (active) setStatus('Dùng sơ đồ cục bộ')
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => { active = false }
  }, [])

  const navigateTo = (lat, lng, message) => {
    commit({
      ...history.present,
      layout: { ...layout, centerLat: lat, centerLng: lng },
    }, message)
    setFlyToTarget({ lat, lng, zoom: layout.zoom, tick: Date.now() })
  }

  const handleAddressSearch = async () => {
    if (!address.trim()) return
    const result = await geocodeAddress(address)
    if (!result) {
      setStatus('Không tìm thấy địa chỉ')
      return
    }
    navigateTo(result.lat, result.lng, `Đã định vị: ${result.label}`)
  }

  const handleGpsGo = () => {
    const lat = Number(gpsLat)
    const lng = Number(gpsLng)
    if (Number.isNaN(lat) || Number.isNaN(lng)) {
      setStatus('Tọa độ GPS không hợp lệ')
      return
    }
    navigateTo(lat, lng, `Đã nhảy tới ${lat.toFixed(5)}, ${lng.toFixed(5)}`)
  }

  const handleMapSearch = async () => {
    if (!searchQuery.trim()) return
    const result = await geocodeAddress(searchQuery)
    if (!result) {
      setStatus('Không tìm thấy vị trí trên bản đồ')
      return
    }
    navigateTo(result.lat, result.lng, `Tìm thấy: ${result.label}`)
  }

  const handleDropType = (objectType, lat, lng) => {
    const created = createObjectFromType(objectType, lat, lng)
    commit({ ...history.present, objects: [...objects, created] }, `Đã thêm ${created.name}`)
    setSelectedId(created.id)
    setPendingAddType(null)
    setTool('move')
  }

  const handleMapClickExtra = (lat, lng) => {
    if (tool === 'route') {
      setDraftRoute((prev) => [...prev, [lat, lng]])
      return
    }
    if (tool === 'ruler') {
      setRulerPoints((prev) => [...prev, [lat, lng]])
    }
  }

  const finishRoute = () => {
    if (draftRoute.length < 2) return
    const meta = FLOW_TYPES.find((item) => item.type === routeType) || FLOW_TYPES[0]
    const route = {
      id: `route-${Date.now()}`,
      routeType,
      name: meta.label,
      points: draftRoute,
      labels: draftRoute.map((_, index) => `Điểm ${index + 1}`),
      valid: true,
    }
    commit({ ...history.present, routes: [...routes, route] }, `Đã vẽ ${meta.label}`)
    setDraftRoute([])
    setTool('move')
  }

  const handleSave = async () => {
    const state = { ...history.present, layout: { ...layout, address } }
    saveDesignerState(state)
    try {
      await saveSmartFarmDesigner(toApiPayload(state))
      setStatus('Đã lưu sơ đồ vào database')
    } catch {
      setStatus('Đã lưu sơ đồ cục bộ')
    }
  }

  const handleSaveTemplate = async () => {
    const state = {
      ...history.present,
      layout: { ...layout, address, isTemplate: true, name: `${layout.name} (Mẫu)` },
    }
    saveDesignerTemplate(state)
    try {
      await saveSmartFarmDesigner(toApiPayload(state))
      setStatus('Đã lưu mẫu sơ đồ')
    } catch {
      setStatus('Đã lưu mẫu cục bộ')
    }
  }

  const handleEvaluateAtsh = () => {
    const report = evaluateAtsh(objects, routes)
    setAtshReport(report)
    setStatus(`Đánh giá ATSH: ${report.score}/100`)
  }

  const handleDuplicate = () => {
    if (!selected) return
    const copy = duplicateObject(selected)
    commit({ ...history.present, objects: [...objects, copy] }, `Đã nhân bản ${selected.name}`)
    setSelectedId(copy.id)
  }

  const handleDelete = () => {
    if (!selected) return
    if (!window.confirm(`Xóa "${selected.name}" khỏi sơ đồ?`)) return
    commit({
      ...history.present,
      objects: objects.filter((item) => item.id !== selected.id),
      routes: routes.filter((route) => !route.points.every((point) => point[0] === selected.x)),
    }, `Đã xóa ${selected.name}`)
    setSelectedId(null)
  }

  const paletteItems = FARM_OBJECT_TYPES.filter((item) => item.type !== 'camera')

  return (
    <div className={`smart-farm-designer${embedded ? ' smart-farm-designer--embedded' : ''}`}>
      {!embedded && (
        <header className="smart-farm-designer__hero">
          <div>
            <h1>Bản đồ & Thiết kế trang trại</h1>
            <p>Xem và tự thiết kế sơ đồ trại trên nền vệ tinh — kéo thả, ATSH, luồng di chuyển, bản đồ nhiệt.</p>
          </div>
          <div className="smart-farm-designer__actions">
            <button type="button" className="btn btn--outline" onClick={handleSave}><Save size={15} /> Lưu sơ đồ</button>
            <button type="button" className="btn btn--outline" onClick={handleSaveTemplate}><Copy size={15} /> Lưu mẫu</button>
            <button type="button" className="btn btn--outline" onClick={() => window.print()}><FileText size={15} /> PDF</button>
            <button type="button" className="btn btn--primary" onClick={() => exportDesignerPng(objects, routes)}><Image size={15} /> PNG</button>
          </div>
        </header>
      )}

      {embedded && (
        <div className="smart-farm-designer__actions smart-farm-designer__actions--embedded">
          <button type="button" className="btn btn--outline" onClick={handleSave}><Save size={15} /> Lưu sơ đồ</button>
          <button type="button" className="btn btn--outline" onClick={handleSaveTemplate}><Copy size={15} /> Lưu mẫu</button>
          <button type="button" className="btn btn--outline" onClick={() => window.print()}><FileText size={15} /> PDF</button>
          <button type="button" className="btn btn--primary" onClick={() => exportDesignerPng(objects, routes)}><Image size={15} /> PNG</button>
          <span className="farm-editor-status">{status}</span>
        </div>
      )}

      <section className="smart-farm-designer__location panel">
        <label>
          <span>Địa chỉ</span>
          <div className="smart-farm-designer__search-row">
            <input value={address} onChange={(e) => setAddress(e.target.value)} placeholder="Ấp, xã, huyện, tỉnh..." />
            <button type="button" className="btn btn--outline" onClick={handleAddressSearch}><Search size={15} /> Tìm</button>
          </div>
        </label>
        <label>
          <span>Tọa độ GPS</span>
          <div className="smart-farm-designer__gps-row">
            <input value={gpsLat} onChange={(e) => setGpsLat(e.target.value)} placeholder="Vĩ độ (lat)" />
            <input value={gpsLng} onChange={(e) => setGpsLng(e.target.value)} placeholder="Kinh độ (lng)" />
            <button type="button" className="btn btn--outline" onClick={handleGpsGo}><MapPin size={15} /> Đi tới</button>
          </div>
        </label>
        <label>
          <span>Tìm kiếm trên bản đồ</span>
          <div className="smart-farm-designer__search-row">
            <input value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} placeholder="Tìm địa điểm, trại, khu vực..." />
            <button type="button" className="btn btn--primary" onClick={handleMapSearch}><Search size={15} /> Tìm</button>
          </div>
        </label>
      </section>

      <div className="smart-farm-designer__layers">
        {Object.values(TILE_LAYERS).map((layer) => (
          <button
            key={layer.id}
            type="button"
            className={`farm-gis-toolbar__btn${layout.baseLayer === layer.id ? ' farm-gis-toolbar__btn--active' : ''}`}
            onClick={() => commit({ ...history.present, layout: { ...layout, baseLayer: layer.id } })}
          >
            {layer.label}
          </button>
        ))}
        <span className="farm-gis-toolbar__sep" />
        {[
          ['objects', 'Đối tượng'],
          ['cameras', 'Camera'],
          ['atsh', 'ATSH'],
          ['routes', 'Luồng'],
          ['heatmap', 'Bản đồ nhiệt'],
        ].map(([key, label]) => (
          <button
            key={key}
            type="button"
            className={`farm-gis-toolbar__btn${layerState[key] ? ' farm-gis-toolbar__btn--active' : ''}`}
            onClick={() => setLayers({ [key]: !layerState[key] })}
          >
            {label}
          </button>
        ))}
        <span className="farm-editor-status">{status}</span>
      </div>

      <div className="smart-farm-designer__layout">
        <aside className="smart-farm-designer__palette panel">
          <h2>Lớp đối tượng · Kéo thả</h2>
          <div className="farm-editor-palette__grid">
            {paletteItems.map((item) => (
              <div
                key={item.type}
                draggable
                role="button"
                tabIndex={0}
                className={`farm-editor-palette__item${pendingAddType === item.type ? ' farm-editor-palette__item--active' : ''}`}
                onDragStart={(e) => e.dataTransfer.setData('farm-object-type', item.type)}
                onClick={() => { setPendingAddType(item.type); setTool('move'); setStatus(`Chọn vị trí: ${item.label}`) }}
              >
                <span>{item.icon}</span>
                {item.label}
              </div>
            ))}
            <div
              draggable
              role="button"
              tabIndex={0}
              className="farm-editor-palette__item"
              onDragStart={(e) => e.dataTransfer.setData('farm-object-type', 'camera')}
              onClick={() => { setPendingAddType('camera'); setStatus('Chọn vị trí ghim camera') }}
            >
              <span>📷</span>
              Camera
            </div>
          </div>

          <h2>Công cụ chỉnh sửa</h2>
          <div className="smart-farm-designer__tools">
            {EDIT_TOOLS.map((item) => {
              const Icon = item.icon
              return (
                <button key={item.id} type="button" className={`farm-editor-tool${tool === item.id ? ' farm-editor-tool--active' : ''}`} onClick={() => { setTool(item.id); setDraftRoute([]); setRulerPoints([]) }}>
                  <Icon size={15} /> {item.label}
                </button>
              )
            })}
          </div>

          {tool === 'route' && (
            <div className="smart-farm-designer__route-tools">
              <h3>Luồng di chuyển</h3>
              {FLOW_TYPES.map((item) => (
                <button key={item.type} type="button" className={`farm-map-flow-btn${routeType === item.type ? ' farm-map-flow-btn--active' : ''}`} onClick={() => { setRouteType(item.type); setDraftRoute([]) }}>
                  <span style={{ background: item.color }} /> {item.label}
                </button>
              ))}
              {draftRoute.length >= 2 && (
                <button type="button" className="btn btn--primary" onClick={finishRoute}>Hoàn tất luồng ({draftRoute.length} điểm)</button>
              )}
            </div>
          )}

          {tool === 'ruler' && (
            <div className="smart-farm-designer__measure panel-nested">
              <strong>Thước đo</strong>
              <p>Khoảng cách: <b>{rulerDistance} m</b></p>
              <button type="button" className="btn btn--outline" onClick={() => setRulerPoints([])}>Xóa thước</button>
            </div>
          )}

          <div className="farm-editor-zone-actions">
            <button type="button" className="btn btn--primary" onClick={() => { const c = createObjectFromType('gestation', layout.centerLat, layout.centerLng); commit({ ...history.present, objects: [...objects, c] }, 'Đã thêm khu vực'); setSelectedId(c.id) }}><Plus size={15} /> Thêm khu vực</button>
            <button type="button" className="btn btn--outline" onClick={handleDuplicate} disabled={!selected}><Copy size={15} /> Nhân bản</button>
            <button type="button" className="btn btn--outline btn--danger" onClick={handleDelete} disabled={!selected}><Trash2 size={15} /> Xóa</button>
            <button type="button" className="btn btn--outline" onClick={() => setHistory((prev) => historyUndo(prev))} disabled={!history.past.length}><Undo2 size={15} /> Hoàn tác</button>
            <button type="button" className="btn btn--outline" onClick={() => setHistory((prev) => historyRedo(prev))} disabled={!history.future.length}><Redo2 size={15} /> Làm lại</button>
          </div>
        </aside>

        <div className="farm-gis-map panel">
          {loading ? (
            <div className="farm-gis-map__loading">Đang tải Smart Farm Designer…</div>
          ) : (
            <Suspense fallback={<div className="farm-gis-map__loading">Đang tải bản đồ…</div>}>
              <FarmGisMap
                layout={layout}
                objects={objects}
                routes={routes}
                draftRoute={draftRoute}
                rulerPoints={rulerPoints}
                selectedId={selectedId}
                tool={tool}
                pendingAddType={pendingAddType}
                drawingRoute={tool === 'route'}
                drawingRuler={tool === 'ruler'}
                showAtsh={layerState.atsh}
                showCameras={layerState.cameras}
                showRoutes={layerState.routes}
                showHeatmap={layerState.heatmap}
                flyToTarget={flyToTarget}
                onSelect={setSelectedId}
                onUpdate={updateObject}
                onDropType={handleDropType}
                onAddAt={handleDropType}
                onMapClickExtra={handleMapClickExtra}
              />
            </Suspense>
          )}
        </div>

        <aside className="smart-farm-designer__inspector panel">
          <section className="smart-farm-designer__stats">
            <h2><BarChart3 size={16} /> Thống kê</h2>
            <ul>
              <li><span>Tổng chuồng</span><strong>{stats.totalBarns}</strong></li>
              <li><span>Tổng camera</span><strong>{stats.totalCameras}</strong></li>
              <li><span>Tổng vùng ATSH</span><strong>{stats.totalAtshZones}</strong></li>
              <li><span>Tổng luồng di chuyển</span><strong>{stats.totalRoutes}</strong></li>
            </ul>
          </section>

          {selected && (
            <section className="smart-farm-designer__props">
              <h2>Thuộc tính</h2>
              <div className="farm-gis-form">
                <label><span>Tên khu vực</span><input value={selected.name} onChange={(e) => updateObject(selected.id, { name: e.target.value })} /></label>
                <label>
                  <span>Loại khu vực</span>
                  <select value={selected.objectType} onChange={(e) => {
                    const meta = FARM_OBJECT_TYPES.find((item) => item.type === e.target.value)
                    updateObject(selected.id, { objectType: e.target.value, atshZoneType: meta?.atshZoneType || selected.atshZoneType })
                  }}>
                    {FARM_OBJECT_TYPES.map((item) => <option key={item.type} value={item.type}>{item.label}</option>)}
                  </select>
                </label>
                <label><span>Mô tả</span><textarea rows={2} value={selected.description || ''} onChange={(e) => updateObject(selected.id, { description: e.target.value })} /></label>
                <label>
                  <span>Vùng ATSH</span>
                  <select value={selected.atshZoneType} onChange={(e) => updateObject(selected.id, { atshZoneType: e.target.value })}>
                    {Object.entries(ATSH_ZONE_TYPES).map(([key, item]) => <option key={key} value={key}>{item.label}</option>)}
                  </select>
                </label>
                <label>
                  <span>Mức ATSH (bản đồ nhiệt)</span>
                  <select value={selected.atshLevel} onChange={(e) => updateObject(selected.id, { atshLevel: e.target.value })}>
                    {Object.entries(HEATMAP_COLORS).map(([key, item]) => <option key={key} value={key}>{item.label}</option>)}
                  </select>
                </label>
                {selectedDims && (
                  <div className="smart-farm-designer__measure panel-nested">
                    <strong>Thước đo (mét)</strong>
                    <p>Chiều dài: <b>{selectedDims.lengthM} m</b></p>
                    <p>Chiều rộng: <b>{selectedDims.widthM} m</b></p>
                    <p>Diện tích: <b>{selectedDims.areaM2} m²</b></p>
                  </div>
                )}
                {selected.objectType === 'camera' && (
                  <>
                    <label>
                      <span>Camera liên kết</span>
                      <select value={selected.linkedCameraId || ''} onChange={(e) => updateObject(selected.id, { linkedCameraId: e.target.value })}>
                        <option value="">— Chọn —</option>
                        {cameras.map((cam) => <option key={cam.id} value={cam.id}>{cam.name}</option>)}
                      </select>
                    </label>
                    <label>
                      <span>Liên kết khu vực</span>
                      <select value={selected.linkedZoneId || ''} onChange={(e) => updateObject(selected.id, { linkedZoneId: e.target.value })}>
                        <option value="">— Không —</option>
                        {linkableZones.map((zone) => <option key={zone.id} value={zone.id}>{zone.name}</option>)}
                      </select>
                    </label>
                    <label><span>Hướng camera (°)</span><input type="number" value={selected.cameraDirection ?? 90} onChange={(e) => updateObject(selected.id, { cameraDirection: Number(e.target.value) })} /></label>
                    <label><span>Góc quan sát (°)</span><input type="number" value={selected.cameraFov ?? 60} onChange={(e) => updateObject(selected.id, { cameraFov: Number(e.target.value) })} /></label>
                    {selected.linkedCameraId && <Link to={`/monitoring/${selected.linkedCameraId}`} className="btn btn--outline">Xem live</Link>}
                  </>
                )}
              </div>
            </section>
          )}

          <section className="smart-farm-designer__atsh panel-nested">
            <h2><ShieldCheck size={16} /> Kiểm tra ATSH</h2>
            <button type="button" className="btn btn--primary" onClick={handleEvaluateAtsh}><Flame size={15} /> Đánh giá ATSH</button>
            {atshReport && (
              <div className="smart-farm-designer__atsh-report">
                <div className="smart-farm-designer__score">
                  <span>Điểm ATSH</span>
                  <strong className={atshReport.score >= 80 ? 'score--green' : atshReport.score >= 60 ? 'score--yellow' : 'score--red'}>{atshReport.score}</strong>
                </div>
                <div className="smart-farm-designer__score">
                  <span>Điểm rủi ro</span>
                  <strong>{atshReport.riskScore}</strong>
                </div>
                <h3>Danh sách nguy cơ</h3>
                <ul>{atshReport.risks.map((item) => <li key={item}>{item}</li>)}</ul>
                <h3>Khuyến nghị</h3>
                <ul>{atshReport.recommendations.map((item) => <li key={item}>{item}</li>)}</ul>
              </div>
            )}
          </section>

          <section className="smart-farm-designer__heatmap-legend">
            <h3>Bản đồ nhiệt ATSH</h3>
            {Object.values(HEATMAP_COLORS).map((item) => (
              <span key={item.label}><i style={{ background: item.color }} /> {item.label}</span>
            ))}
          </section>
        </aside>
      </div>
    </div>
  )
}

export default SmartFarmDesigner
