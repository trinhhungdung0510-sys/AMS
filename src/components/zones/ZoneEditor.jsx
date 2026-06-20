import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { CAMERA_ZONE_TYPES, DEFAULT_ZONE_COLOR } from '../../config/cameraZones'
import {
  buildZoneTree,
  createZone,
  deleteZone,
  getZones,
  updateZone,
} from '../../services/zoneService'
import { getReferenceFromMetrics, resolveNormalizedPoints } from '../../utils/zoneGeometry'
import ZoneCanvas from './ZoneCanvas'
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

function ZoneEditor({ cameraId, previewUrl }) {
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [mode, setMode] = useState(MODES.VIEW)
  const [selectedZoneId, setSelectedZoneId] = useState(null)
  const [draftPoints, setDraftPoints] = useState([])
  const [referenceSize, setReferenceSize] = useState({ width: null, height: null })
  const [form, setForm] = useState(DEFAULT_FORM)
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
      const data = await getZones(cameraId)
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

  const resetDraft = useCallback(() => {
    setDraftPoints([])
    setMode(MODES.VIEW)
  }, [])

  const handleAddZone = () => {
    setSelectedZoneId(null)
    setDraftPoints([])
    setForm({
      ...DEFAULT_FORM,
      name: 'Zone mới',
    })
    setMode(MODES.ADD)
    setError('')
  }

  const handleEditZone = () => {
    if (!selectedZone) {
      setError('Chọn một Zone để chỉnh sửa')
      return
    }
    setDraftPoints(resolveNormalizedPoints(selectedZone, referenceSize))
    setMode(MODES.EDIT)
    setError('')
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
    if (!window.confirm('Xóa zone này? SubZone con cũng sẽ bị xóa.')) return

    try {
      await deleteZone(zoneId)
      if (!mountedRef.current) return
      removeZoneFromState(zoneId)
    } catch (deleteError) {
      if (!mountedRef.current) return
      setError(deleteError.message)
    }
  }

  const handleSave = async () => {
    if (draftPoints.length < 3) {
      setError('Cần tối thiểu 3 điểm để tạo polygon')
      return
    }

    if (!form.name.trim()) {
      setError('Tên zone không được để trống')
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
        setZones((current) => current.map((zone) => (zone.id === updated.id ? updated : zone)))
        setSelectedZoneId(updated.id)
      } else {
        const created = await createZone(cameraId, payload)
        if (!mountedRef.current) return
        setZones((current) => [...current, created])
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
    if (!isDrawing) return
    setDraftPoints((current) => [...current, point])
  }

  const handleCanvasDoubleClick = () => {
    if (draftPoints.length < 3) return
    handleSave()
  }

  return (
    <section className="zone-manager">
      <div className="zone-manager__toolbar">
        <button type="button" className="btn btn--primary" onClick={handleAddZone} disabled={saving || loading}>
          Add Zone
        </button>
        <button
          type="button"
          className="btn btn--outline"
          onClick={handleEditZone}
          disabled={saving || loading || !selectedZone}
        >
          Edit Zone
        </button>
        <button
          type="button"
          className="btn btn--outline"
          onClick={() => selectedZone && handleDeleteZone(selectedZone.id)}
          disabled={saving || loading || !selectedZone}
        >
          Delete Zone
        </button>
        {isDrawing ? (
          <>
            <button type="button" className="btn btn--outline" onClick={resetDraft} disabled={saving}>
              Cancel
            </button>
            <button type="button" className="btn btn--primary" onClick={handleSave} disabled={saving}>
              {saving ? 'Đang lưu...' : 'Save Polygon'}
            </button>
          </>
        ) : null}
      </div>

      {error ? <div className="zone-manager__error">{error}</div> : null}

      {isDrawing ? (
        <p className="zone-manager__hint">
          Click để thêm điểm, double-click để hoàn thành polygon ({draftPoints.length} điểm).
        </p>
      ) : null}

      <div className="zone-manager__layout">
        <ZoneCanvas
          previewUrl={previewUrl}
          zones={zones}
          selectedZoneId={selectedZoneId}
          draftPoints={draftPoints}
          draftColor={form.color}
          isDrawing={isDrawing}
          onCanvasClick={handleCanvasClick}
          onCanvasDoubleClick={handleCanvasDoubleClick}
          onSelectZone={(zone) => {
            setSelectedZoneId(zone.id)
            resetDraft()
          }}
          onMetricsChange={(metrics) => {
            setReferenceSize(getReferenceFromMetrics(metrics))
          }}
        />

        <aside className="zone-manager__sidebar">
          <div className="zone-manager__form">
            <label>
              <span>Tên Zone</span>
              <input
                className="settings-form__input"
                value={form.name}
                onChange={(e) => setForm((current) => ({ ...current, name: e.target.value }))}
                disabled={!isDrawing && !selectedZone}
              />
            </label>
            <label>
              <span>Mô tả</span>
              <textarea
                className="settings-form__input"
                rows={2}
                value={form.description}
                onChange={(e) => setForm((current) => ({ ...current, description: e.target.value }))}
                disabled={!isDrawing && !selectedZone}
              />
            </label>
            <label>
              <span>Loại</span>
              <select
                className="settings-form__input"
                value={form.type}
                onChange={(e) => setForm((current) => ({ ...current, type: e.target.value }))}
                disabled={!isDrawing && !selectedZone}
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
                className="settings-form__input"
                value={form.color}
                onChange={(e) => setForm((current) => ({ ...current, color: e.target.value }))}
                disabled={!isDrawing && !selectedZone}
              />
            </label>
            {mode === MODES.ADD ? (
              <label>
                <span>Thuộc Zone cha (SubZone)</span>
                <select
                  className="settings-form__input"
                  value={form.parent_zone_id || ''}
                  onChange={(e) => setForm((current) => ({
                    ...current,
                    parent_zone_id: e.target.value || null,
                  }))}
                >
                  <option value="">— Zone chính —</option>
                  {rootZones.map((zone) => (
                    <option key={zone.id} value={zone.id}>{zone.name}</option>
                  ))}
                </select>
              </label>
            ) : null}
          </div>

          <ZoneList
            zoneTree={zoneTree}
            selectedZoneId={selectedZoneId}
            loading={loading}
            onSelectZone={(zone) => {
              setSelectedZoneId(zone.id)
              resetDraft()
            }}
            onDeleteZone={handleDeleteZone}
          />
        </aside>
      </div>
    </section>
  )
}

export default ZoneEditor
