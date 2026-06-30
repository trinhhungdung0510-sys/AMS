import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Plus } from 'lucide-react'
import { CAMERA_ZONE_TYPES, DEFAULT_ZONE_COLOR, ZONE_NAME_SUGGESTIONS } from '../../config/cameraZones'
import {
  buildZoneTree,
  createZone,
  deleteZone,
  getZones,
  updateZone,
} from '../../services/zoneService'
import { publishCameraZones } from '../../services/zonePublishService'
import { loadEngineZones } from '../../utils/cameraZoneReadiness'
import { getReferenceFromMetrics, resolveNormalizedPoints } from '../../utils/zoneGeometry'
import ZoneCanvas from './ZoneCanvas'
import ZoneCanvasToolbar, { CANVAS_TOOLS } from './ZoneCanvasToolbar'
import ZoneList from './ZoneList'

const MODES = {
  VIEW: 'view',
  ADD: 'add',
  EDIT: 'edit',
}

const DEFAULT_FORM = {
  name: '',
  description: '',
  type: 'monitoring',
  color: DEFAULT_ZONE_COLOR,
  parent_zone_id: null,
}

function ZoneEditor({ cameraId, previewUrl, readOnly = false }) {
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [mode, setMode] = useState(MODES.VIEW)
  const [activeTool, setActiveTool] = useState(CANVAS_TOOLS.SELECT)
  const [drawShape, setDrawShape] = useState(null)
  const [selectedZoneId, setSelectedZoneId] = useState(null)
  const [draftPoints, setDraftPoints] = useState([])
  const [historyPast, setHistoryPast] = useState([])
  const [historyFuture, setHistoryFuture] = useState([])
  const [referenceSize, setReferenceSize] = useState({ width: null, height: null })
  const [form, setForm] = useState(DEFAULT_FORM)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [showZoneNames, setShowZoneNames] = useState(true)
  const [hideZones, setHideZones] = useState(false)
  const [filteredCount, setFilteredCount] = useState(0)
  const mountedRef = useRef(true)

  const zoneTree = useMemo(() => buildZoneTree(zones), [zones])
  const rootZones = useMemo(() => zones.filter((zone) => !zone.parent_zone_id), [zones])
  const selectedZone = zones.find((zone) => zone.id === selectedZoneId) ?? null
  const isDrawing = mode === MODES.ADD || mode === MODES.EDIT

  useEffect(() => {
    mountedRef.current = true
    return () => {
      mountedRef.current = false
    }
  }, [])

  const loadZones = useCallback(async () => {
    if (!cameraId) return

    setLoading(true)
    setError('')

    try {
      const data = await loadEngineZones(cameraId)
      if (!mountedRef.current) return
      setZones(data)
    } catch (loadError) {
      if (!mountedRef.current) return
      setError(loadError.message)
    } finally {
      if (mountedRef.current) setLoading(false)
    }
  }, [cameraId])

  useEffect(() => {
    loadZones()
  }, [loadZones])

  useEffect(() => {
    if (!selectedZone) return
    setForm({
      name: selectedZone.name,
      description: selectedZone.description || '',
      type: selectedZone.type,
      color: selectedZone.color,
      parent_zone_id: selectedZone.parent_zone_id,
    })
  }, [selectedZone])

  const clearHistory = useCallback(() => {
    setHistoryPast([])
    setHistoryFuture([])
  }, [])

  const resetDraft = useCallback(() => {
    setDraftPoints([])
    setDrawShape(null)
    setMode(MODES.VIEW)
    setActiveTool(CANVAS_TOOLS.SELECT)
    setError('')
    clearHistory()
  }, [clearHistory])

  const setDraftWithHistory = useCallback((updater) => {
    setDraftPoints((current) => {
      const next = typeof updater === 'function' ? updater(current) : updater
      setHistoryPast((past) => [...past.slice(-50), current])
      setHistoryFuture([])
      return next
    })
  }, [])

  const startDrawing = useCallback((shape) => {
    setSelectedZoneId(null)
    setDraftPoints([])
    clearHistory()
    setForm({
      ...DEFAULT_FORM,
      name: shape === 'rect' ? 'Vùng chữ nhật mới' : 'Vùng mới',
    })
    setDrawShape(shape)
    setMode(MODES.ADD)
    setError('')
  }, [clearHistory])

  const handleToolChange = (tool) => {
    if (readOnly) return
    setActiveTool(tool)

    if (tool === CANVAS_TOOLS.SELECT) {
      if (mode === MODES.ADD) resetDraft()
      return
    }

    if (tool === CANVAS_TOOLS.PAN) {
      return
    }

    if (tool === CANVAS_TOOLS.POLYGON) {
      startDrawing('polygon')
      return
    }

    if (tool === CANVAS_TOOLS.RECT) {
      startDrawing('rect')
    }
  }

  const handleAddZone = () => {
    if (readOnly) return
    setActiveTool(CANVAS_TOOLS.POLYGON)
    startDrawing('polygon')
  }

  const handleEditZone = (zone) => {
    if (readOnly) return
    const target = zone || selectedZone
    if (!target) {
      setError('Chọn một vùng để chỉnh sửa')
      return
    }

    setSelectedZoneId(target.id)
    const points = resolveNormalizedPoints(target, referenceSize)
    setDraftPoints(points)
    clearHistory()
    setForm({
      name: target.name,
      description: target.description || '',
      type: target.type,
      color: target.color,
      parent_zone_id: target.parent_zone_id,
    })
    setDrawShape('polygon')
    setMode(MODES.EDIT)
    setActiveTool(CANVAS_TOOLS.POLYGON)
    setError('')
  }

  const handleSelectZone = (zone) => {
    if (isDrawing) return
    setSelectedZoneId(zone.id)
    setActiveTool(CANVAS_TOOLS.SELECT)
    resetDraft()
  }

  const removeZoneFromState = (zoneId) => {
    setZones((current) => {
      const next = current.filter(
        (zone) => zone.id !== zoneId && zone.parent_zone_id !== zoneId,
      )
      setSelectedZoneId((selectedId) => {
        if (!selectedId || selectedId === zoneId) return null
        const selected = current.find((zone) => zone.id === selectedId)
        if (selected?.parent_zone_id === zoneId) return null
        return next.some((zone) => zone.id === selectedId) ? selectedId : null
      })
      return next
    })
    resetDraft()
  }

  const handleDeleteZone = async (zoneId) => {
    if (readOnly) return
    const targetId = zoneId || selectedZoneId
    if (!targetId) return
    if (!window.confirm('Xóa vùng này? SubZone con cũng sẽ bị xóa.')) return

    try {
      await deleteZone(targetId)
      if (!mountedRef.current) return
      setZones((current) => {
        const nextZones = current.filter(
          (zone) => zone.id !== targetId && zone.parent_zone_id !== targetId,
        )
        publishCameraZones(cameraId, { zones: nextZones })
        setSelectedZoneId((selectedId) => {
          if (!selectedId || selectedId === targetId) return null
          const selected = current.find((zone) => zone.id === selectedId)
          if (selected?.parent_zone_id === targetId) return null
          return nextZones.some((zone) => zone.id === selectedId) ? selectedId : null
        })
        return nextZones
      })
      resetDraft()
    } catch (deleteError) {
      if (!mountedRef.current) return
      setError(deleteError.message)
    }
  }

  const handleSave = async () => {
    if (readOnly) return
    if (draftPoints.length < 3) {
      setError('Cần tối thiểu 3 điểm để tạo polygon')
      return
    }

    if (!form.name.trim()) {
      setError('Tên vùng không được để trống')
      return
    }

    if (!referenceSize.width || !referenceSize.height) {
      setError('Chưa xác định kích thước ảnh reference. Vui lòng đợi preview tải xong.')
      return
    }

    setSaving(true)
    setError('')

    const payload = {
      name: form.name.trim(),
      description: form.description.trim() || null,
      type: form.type,
      color: form.color,
      points: draftPoints,
      reference_width: referenceSize.width,
      reference_height: referenceSize.height,
      parent_zone_id: mode === MODES.ADD ? (form.parent_zone_id || null) : selectedZone?.parent_zone_id ?? null,
    }

    try {
      if (mode === MODES.EDIT && selectedZone) {
        const updated = await updateZone(selectedZone.id, payload)
        if (!mountedRef.current) return
        setZones((current) => {
          const nextZones = current.map((zone) => (zone.id === updated.id ? updated : zone))
          publishCameraZones(cameraId, { zones: nextZones })
          return nextZones
        })
        setSelectedZoneId(updated.id)
      } else {
        const created = await createZone(cameraId, payload)
        if (!mountedRef.current) return
        setZones((current) => {
          const nextZones = [...current, created]
          publishCameraZones(cameraId, { zones: nextZones })
          return nextZones
        })
        setSelectedZoneId(created.id)
      }
      resetDraft()
    } catch (saveError) {
      if (!mountedRef.current) return
      setError(saveError.message)
    } finally {
      if (mountedRef.current) setSaving(false)
    }
  }

  const handleCanvasClick = (point) => {
    if (!isDrawing || drawShape !== 'polygon') return
    setDraftWithHistory((current) => [...current, point])
  }

  const handleDraftPointsSet = (points) => {
    if (!isDrawing || drawShape !== 'rect') return
    setDraftWithHistory(points)
  }

  const handleCanvasDoubleClick = () => {
    if (draftPoints.length < 3) return
    handleSave()
  }

  const handleUndo = () => {
    if (!historyPast.length) return
    const previous = historyPast[historyPast.length - 1]
    setHistoryPast((current) => current.slice(0, -1))
    setHistoryFuture((current) => [draftPoints, ...current])
    setDraftPoints(previous)
  }

  const handleRedo = () => {
    if (!historyFuture.length) return
    const next = historyFuture[0]
    setHistoryFuture((current) => current.slice(1))
    setHistoryPast((current) => [...current, draftPoints])
    setDraftPoints(next)
  }

  const handleZoomIn = () => {
    setZoom((current) => Math.min(3, Number((current + 0.1).toFixed(2))))
  }

  const handleZoomOut = () => {
    setZoom((current) => Math.max(0.5, Number((current - 0.1).toFixed(2))))
  }

  const handleZoomReset = () => {
    setZoom(1)
    setPan({ x: 0, y: 0 })
  }

  const drawingHint = drawShape === 'rect'
    ? 'Kéo thả 2 góc đối diện để vẽ hình chữ nhật'
    : 'Click để thêm điểm · Double-click để lưu nhanh'

  return (
    <section className={`zone-editor zone-editor--enterprise${readOnly ? ' zone-editor--readonly' : ''}`}>
      {readOnly ? (
        <p className="zone-editor__readonly-notice" role="status">
          Chế độ chỉ xem — bạn không có quyền Quản lý vùng ATSH. Chỉ Chủ trại hoặc vai trò được cấp quyền mới chỉnh sửa vùng.
        </p>
      ) : null}
      <div className="zone-editor__layout">
        <div className="zone-editor__preview">
          <ZoneCanvasToolbar
            activeTool={activeTool}
            zoom={zoom}
            canUndo={historyPast.length > 0}
            canRedo={historyFuture.length > 0}
            canDelete={Boolean(selectedZoneId) && !isDrawing}
            showZoneNames={showZoneNames}
            hideZones={hideZones}
            onToolChange={handleToolChange}
            onZoomIn={handleZoomIn}
            onZoomOut={handleZoomOut}
            onZoomReset={handleZoomReset}
            onUndo={handleUndo}
            onRedo={handleRedo}
            onDelete={() => handleDeleteZone(selectedZoneId)}
            onToggleZoneNames={() => setShowZoneNames((current) => !current)}
            onToggleHideZones={() => setHideZones((current) => !current)}
          />

          <ZoneCanvas
            previewUrl={previewUrl}
            zones={zones}
            selectedZoneId={selectedZoneId}
            draftPoints={draftPoints}
            draftColor={form.color}
            isDrawing={isDrawing}
            drawShape={drawShape}
            activeTool={activeTool}
            zoom={zoom}
            pan={pan}
            showZoneNames={showZoneNames}
            hideZones={hideZones}
            onCanvasClick={handleCanvasClick}
            onCanvasDoubleClick={handleCanvasDoubleClick}
            onDraftPointsSet={handleDraftPointsSet}
            onSelectZone={handleSelectZone}
            onPanChange={setPan}
            onZoomChange={setZoom}
            onMetricsChange={(metrics) => {
              setReferenceSize(getReferenceFromMetrics(metrics))
            }}
          />

          {isDrawing ? (
            <p className="zone-editor__hint">
              {drawingHint} ({draftPoints.length} điểm)
            </p>
          ) : (
            <p className="zone-editor__hint zone-editor__hint--muted">
              Click thẻ vùng để highlight · Double-click thẻ để chỉnh sửa · Dùng toolbar phía trên để vẽ
            </p>
          )}
        </div>

        <aside className="zone-editor__panel">
          <header className="zone-editor__panel-header">
            <div>
              <h3 className="zone-editor__panel-title">Danh sách vùng</h3>
              <span className="zone-editor__panel-meta">
                {filteredCount === zones.length
                  ? `${zones.length} vùng · không giới hạn`
                  : `Hiển thị ${filteredCount} / ${zones.length} vùng`}
              </span>
            </div>
          </header>

          <div className="zone-editor__panel-list">
            <ZoneList
              zoneTree={zoneTree}
              zones={zones}
              selectedZoneId={selectedZoneId}
              loading={loading}
              mode={mode}
              modes={MODES}
              isDrawing={isDrawing}
              onSelectZone={handleSelectZone}
              onEditZone={handleEditZone}
              onDeleteZone={handleDeleteZone}
              onFilteredCountChange={(count) => setFilteredCount(count)}
            />
          </div>

          {error ? <div className="zone-editor__error">{error}</div> : null}

          {isDrawing ? (
            <div className="zone-editor__form">
              <label>
                <span>Tên vùng</span>
                <input
                  className="settings-form__input"
                  list="zone-name-suggestions"
                  value={form.name}
                  onChange={(e) => setForm((current) => ({ ...current, name: e.target.value }))}
                />
                <datalist id="zone-name-suggestions">
                  {ZONE_NAME_SUGGESTIONS.map((name) => (
                    <option key={name} value={name} />
                  ))}
                </datalist>
              </label>
              <label>
                <span>Loại vùng</span>
                <select
                  className="settings-form__input"
                  value={form.type}
                  onChange={(e) => setForm((current) => ({ ...current, type: e.target.value }))}
                >
                  {CAMERA_ZONE_TYPES.map((option) => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </label>
              <label>
                <span>Màu</span>
                <input
                  type="color"
                  className="settings-form__input zone-editor__color-input"
                  value={form.color}
                  onChange={(e) => setForm((current) => ({ ...current, color: e.target.value }))}
                />
              </label>
              {mode === MODES.ADD ? (
                <label>
                  <span>Thuộc vùng cha (SubZone)</span>
                  <select
                    className="settings-form__input"
                    value={form.parent_zone_id || ''}
                    onChange={(e) => setForm((current) => ({
                      ...current,
                      parent_zone_id: e.target.value || null,
                    }))}
                  >
                    <option value="">— Vùng chính —</option>
                    {rootZones.map((zone) => (
                      <option key={zone.id} value={zone.id}>{zone.name}</option>
                    ))}
                  </select>
                </label>
              ) : null}
            </div>
          ) : null}

          <footer className="zone-editor__actions">
            <button
              type="button"
              className="btn btn--primary zone-editor__action"
              onClick={handleAddZone}
              disabled={readOnly || saving || loading || isDrawing}
            >
              <Plus size={16} />
              Thêm vùng
            </button>
            <button
              type="button"
              className="btn btn--outline zone-editor__action"
              onClick={handleSave}
              disabled={readOnly || saving || loading || !isDrawing || draftPoints.length < 3}
            >
              {saving ? 'Đang lưu...' : 'Lưu'}
            </button>
            <button
              type="button"
              className="btn btn--outline zone-editor__action"
              onClick={resetDraft}
              disabled={readOnly || saving || !isDrawing}
            >
              Hủy
            </button>
          </footer>
        </aside>
      </div>
    </section>
  )
}

export default ZoneEditor
