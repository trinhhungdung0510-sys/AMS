import { useCallback, useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { Polygon, useMap } from 'react-leaflet'
import {
  ATSH_ZONE_TYPES,
  FARM_OBJECT_TYPES,
  getCameraFovPolygon,
  getRotatedCorners,
} from '../../data/farmGisMap'
import { HEATMAP_COLORS, objectDimensionsMeters } from '../../data/smartFarmDesigner'

const TYPE_LOOKUP = Object.fromEntries(FARM_OBJECT_TYPES.map((item) => [item.type, item]))

function geoSizeToPixels(map, obj) {
  const center = map.latLngToContainerPoint([obj.x, obj.y])
  const east = map.latLngToContainerPoint([obj.x, obj.y + obj.height / 2])
  const west = map.latLngToContainerPoint([obj.x, obj.y - obj.height / 2])
  const north = map.latLngToContainerPoint([obj.x + obj.width / 2, obj.y])
  const south = map.latLngToContainerPoint([obj.x - obj.width / 2, obj.y])
  return {
    center,
    width: Math.max(24, Math.abs(east.x - west.x)),
    height: Math.max(24, Math.abs(north.y - south.y)),
  }
}

function MapEditorOverlay({
  objects,
  selectedId,
  tool,
  showAtsh,
  showCameras,
  showHeatmap = false,
  onSelect,
  onUpdate,
  onDropType,
}) {
  const map = useMap()
  const [layoutTick, setLayoutTick] = useState(0)
  const [drag, setDrag] = useState(null)

  useEffect(() => {
    const bump = () => setLayoutTick((value) => value + 1)
    map.on('move zoom moveend zoomend resize', bump)
    bump()
    return () => {
      map.off('move zoom moveend zoomend resize', bump)
    }
  }, [map])

  useEffect(() => {
    const container = map.getContainer()
    const onDragOver = (event) => {
      event.preventDefault()
      event.dataTransfer.dropEffect = 'copy'
    }
    const onDrop = (event) => {
      event.preventDefault()
      const objectType = event.dataTransfer.getData('farm-object-type')
      if (!objectType) return
      const rect = container.getBoundingClientRect()
      const point = map.containerPointToLatLng([
        event.clientX - rect.left,
        event.clientY - rect.top,
      ])
      onDropType(objectType, point.lat, point.lng)
    }
    container.addEventListener('dragover', onDragOver)
    container.addEventListener('drop', onDrop)
    return () => {
      container.removeEventListener('dragover', onDragOver)
      container.removeEventListener('drop', onDrop)
    }
  }, [map, onDropType])

  const onPointerMove = useCallback((event) => {
    if (!drag) return
    const rect = map.getContainer().getBoundingClientRect()
    const point = map.containerPointToLatLng([
      event.clientX - rect.left,
      event.clientY - rect.top,
    ])

    if (drag.mode === 'move') {
      onUpdate(drag.id, { x: point.lat, y: point.lng })
      return
    }

    if (drag.mode === 'rotate') {
      const obj = objects.find((item) => item.id === drag.id)
      if (!obj) return
      const centerPt = map.latLngToContainerPoint([obj.x, obj.y])
      const mousePt = map.containerPointToLatLng([
        event.clientX - rect.left,
        event.clientY - rect.top,
      ])
      const centerMouse = map.latLngToContainerPoint([mousePt.lat, mousePt.lng])
      const angle = Math.atan2(centerMouse.y - centerPt.y, centerMouse.x - centerPt.x) * 180 / Math.PI + 90
      onUpdate(drag.id, { rotation: Math.round((angle + 360) % 360) })
      return
    }

    if (drag.mode === 'resize') {
      const obj = objects.find((item) => item.id === drag.id)
      if (!obj) return
      const deltaLat = Math.abs(point.lat - obj.x) * 2
      const deltaLng = Math.abs(point.lng - obj.y) * 2
      onUpdate(drag.id, {
        width: Math.max(0.00008, deltaLat),
        height: Math.max(0.00008, deltaLng),
      })
    }
  }, [drag, map, objects, onUpdate])

  useEffect(() => {
    if (!drag) return undefined
    window.addEventListener('pointermove', onPointerMove)
    window.addEventListener('pointerup', () => setDrag(null), { once: true })
    return () => window.removeEventListener('pointermove', onPointerMove)
  }, [drag, onPointerMove])

  void layoutTick

  const zoneObjects = objects.filter((item) => item.objectType !== 'camera')
  const cameraObjects = objects.filter((item) => item.objectType === 'camera')

  return (
    <>
      {showAtsh && zoneObjects.map((obj) => {
        const meta = showHeatmap
          ? (HEATMAP_COLORS[obj.atshLevel] || HEATMAP_COLORS.green)
          : (ATSH_ZONE_TYPES[obj.atshZoneType] || ATSH_ZONE_TYPES.buffer)
        return (
          <Polygon
            key={`atsh-${obj.id}`}
            positions={getRotatedCorners(obj)}
            pathOptions={{
              color: meta.color,
              fillColor: meta.color,
              fillOpacity: showHeatmap ? 0.5 : (selectedId === obj.id ? 0.35 : 0.22),
              weight: selectedId === obj.id ? 3 : 2,
            }}
            eventHandlers={{ click: () => onSelect(obj.id) }}
          />
        )
      })}

      {showCameras && cameraObjects.map((cam) => (
        <Polygon
          key={`fov-${cam.id}`}
          positions={getCameraFovPolygon(cam)}
          pathOptions={{
            color: cam.status === 'online' ? '#16a34a' : '#64748b',
            fillColor: cam.status === 'online' ? '#16a34a' : '#64748b',
            fillOpacity: 0.14,
            weight: 1,
          }}
        />
      ))}

      {createPortal(
        <div className="farm-editor-overlay">
          {objects.map((obj) => {
            const { center, width, height } = geoSizeToPixels(map, obj)
            const meta = TYPE_LOOKUP[obj.objectType] || TYPE_LOOKUP.gestation
            const isSelected = selectedId === obj.id
            const isCamera = obj.objectType === 'camera'
            const dims = isSelected && !isCamera ? objectDimensionsMeters(obj) : null

            return (
              <div
                key={obj.id}
                className={`farm-editor-object${isSelected ? ' farm-editor-object--selected' : ''}${isCamera ? ' farm-editor-object--camera' : ''}`}
                style={{
                  left: center.x,
                  top: center.y,
                  width,
                  height,
                  transform: `translate(-50%, -50%) rotate(${obj.rotation || 0}deg)`,
                }}
                onPointerDown={(event) => {
                  event.stopPropagation()
                  onSelect(obj.id)
                  if (tool === 'move') {
                    setDrag({ id: obj.id, mode: 'move' })
                  }
                }}
              >
                <div className="farm-editor-object__body" style={{ borderColor: ATSH_ZONE_TYPES[obj.atshZoneType]?.color }}>
                  <span className="farm-editor-object__icon">{meta.icon}</span>
                  <span className="farm-editor-object__name">{obj.name}</span>
                  {isCamera && (
                    <span className={`farm-editor-object__status farm-editor-object__status--${obj.status}`}>
                      {obj.status === 'online' ? '● Online' : '● Offline'}
                    </span>
                  )}
                  {dims && (
                    <span className="farm-editor-object__measure">
                      {dims.lengthM}×{dims.widthM} m · {dims.areaM2} m²
                    </span>
                  )}
                </div>

                {isSelected && tool === 'rotate' && (
                  <button
                    type="button"
                    className="farm-editor-handle farm-editor-handle--rotate"
                    aria-label="Xoay"
                    onPointerDown={(event) => {
                      event.stopPropagation()
                      setDrag({ id: obj.id, mode: 'rotate' })
                    }}
                  >
                    ↻
                  </button>
                )}

                {isSelected && tool === 'resize' && (
                  <button
                    type="button"
                    className="farm-editor-handle farm-editor-handle--resize"
                    aria-label="Thay đổi kích thước"
                    onPointerDown={(event) => {
                      event.stopPropagation()
                      setDrag({ id: obj.id, mode: 'resize' })
                    }}
                  />
                )}
              </div>
            )
          })}
        </div>,
        map.getContainer(),
      )}
    </>
  )
}

export default MapEditorOverlay
