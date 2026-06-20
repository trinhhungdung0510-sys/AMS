import { getZoneTypeLabel } from '../../config/cameraZones'

function ZoneList({
  zoneTree,
  selectedZoneId,
  loading,
  onSelectZone,
  onDeleteZone,
}) {
  if (loading) {
    return <div className="zone-list__loading">Đang tải vùng...</div>
  }

  if (zoneTree.length === 0) {
    return <p className="zone-list__empty">Chưa có Zone nào. Bấm Add Zone để bắt đầu.</p>
  }

  return (
    <ul className="zone-list">
      {zoneTree.map((zone) => (
        <li key={zone.id} className="zone-list__group">
          <div
            className={`zone-list__item${selectedZoneId === zone.id ? ' zone-list__item--active' : ''}`}
          >
            <button
              type="button"
              className="zone-list__main"
              onClick={() => onSelectZone(zone)}
            >
              <span className="zone-list__swatch" style={{ backgroundColor: zone.color }} />
              <span>
                <strong>{zone.name}</strong>
                <small>{getZoneTypeLabel(zone.type)}</small>
              </span>
            </button>
            <button
              type="button"
              className="btn btn--ghost zone-list__delete"
              onClick={() => onDeleteZone(zone.id)}
            >
              Delete
            </button>
          </div>

          {zone.subzones?.length > 0 ? (
            <ul className="zone-list__subzones">
              {zone.subzones.map((subzone) => (
                <li
                  key={subzone.id}
                  className={`zone-list__item zone-list__item--sub${selectedZoneId === subzone.id ? ' zone-list__item--active' : ''}`}
                >
                  <button
                    type="button"
                    className="zone-list__main"
                    onClick={() => onSelectZone(subzone)}
                  >
                    <span className="zone-list__swatch" style={{ backgroundColor: subzone.color }} />
                    <span>
                      <strong>{subzone.name}</strong>
                      <small>{getZoneTypeLabel(subzone.type)}</small>
                    </span>
                  </button>
                  <button
                    type="button"
                    className="btn btn--ghost zone-list__delete"
                    onClick={() => onDeleteZone(subzone.id)}
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          ) : null}
        </li>
      ))}
    </ul>
  )
}

export default ZoneList
