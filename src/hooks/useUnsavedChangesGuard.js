import { useEffect } from 'react'
import { UNSAVED_ZONE_CHANGES_MESSAGE } from '../utils/cameraZoneReadiness'

/**
 * Warns when leaving with unsaved zone edits.
 * Uses beforeunload only — compatible with BrowserRouter and RouterProvider.
 */
export function useUnsavedChangesGuard(isDirty, {
  enabled = true,
  message = UNSAVED_ZONE_CHANGES_MESSAGE,
} = {}) {
  const shouldBlock = Boolean(enabled && isDirty)

  useEffect(() => {
    if (!shouldBlock) return undefined

    const handleBeforeUnload = (event) => {
      event.preventDefault()
      event.returnValue = message
    }

    window.addEventListener('beforeunload', handleBeforeUnload)
    return () => window.removeEventListener('beforeunload', handleBeforeUnload)
  }, [shouldBlock, message])

  return { state: shouldBlock ? 'blocked' : 'unblocked' }
}
