import { Navigate, useSearchParams } from 'react-router-dom'

function SmartFarmDesignerPage() {
  const [searchParams] = useSearchParams()
  const query = searchParams.toString()
  const suffix = query ? `?${query}` : '?tab=ban-do'
  return <Navigate to={`/bang-dieu-khien${suffix.includes('tab=') ? suffix : '?tab=ban-do'}`} replace />
}

export default SmartFarmDesignerPage
