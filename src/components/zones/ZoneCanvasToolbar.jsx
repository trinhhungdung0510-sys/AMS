import {
  EyeOff,
  Hand,
  MousePointer2,
  Redo2,
  RotateCcw,
  Shapes,
  Square,
  Tag,
  Trash2,
  ZoomIn,
  ZoomOut,
} from 'lucide-react'

export const CANVAS_TOOLS = {
  SELECT: 'select',
  POLYGON: 'polygon',
  RECT: 'rect',
  PAN: 'pan',
}

function ZoneCanvasToolbar({
  activeTool,
  zoom,
  canUndo,
  canRedo,
  canDelete,
  showZoneNames,
  hideZones,
  onToolChange,
  onZoomIn,
  onZoomOut,
  onZoomReset,
  onUndo,
  onRedo,
  onDelete,
  onToggleZoneNames,
  onToggleHideZones,
}) {
  const tools = [
    { id: CANVAS_TOOLS.SELECT, label: 'Con trỏ', Icon: MousePointer2 },
    { id: CANVAS_TOOLS.POLYGON, label: 'Vẽ Polygon', Icon: Shapes },
    { id: CANVAS_TOOLS.RECT, label: 'Vẽ Rectangle', Icon: Square },
    { id: CANVAS_TOOLS.PAN, label: 'Di chuyển', Icon: Hand },
  ]

  return (
    <div className="zone-editor-canvas-toolbar" role="toolbar" aria-label="Công cụ vẽ vùng">
      <div className="zone-editor-canvas-toolbar__group">
        {tools.map(({ id, label, Icon }) => (
          <button
            key={id}
            type="button"
            className={`zone-tool-btn${activeTool === id ? ' zone-tool-btn--active' : ''}`}
            title={label}
            aria-pressed={activeTool === id}
            onClick={() => onToolChange(id)}
          >
            <Icon size={16} />
            <span>{label}</span>
          </button>
        ))}
      </div>

      <div className="zone-editor-canvas-toolbar__divider" aria-hidden="true" />

      <div className="zone-editor-canvas-toolbar__group zone-editor-canvas-toolbar__zoom">
        <span className="zone-editor-canvas-toolbar__label">Zoom</span>
        <button type="button" className="zone-tool-btn" title="Thu nhỏ" onClick={onZoomOut}>
          <ZoomOut size={16} />
        </button>
        <button
          type="button"
          className="zone-tool-btn zone-editor-canvas-toolbar__zoom-value"
          title="Đặt lại zoom"
          onClick={onZoomReset}
        >
          {Math.round(zoom * 100)}%
        </button>
        <button type="button" className="zone-tool-btn" title="Phóng to" onClick={onZoomIn}>
          <ZoomIn size={16} />
        </button>
      </div>

      <div className="zone-editor-canvas-toolbar__divider" aria-hidden="true" />

      <div className="zone-editor-canvas-toolbar__group">
        <button
          type="button"
          className="zone-tool-btn"
          title="Undo"
          disabled={!canUndo}
          onClick={onUndo}
        >
          <RotateCcw size={16} />
          <span>Undo</span>
        </button>
        <button
          type="button"
          className="zone-tool-btn"
          title="Redo"
          disabled={!canRedo}
          onClick={onRedo}
        >
          <Redo2 size={16} />
          <span>Redo</span>
        </button>
        <button
          type="button"
          className="zone-tool-btn zone-tool-btn--danger"
          title="Xóa"
          disabled={!canDelete}
          onClick={onDelete}
        >
          <Trash2 size={16} />
          <span>Xóa</span>
        </button>
      </div>

      <div className="zone-editor-canvas-toolbar__divider" aria-hidden="true" />

      <div className="zone-editor-canvas-toolbar__group">
        <button
          type="button"
          className={`zone-tool-btn${showZoneNames ? ' zone-tool-btn--active' : ''}`}
          title="Hiển thị tên vùng"
          aria-pressed={showZoneNames}
          onClick={onToggleZoneNames}
        >
          <Tag size={16} />
          <span>Hiển thị tên vùng</span>
        </button>
        <button
          type="button"
          className={`zone-tool-btn${hideZones ? ' zone-tool-btn--active' : ''}`}
          title="Ẩn vùng"
          aria-pressed={hideZones}
          onClick={onToggleHideZones}
        >
          <EyeOff size={16} />
          <span>Ẩn vùng</span>
        </button>
      </div>
    </div>
  )
}

export default ZoneCanvasToolbar
