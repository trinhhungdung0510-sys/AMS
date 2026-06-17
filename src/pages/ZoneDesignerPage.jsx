import { useEffect, useMemo, useState } from 'react'
import { Check, Edit3, MousePointer2, Pencil, RefreshCw, Save, Trash2 } from 'lucide-react'
import { cameras } from '../data/mockData'

const API_BASE_URL = 'http://127.0.0.1:8000'
const CANVAS_WIDTH = 1280
const CANVAS_HEIGHT = 720

const ATSH_LEVELS = [
  { value: 'red', label: 'Vùng cấm', color: '#dc2626' },
  { value: 'orange', label: 'Vùng hạn chế', color: '#f97316' },
  { value: 'yellow', label: 'Vùng kiểm soát', color: '#eab308' },
  { value: 'green', label: 'Vùng an toàn', color: '#16a34a' },
]

function mapZoneFromApi(item) {
  return {
    id: item.id,
    farm_id: item.trang_trai_id,
    camera_id: item.camera_id,
    zone_name: item.ten_vung,
    zone_type: item.ma_vung,
    zone_type_label: item.ten_loai_vung,
    biosecurity_level: item.cap_atsh,
    biosecurity_label: item.muc_atsh,
    color: item.mau_sac,
    polygon_points: item.diem_polygon,
    active: item.dang_hoat_dong,
    created_at: item.thoi_gian_tao,
  }
}

function toPoints(points) {
  return points.map(([x, y]) => `${x},${y}`).join(' ')
}

function getSvgPoint(event) {
  const rect = event.currentTarget.getBoundingClientRect()
  const x = ((event.clientX - rect.left) / rect.width) * CANVAS_WIDTH
  const y = ((event.clientY - rect.top) / rect.height) * CANVAS_HEIGHT
  return [
    Math.max(0, Math.min(CANVAS_WIDTH, Math.round(x))),
    Math.max(0, Math.min(CANVAS_HEIGHT, Math.round(y))),
  ]
}

function levelColor(level) {
  return ATSH_LEVELS.find((item) => item.value === level)?.color || '#eab308'
}

function ZoneDesignerPage() {
  const camera = cameras.find((item) => item.id === 'CAM-001') ?? cameras[0]
  const [zones, setZones] = useState([])
  const [zoneTypes, setZoneTypes] = useState([])
  const [selectedZoneId, setSelectedZoneId] = useState(null)
  const [draftPoints, setDraftPoints] = useState([])
  const [zoneName, setZoneName] = useState('Vùng ATSH mới')
  const [zoneType, setZoneType] = useState('farm_gate')
  const [biosecurityLevel, setBiosecurityLevel] = useState('orange')
  const [mode, setMode] = useState('select')
  const [dragPoint, setDragPoint] = useState(null)
  const [apiStatus, setApiStatus] = useState('Đang tải vùng từ backend...')

  const selectedZone = useMemo(
    () => zones.find((zone) => zone.id === selectedZoneId),
    [selectedZoneId, zones],
  )

  const loadCatalog = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/zones/types`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      setZoneTypes(data)
      if (data.length) {
        setZoneType(data[0].ma_vung)
        setBiosecurityLevel(data[0].cap_atsh_mac_dinh)
        setZoneName(data[0].ten_loai_vung)
      }
    } catch {
      setZoneTypes([])
    }
  }

  const loadZones = async () => {
    try {
      setApiStatus('Đang tải vùng từ backend...')
      const response = await fetch(`${API_BASE_URL}/api/zones`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      const cameraZones = data.filter((zone) => zone.camera_id === camera.id).map(mapZoneFromApi)
      setZones(cameraZones)
      setSelectedZoneId(cameraZones[0]?.id ?? null)
      setApiStatus(`Đã đồng bộ ${cameraZones.length} vùng ATSH`)
    } catch (error) {
      setZones([])
      setApiStatus(`Không tải được vùng: ${error.message}`)
    }
  }

  useEffect(() => {
    loadCatalog()
    loadZones()
  }, [])

  useEffect(() => {
    if (!selectedZone) return
    setZoneName(selectedZone.zone_name)
    setZoneType(selectedZone.zone_type)
    setBiosecurityLevel(selectedZone.biosecurity_level)
  }, [selectedZone])

  const handleZoneTypeChange = (value) => {
    setZoneType(value)
    const option = zoneTypes.find((item) => item.ma_vung === value)
    if (option) {
      setBiosecurityLevel(option.cap_atsh_mac_dinh)
      if (zoneName === '' || zoneName === 'Vùng ATSH mới') {
        setZoneName(option.ten_loai_vung)
      }
    }
  }

  const handleCanvasClick = (event) => {
    if (mode !== 'draw') return
    setDraftPoints((prev) => [...prev, getSvgPoint(event)])
  }

  const clearDraft = () => {
    setDraftPoints([])
    setMode('select')
  }

  const saveDraft = async () => {
    if (draftPoints.length < 3) {
      setApiStatus('Polygon cần tối thiểu 3 điểm')
      return
    }

    const payload = {
      farm_id: 'FARM-001',
      camera_id: camera.id,
      zone_name: zoneName,
      zone_type: zoneType,
      biosecurity_level: biosecurityLevel,
      color: levelColor(biosecurityLevel),
      polygon_points: draftPoints,
      active: true,
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/zones`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const created = mapZoneFromApi(await response.json())
      setZones((prev) => [created, ...prev])
      setSelectedZoneId(created.id)
      setDraftPoints([])
      setMode('select')
      setApiStatus(`Đã tạo vùng ${created.zone_name}`)
    } catch (error) {
      setApiStatus(`Không lưu được vùng: ${error.message}`)
    }
  }

  const saveSelectedZone = async () => {
    if (!selectedZone) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/zones/${selectedZone.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          zone_name: zoneName,
          zone_type: zoneType,
          biosecurity_level: biosecurityLevel,
          color: levelColor(biosecurityLevel),
        }),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const updated = mapZoneFromApi(await response.json())
      setZones((prev) => prev.map((zone) => (zone.id === updated.id ? updated : zone)))
      setApiStatus(`Đã cập nhật vùng ${updated.zone_name}`)
    } catch (error) {
      setApiStatus(`Không cập nhật được vùng: ${error.message}`)
    }
  }

  const deleteZone = async (zoneId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/zones/${zoneId}`, { method: 'DELETE' })
      if (!response.ok && response.status !== 404) throw new Error(`HTTP ${response.status}`)
      setZones((prev) => prev.filter((zone) => zone.id !== zoneId))
      if (selectedZoneId === zoneId) setSelectedZoneId(null)
      setApiStatus('Đã xóa vùng')
    } catch (error) {
      setApiStatus(`Không xóa được vùng: ${error.message}`)
    }
  }

  const updateSelectedPoint = async (pointIndex, point) => {
    if (!selectedZone) return

    const nextPoints = selectedZone.polygon_points.map((item, index) =>
      index === pointIndex ? point : item,
    )
    const nextZone = { ...selectedZone, polygon_points: nextPoints }
    setZones((prev) => prev.map((zone) => (zone.id === selectedZone.id ? nextZone : zone)))

    try {
      const response = await fetch(`${API_BASE_URL}/api/zones/${selectedZone.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ polygon_points: nextPoints }),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      setApiStatus(`Đã chỉnh sửa polygon ${selectedZone.zone_name}`)
    } catch (error) {
      setApiStatus(`Không cập nhật được polygon: ${error.message}`)
    }
  }

  const handlePointerMove = (event) => {
    if (!dragPoint) return
    updateSelectedPoint(dragPoint.index, getSvgPoint(event))
  }

  return (
    <div className="zone-designer">
      <section className="panel zone-designer__workspace">
        <div className="panel__header">
          <div>
            <h2><Pencil size={18} /> Thiết kế vùng ATSH trên camera</h2>
            <p>{camera.name} · {camera.zone} · Vẽ / Sửa / Xóa polygon</p>
          </div>
          <div className="zone-toolbar">
            <button type="button" className="btn btn--outline" onClick={loadZones}>
              <RefreshCw size={16} /> Đồng bộ
            </button>
            <button
              type="button"
              className={`btn ${mode === 'draw' ? 'btn--primary' : 'btn--outline'}`}
              onClick={() => {
                setMode('draw')
                setDraftPoints([])
              }}
            >
              <Pencil size={16} /> Vẽ polygon
            </button>
            <button
              type="button"
              className={`btn ${mode === 'edit' ? 'btn--primary' : 'btn--outline'}`}
              disabled={!selectedZone}
              onClick={() => setMode('edit')}
            >
              <Edit3 size={16} /> Sửa polygon
            </button>
          </div>
        </div>

        <div className="zone-canvas-card">
          <div className="zone-camera-meta">
            <span className="live-pill"><span className="live-pill__dot" /> TRỰC TIẾP</span>
            <strong>{camera.id}</strong>
            <span>{camera.resolution} · {camera.fps} FPS · {apiStatus}</span>
          </div>

          <div className="zone-canvas">
            <div className="zone-snapshot">
              <div className="zone-snapshot__gate">Cổng trại</div>
              <div className="zone-snapshot__road" />
              <div className="zone-snapshot__checkpoint">Chốt kiểm soát</div>
              <div className="zone-snapshot__barn">Khu chuồng</div>
            </div>
            <svg
              className="zone-svg"
              viewBox={`0 0 ${CANVAS_WIDTH} ${CANVAS_HEIGHT}`}
              onClick={handleCanvasClick}
              onPointerMove={handlePointerMove}
              onPointerUp={() => setDragPoint(null)}
              onPointerLeave={() => setDragPoint(null)}
            >
              {zones.map((zone) => (
                <g key={zone.id} className="zone-shape">
                  <polygon
                    points={toPoints(zone.polygon_points)}
                    fill={zone.color}
                    fillOpacity={zone.id === selectedZoneId ? 0.28 : 0.18}
                    stroke={zone.color}
                    strokeWidth={zone.id === selectedZoneId ? 5 : 3}
                    onClick={(event) => {
                      event.stopPropagation()
                      setSelectedZoneId(zone.id)
                    }}
                  />
                  <text
                    x={zone.polygon_points[0][0]}
                    y={Math.max(24, zone.polygon_points[0][1] - 12)}
                    fill="#ffffff"
                    className="zone-svg__label"
                  >
                    {zone.zone_name}
                  </text>
                </g>
              ))}

              {draftPoints.length > 0 && (
                <g>
                  <polyline
                    points={toPoints(draftPoints)}
                    fill="none"
                    stroke={levelColor(biosecurityLevel)}
                    strokeDasharray="10 8"
                    strokeWidth="4"
                  />
                  {draftPoints.map(([x, y], index) => (
                    <circle key={`${x}-${y}-${index}`} cx={x} cy={y} r="8" fill={levelColor(biosecurityLevel)} />
                  ))}
                </g>
              )}

              {mode === 'edit' && selectedZone?.polygon_points.map(([x, y], index) => (
                <circle
                  key={`${selectedZone.id}-${index}`}
                  cx={x}
                  cy={y}
                  r="13"
                  className="zone-svg__handle"
                  onPointerDown={(event) => {
                    event.stopPropagation()
                    setDragPoint({ index })
                  }}
                />
              ))}
            </svg>
          </div>
        </div>

        <div className="zone-editor-bar">
          <label>
            <span>Tên vùng</span>
            <input value={zoneName} onChange={(event) => setZoneName(event.target.value)} />
          </label>
          <label>
            <span>Loại vùng</span>
            <select value={zoneType} onChange={(event) => handleZoneTypeChange(event.target.value)}>
              {zoneTypes.map((option) => (
                <option key={option.ma_vung} value={option.ma_vung}>{option.ten_loai_vung}</option>
              ))}
            </select>
          </label>
          <label>
            <span>Mức ATSH</span>
            <select value={biosecurityLevel} onChange={(event) => setBiosecurityLevel(event.target.value)}>
              {ATSH_LEVELS.map((level) => (
                <option key={level.value} value={level.value}>{level.label}</option>
              ))}
            </select>
          </label>
          <div className="zone-editor-bar__actions">
            <button type="button" className="btn btn--outline" onClick={clearDraft}>
              <MousePointer2 size={16} /> Chọn
            </button>
            {mode === 'draw' ? (
              <button type="button" className="btn btn--primary" onClick={saveDraft}>
                <Check size={16} /> Lưu polygon ({draftPoints.length})
              </button>
            ) : (
              <button type="button" className="btn btn--primary" disabled={!selectedZone} onClick={saveSelectedZone}>
                <Save size={16} /> Lưu thông tin vùng
              </button>
            )}
          </div>
        </div>
      </section>

      <aside className="panel zone-list-panel">
        <div className="panel__header">
          <div>
            <h2>Danh sách vùng</h2>
            <p>{zones.length} polygon trên camera {camera.id}</p>
          </div>
        </div>
        <div className="zone-list">
          {zones.map((zone) => (
            <button
              type="button"
              key={zone.id}
              className={`zone-list__item${selectedZoneId === zone.id ? ' zone-list__item--active' : ''}`}
              onClick={() => setSelectedZoneId(zone.id)}
            >
              <span className="zone-list__color" style={{ background: zone.color }} />
              <span>
                <strong>{zone.zone_name}</strong>
                <small>{zone.zone_type_label} · {zone.biosecurity_label} · {zone.polygon_points.length} điểm</small>
              </span>
              <Trash2
                size={17}
                className="zone-list__delete"
                onClick={(event) => {
                  event.stopPropagation()
                  deleteZone(zone.id)
                }}
              />
            </button>
          ))}
        </div>

        <div className="zone-legend">
          <h3>Phân cấp ATSH</h3>
          {ATSH_LEVELS.map((level) => (
            <div key={level.value} className="zone-legend__item">
              <span style={{ background: level.color }} />
              {level.label}
            </div>
          ))}
        </div>
      </aside>
    </div>
  )
}

export default ZoneDesignerPage
