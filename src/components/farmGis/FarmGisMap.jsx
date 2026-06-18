import { useEffect } from 'react'
import { MapContainer, Polyline, TileLayer, useMap, useMapEvents } from 'react-leaflet'
import MapEditorOverlay from './MapEditorOverlay'
import { FLOW_TYPES } from '../../data/smartFarmDesigner'
import { FARM_ZOOM, TILE_LAYERS } from '../../data/farmGisMap'

function MapResizeFix() {
  const map = useMap()
  useEffect(() => {
    const timer = setTimeout(() => map.invalidateSize(), 120)
    return () => clearTimeout(timer)
  }, [map])
  return null
}

function MapFlyTo({ target }) {
  const map = useMap()
  useEffect(() => {
    if (!target) return
    map.flyTo([target.lat, target.lng], target.zoom || map.getZoom(), { duration: 0.8 })
  }, [map, target])
  return null
}

function MapInteractions({ pendingType, pendingRoute, pendingRuler, onAddAt, onMapClickExtra }) {
  useMapEvents({
    click(event) {
      if (pendingType) {
        onAddAt(pendingType, event.latlng.lat, event.latlng.lng)
        return
      }
      if (pendingRoute || pendingRuler) {
        onMapClickExtra(event.latlng.lat, event.latlng.lng)
      }
    },
  })
  return null
}

function FarmGisMap({
  layout,
  objects,
  routes = [],
  draftRoute = [],
  rulerPoints = [],
  selectedId,
  tool,
  pendingAddType,
  drawingRoute = false,
  drawingRuler = false,
  showAtsh = true,
  showCameras = true,
  showRoutes = true,
  showHeatmap = false,
  flyToTarget,
  onSelect,
  onUpdate,
  onDropType,
  onAddAt,
  onMapClickExtra,
}) {
  const tile = TILE_LAYERS[layout.baseLayer] || TILE_LAYERS.satellite
  const center = [layout.centerLat, layout.centerLng]

  return (
    <MapContainer
      center={center}
      zoom={layout.zoom || FARM_ZOOM}
      className="farm-gis-map__leaflet"
      zoomControl
    >
      <TileLayer attribution={tile.attribution} url={tile.url} />
      {layout.baseLayer === 'hybrid' && tile.overlayUrl && (
        <TileLayer url={tile.overlayUrl} attribution="" opacity={tile.overlayOpacity ?? 0.75} />
      )}
      <MapResizeFix />
      <MapFlyTo target={flyToTarget} />
      <MapInteractions
        pendingType={pendingAddType}
        pendingRoute={drawingRoute}
        pendingRuler={drawingRuler}
        onAddAt={onAddAt}
        onMapClickExtra={onMapClickExtra}
      />

      {showRoutes && routes.map((route) => {
        const meta = FLOW_TYPES.find((item) => item.type === route.routeType) || FLOW_TYPES[0]
        return (
          <Polyline
            key={route.id}
            positions={route.points}
            pathOptions={{
              color: route.valid === false ? '#dc2626' : meta.color,
              weight: 4,
              dashArray: route.valid === false ? '8 6' : undefined,
            }}
          />
        )
      })}

      {(drawingRoute && draftRoute.length > 0) && (
        <Polyline positions={draftRoute} pathOptions={{ color: '#0B6B1B', weight: 3, dashArray: '6 6' }} />
      )}

      {rulerPoints.length > 0 && (
        <Polyline positions={rulerPoints} pathOptions={{ color: '#F36A10', weight: 3, dashArray: '4 4' }} />
      )}

      <MapEditorOverlay
        objects={objects}
        selectedId={selectedId}
        tool={tool}
        showAtsh={showAtsh}
        showCameras={showCameras}
        showHeatmap={showHeatmap}
        onSelect={onSelect}
        onUpdate={onUpdate}
        onDropType={onDropType}
      />
    </MapContainer>
  )
}

export default FarmGisMap
