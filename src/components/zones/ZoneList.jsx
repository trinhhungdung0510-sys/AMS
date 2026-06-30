import { useEffect, useMemo, useState } from 'react'
import { Search } from 'lucide-react'
import { Trash2 } from 'lucide-react'
import {
  CAMERA_ZONE_TYPES,
  ZONE_LIST_LEVEL_FILTERS,
  ZONE_LIST_SORT_OPTIONS,
  ZONE_LIST_STATUS_FILTERS,
  getZoneTypeLabel,
} from '../../config/cameraZones'
import {
  filterAndSortZoneItems,
  flattenZoneTree,
} from '../../utils/zoneListFilters'
import {
  getZonePointCount,
  getZoneStatusKey,
  getZoneStatusLabel,
} from '../../utils/zoneListUtils'

export { getZonePointCount, getZoneStatusKey, getZoneStatusLabel }

function ZoneCard({
  zone,
  isSubzone,
  parentName,
  isActive,
  statusLabel,
  statusKey,
  disabled,
  onSelectZone,
  onEditZone,
  onDeleteZone,
}) {
  const pointCount = getZonePointCount(zone)

  return (
    <li
      className={`zone-card${isActive ? ' zone-card--active' : ''}${isSubzone ? ' zone-card--sub' : ''}${disabled ? ' zone-card--disabled' : ''}`}
    >
      <button
        type="button"
        className="zone-card__body"
        disabled={disabled}
        onClick={() => onSelectZone(zone)}
        onDoubleClick={(event) => {
          event.preventDefault()
          if (!disabled) onEditZone(zone)
        }}
      >
        <div className="zone-card__header">
          <span className="zone-card__swatch" style={{ backgroundColor: zone.color }} />
          <div className="zone-card__title-wrap">
            <strong className="zone-card__name">{zone.name}</strong>
            {isSubzone && parentName ? (
              <small className="zone-card__parent">SubZone · {parentName}</small>
            ) : null}
          </div>
        </div>

        <dl className="zone-card__meta">
          <div className="zone-card__row">
            <dt>Loại vùng</dt>
            <dd>{getZoneTypeLabel(zone.type)}</dd>
          </div>
          <div className="zone-card__row">
            <dt>Màu</dt>
            <dd>
              <span className="zone-card__color-code">{zone.color}</span>
            </dd>
          </div>
          <div className="zone-card__row">
            <dt>Số điểm</dt>
            <dd>{pointCount}</dd>
          </div>
          <div className="zone-card__row">
            <dt>Trạng thái</dt>
            <dd>
              <span className={`zone-card__status zone-card__status--${statusKey}`}>
                {statusLabel}
              </span>
            </dd>
          </div>
        </dl>
      </button>

      <button
        type="button"
        className="zone-card__delete"
        title="Xóa vùng"
        disabled={disabled}
        onClick={(event) => {
          event.stopPropagation()
          onDeleteZone(zone.id)
        }}
      >
        <Trash2 size={14} />
      </button>
    </li>
  )
}

function ZoneListControls({
  query,
  typeFilter,
  levelFilter,
  statusFilter,
  sortBy,
  onQueryChange,
  onTypeFilterChange,
  onLevelFilterChange,
  onStatusFilterChange,
  onSortChange,
}) {
  return (
    <div className="zone-list-controls">
      <label className="zone-list-controls__search">
        <Search size={16} />
        <input
          type="search"
          className="settings-form__input"
          placeholder="Tìm vùng theo tên, loại, mô tả..."
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
        />
      </label>

      <div className="zone-list-controls__filters">
        <label>
          <span>Loại</span>
          <select
            className="settings-form__input"
            value={typeFilter}
            onChange={(event) => onTypeFilterChange(event.target.value)}
          >
            <option value="all">Tất cả loại</option>
            {CAMERA_ZONE_TYPES.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Cấp</span>
          <select
            className="settings-form__input"
            value={levelFilter}
            onChange={(event) => onLevelFilterChange(event.target.value)}
          >
            {ZONE_LIST_LEVEL_FILTERS.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Trạng thái</span>
          <select
            className="settings-form__input"
            value={statusFilter}
            onChange={(event) => onStatusFilterChange(event.target.value)}
          >
            {ZONE_LIST_STATUS_FILTERS.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Sắp xếp</span>
          <select
            className="settings-form__input"
            value={sortBy}
            onChange={(event) => onSortChange(event.target.value)}
          >
            {ZONE_LIST_SORT_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>
      </div>
    </div>
  )
}

function ZoneList({
  zoneTree,
  zones,
  selectedZoneId,
  loading,
  mode,
  modes,
  isDrawing,
  onSelectZone,
  onEditZone,
  onDeleteZone,
  onFilteredCountChange,
}) {
  const [query, setQuery] = useState('')
  const [typeFilter, setTypeFilter] = useState('all')
  const [levelFilter, setLevelFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [sortBy, setSortBy] = useState('name-asc')

  const statusContext = useMemo(
    () => ({ selectedZoneId, mode, modes }),
    [selectedZoneId, mode, modes],
  )

  const flatItems = useMemo(() => flattenZoneTree(zoneTree), [zoneTree])

  const visibleItems = useMemo(
    () => filterAndSortZoneItems(
      flatItems,
      { query, typeFilter, levelFilter, statusFilter, sortBy },
      statusContext,
    ),
    [flatItems, query, typeFilter, levelFilter, statusFilter, sortBy, statusContext],
  )

  useEffect(() => {
    onFilteredCountChange?.(visibleItems.length, zones.length)
  }, [visibleItems.length, zones.length, onFilteredCountChange])

  if (loading) {
    return <div className="zone-list__loading">Đang tải vùng...</div>
  }

  return (
    <>
      <ZoneListControls
        query={query}
        typeFilter={typeFilter}
        levelFilter={levelFilter}
        statusFilter={statusFilter}
        sortBy={sortBy}
        onQueryChange={setQuery}
        onTypeFilterChange={setTypeFilter}
        onLevelFilterChange={setLevelFilter}
        onStatusFilterChange={setStatusFilter}
        onSortChange={setSortBy}
      />

      {zones.length === 0 ? (
        <div className="zone-list__empty">
          <p>Chưa có vùng nào.</p>
          <small>Bấm &quot;+ Thêm vùng&quot; để bắt đầu — không giới hạn số lượng vùng trên camera.</small>
        </div>
      ) : visibleItems.length === 0 ? (
        <div className="zone-list__empty">
          <p>Không có vùng phù hợp bộ lọc.</p>
          <small>Thử đổi từ khóa tìm kiếm hoặc bộ lọc.</small>
        </div>
      ) : (
        <ul className="zone-list zone-list--cards">
          {visibleItems.map(({ zone, isSubzone, parentName }) => (
            <ZoneCard
              key={zone.id}
              zone={zone}
              isSubzone={isSubzone}
              parentName={parentName}
              isActive={selectedZoneId === zone.id}
              statusLabel={getZoneStatusLabel(zone, statusContext)}
              statusKey={getZoneStatusKey(zone, statusContext)}
              disabled={isDrawing}
              onSelectZone={onSelectZone}
              onEditZone={onEditZone}
              onDeleteZone={onDeleteZone}
            />
          ))}
        </ul>
      )}
    </>
  )
}

export default ZoneList
