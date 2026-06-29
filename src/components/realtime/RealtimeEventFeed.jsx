import CollapsibleRealtimeEventPanel from './CollapsibleRealtimeEventPanel'

function RealtimeEventFeed({ limit = 50, filterCameraId = null, defaultExpanded = false }) {
  return (
    <CollapsibleRealtimeEventPanel
      defaultExpanded={defaultExpanded}
      variant="sidebar"
      limit={limit}
      filterCameraId={filterCameraId}
    />
  )
}

export default RealtimeEventFeed
