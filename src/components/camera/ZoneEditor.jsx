import { useCallback, useEffect, useRef, useState } from 'react'
import { pointsToSvgString, screenToNormalized } from '../../utils/zoneCoordinates'
import {
  ZONE_TYPE_OPTIONS,
  createCameraZone,
  deleteCameraZone,
  getCameraZones,
  updateCameraZone,
} from '../../services/cameraZoneService'

const DEFAULT_COLOR = '#ff0000'

function ZoneEditor({ cameraId, snapshotUrl }) {
  const containerRef = useRef(null)
  const [zones, setZones] = useState([])
  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 })
  const [isDrawing, setIsDrawing] = useState(false)
  const [draftPoints, setDraftPoints] = useState([])
  const [selectedZoneId, setSelectedZoneId] = useState(null)
  const [zoneName, setZoneName] = useState('Vùng mới')
  const [zoneType, setZoneType] = useState('restricted')
  const [zoneColor, setZoneColor] = useState(DEFAULT_COLOR)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const selectedZone = zones.find((zone) => zone.id === selectedZoneId) ?? null

  const updateCanvasSize = useCallback(() => {
    const node = containerRef.current
    if (!node) return
    const rect = node.getBoundingClientRect()
    setCanvasSize({ width: rect.width, height: rect.height })
  }, [])

  const loadZones = useCallback(async () => {
    if (!cameraId) return

    setLoading(true)
    setError('')

    try {
      const data = await getCameraZones(cameraId)
      setZones(data)
    } catch (loadError) {
      setError(loadError.message)
    } finally {
      setLoading(false)
    }
  }, [cameraId])

  useEffect(() => {
    loadZones()
  }, [loadZones])

  useEffect(() => {
    updateCanvasSize()
    window.addEventListener('resize', updateCanvasSize)
    return () => window.removeEventListener('resize', updateCanvasSize)
  }, [updateCanvasSize, snapshotUrl])

  useEffect(() => {
    if (!selectedZone) return
    setZoneName(selectedZone.name)
    setZoneType(selectedZone.type)
    setZoneColor(selectedZone.color)
  }, [selectedZone])

  const resetDraft = () => {
    setIsDrawing(false)
    setDraftPoints([])
  }

  const startDrawing = () => {
    setSelectedZoneId(null)
    resetDraft()
    setIsDrawing(true)
    setZoneName('Vùng mới')
    setZoneType('restricted')
    setZoneColor(DEFAULT_COLOR)
    setError('')
  }

  const getNormalizedPoint = (event) => {
    const rect = event.currentTarget.getBoundingClientRect()
    return screenToNormalized(
      { x: event.clientX - rect.left, y: event.clientY - rect.top },
      canvasSize.width,
      canvasSize.height,
    )
  }

  const handleCanvasClick = (event) => {
    if (!isDrawing || canvasSize.width === 0) return
    if (event.detail > 1) return
    setDraftPoints((current) => [...current, getNormalizedPoint(event)])
  }

  const handleCanvasDoubleClick = (event) => {
    if (!isDrawing || draftPoints.length < 3) return
    event.preventDefault()
    setIsDrawing(false)
  }

  const handleSave = async () => {
    if (selectedZone) {
      setSaving(true)
      setError('')
      try {
        const updated = await updateCameraZone(selectedZone.id, {
          name: zoneName,
          type: zoneType,
          color: zoneColor,
        })
        setZones((current) => current.map((zone) => (zone.id === updated.id ? updated : zone)))
      } catch (saveError) {
        setError(saveError.message)
      } finally {
        setSaving(false)
      }
      return
    }

    if (draftPoints.length < 3) {
      setError('Cần tối thiểu 3 điểm để lưu vùng')
      return
    }

    setSaving(true)
    setError('')
    try {
      const created = await createCameraZone(cameraId, {
        name: zoneName,
        type: zoneType,
        color: zoneColor,
        points: draftPoints,
      })
      setZones((current) => [created, ...current])
      setSelectedZoneId(created.id)
      resetDraft()
    } catch (saveError) {
      setError(saveError.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDeleteZone = async (zoneId) => {
    if (!window.confirm('Xóa vùng này?')) return

    try {
      await deleteCameraZone(zoneId)
      setZones((current) => current.filter((zone) => zone.id !== zoneId))
      if (selectedZoneId === zoneId) {
        setSelectedZoneId(null)
      }
    } catch (deleteError) {
      setError(deleteError.message)
    }
  }

  return (
    <section className="panel zone-editor">
      <div className="panel__header">
        <div>
          <h2 className="panel__title">Zone Editor v1.0</h2>
          <p className="panel__desc">Vẽ vùng trên snapshot với tọa độ chuẩn hóa (0–1)</p>
        </div>
        <div className="zone-editor__toolbar">
          <button type="button" className="btn btn--outline" onClick={startDrawing} disabled={saving}>
            Draw Zone
          </button>
          <button type="button" className="btn btn--outline" onClick={resetDraft} disabled={saving}>
            Cancel
          </button>
          <button type="button" className="btn btn--primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Đang lưu...' : 'Save'}
          </button>
        </div>
      </div>

      {error ? <div className="zone-editor__error">{error}</div> : null}
      {loading ? <div className="zone-editor__loading">Đang tải vùng...</div> : null}

      <div className="zone-editor__layout">
        <div className="zone-editor__canvas-wrap" ref={containerRef}>
          {snapshotUrl ? (
            <>
              <img
                src={snapshotUrl}
                alt="Camera snapshot"
                className="zone-editor__image"
                onLoad={updateCanvasSize}
              />
              {canvasSize.width > 0 ? (
                <svg
                  className="zone-editor__svg"
                  viewBox={`0 0 ${canvasSize.width} ${canvasSize.height}`}
                  onClick={handleCanvasClick}
                  onDoubleClick={handleCanvasDoubleClick}
                >
                  {zones.map((zone) => (
                    <polygon
                      key={zone.id}
                      points={pointsToSvgString(zone.points, canvasSize.width, canvasSize.height)}
                      fill={zone.color}
                      fillOpacity={zone.id === selectedZoneId ? 0.35 : 0.22}
                      stroke={zone.color}
                      strokeWidth={zone.id === selectedZoneId ? 3 : 2}
                      onClick={(event) => {
                        event.stopPropagation()
                        setSelectedZoneId(zone.id)
                        resetDraft()
                      }}
                    />
                  ))}

                  {draftPoints.length > 0 ? (
                    <>
                      <polyline
                        points={pointsToSvgString(draftPoints, canvasSize.width, canvasSize.height)}
                        fill="rgba(255,0,0,0.12)"
                        stroke={zoneColor}
                        strokeWidth={2}
                      />
                      {draftPoints.map((point, index) => {
                        const x = point.x * canvasSize.width
                        const y = point.y * canvasSize.height
                        return <circle key={`${index}-${x}`} cx={x} cy={y} r={5} fill={zoneColor} />
                      })}
                    </>
                  ) : null}
                </svg>
              ) : null}
            </>
          ) : (
            <div className="zone-editor__empty">Chụp snapshot trước khi vẽ vùng.</div>
          )}
        </div>

        <aside className="zone-editor__sidebar">
          <div className="zone-editor__fields">
            <label>
              <span>Tên vùng</span>
              <input
                className="settings-form__input"
                value={zoneName}
                onChange={(e) => setZoneName(e.target.value)}
              />
            </label>
            <label>
              <span>Loại vùng</span>
              <select
                className="settings-form__input"
                value={zoneType}
                onChange={(e) => setZoneType(e.target.value)}
              >
                {ZONE_TYPE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </label>
            <label>
              <span>Màu</span>
              <input
                type="color"
                className="settings-form__input"
                value={zoneColor}
                onChange={(e) => setZoneColor(e.target.value)}
              />
            </label>
          </div>

          <div className="zone-editor__list">
            <h3>Danh sách vùng</h3>
            {zones.length === 0 ? (
              <p className="zone-editor__list-empty">Chưa có vùng nào.</p>
            ) : (
              zones.map((zone) => (
                <div
                  key={zone.id}
                  className={`zone-editor__list-item${selectedZoneId === zone.id ? ' zone-editor__list-item--active' : ''}`}
                >
                  <button
                    type="button"
                    className="zone-editor__list-main"
                    onClick={() => {
                      setSelectedZoneId(zone.id)
                      resetDraft()
                    }}
                  >
                    <span className="zone-editor__swatch" style={{ backgroundColor: zone.color }} />
                    <span>
                      <strong>{zone.name}</strong>
                      <small>{zone.type}</small>
                    </span>
                  </button>
                  <button
                    type="button"
                    className="btn btn--ghost zone-editor__delete"
                    onClick={() => handleDeleteZone(zone.id)}
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        </aside>
      </div>
    </section>
  )
}

export default ZoneEditor
