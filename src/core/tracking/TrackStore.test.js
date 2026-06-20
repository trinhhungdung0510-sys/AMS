import { describe, expect, it, beforeEach } from 'vitest'
import { TrackStore } from './TrackStore'

describe('TrackStore', () => {
  let store

  beforeEach(() => {
    store = new TrackStore()
  })

  it('creates a new track on first upsert', () => {
    const { track, isNew } = store.upsertTrack({
      cameraId: 'CAM-1',
      trackId: 'T-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:00Z',
      currentZoneId: 'CZ-1',
      metadata: { confidence: 0.9 },
    })

    expect(isNew).toBe(true)
    expect(track.trackId).toBe('T-1')
    expect(track.cameraId).toBe('CAM-1')
    expect(track.firstSeenAt).toBe('2026-06-22T10:00:00Z')
    expect(track.currentZoneId).toBe('CZ-1')
  })

  it('updates existing track and preserves firstSeenAt', () => {
    store.upsertTrack({
      cameraId: 'CAM-1',
      trackId: 'T-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:00Z',
      currentZoneId: 'CZ-1',
    })

    const { track, isNew, previousTrack } = store.upsertTrack({
      cameraId: 'CAM-1',
      trackId: 'T-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:05Z',
      currentZoneId: 'CZ-2',
      metadata: { confidence: 0.95 },
    })

    expect(isNew).toBe(false)
    expect(previousTrack.currentZoneId).toBe('CZ-1')
    expect(track.firstSeenAt).toBe('2026-06-22T10:00:00Z')
    expect(track.lastSeenAt).toBe('2026-06-22T10:00:05Z')
    expect(track.currentZoneId).toBe('CZ-2')
    expect(track.metadata.confidence).toBe(0.95)
  })

  it('gets, lists, and removes tracks by camera', () => {
    store.upsertTrack({
      cameraId: 'CAM-1',
      trackId: 'T-1',
      objectClass: 'person',
      timestamp: '2026-06-22T10:00:00Z',
    })
    store.upsertTrack({
      cameraId: 'CAM-2',
      trackId: 'T-2',
      objectClass: 'animal',
      timestamp: '2026-06-22T10:00:00Z',
    })

    expect(store.getTrack('CAM-1', 'T-1')?.trackId).toBe('T-1')
    expect(store.getTracksByCamera('CAM-1')).toHaveLength(1)
    expect(store.removeTrack('CAM-1', 'T-1')).toBe(true)
    expect(store.getTrack('CAM-1', 'T-1')).toBeNull()
  })
})
