import { describe, expect, it } from 'vitest'
import {
  computeEventMetrics,
  mergeEventLists,
  normalizeApiEvent,
  normalizeEngineEvent,
  normalizeWsPayload,
  resolveEventId,
  upsertEvent,
} from './eventNormalizer'

describe('eventNormalizer', () => {
  it('normalizes API event', () => {
    const event = normalizeApiEvent({
      id: 'EVT-1',
      ten_vi_pham: 'PERSON_ENTER',
      muc_do: 'Cảnh báo',
      ten_vung: 'Zone A',
      ten_camera: 'Cam 1',
      ten_trang_trai: 'Farm',
      do_tin_cay: 90,
      thoi_gian: '2026-06-20T10:00:00',
      trang_thai: 'Mới',
      nguoi_xu_ly: 'Ops',
    })

    expect(event.id).toBe('EVT-1')
    expect(event.typeLabel).toBe('PERSON_ENTER')
    expect(event.status).toBe('new')
  })

  it('normalizes engine websocket event', () => {
    const event = normalizeEngineEvent({
      id: 'EVT-2',
      camera_id: 'CAM-001',
      camera_name: 'Gate Cam',
      zone_id: 'ZONE-1',
      zone_name: 'Entrance',
      event_type: 'PERSON_COUNT',
      severity: 'MEDIUM',
      status: 'OPEN',
      confidence: 0.91,
      started_at: '2026-06-20T11:00:00+00:00',
    })

    expect(event.eventType).toBe('PERSON_COUNT')
    expect(event.confidence).toBe(91)
    expect(event.statusRaw).toBe('OPEN')
  })

  it('deduplicates by event id', () => {
    const first = normalizeEngineEvent({
      id: 'EVT-3',
      event_type: 'PERSON_ENTER',
      status: 'OPEN',
      severity: 'MEDIUM',
      started_at: '2026-06-20T10:00:00+00:00',
    })
    const updated = { ...first, statusRaw: 'RESOLVED', status: 'resolved' }
    const merged = upsertEvent([first], updated)

    expect(merged).toHaveLength(1)
    expect(merged[0].status).toBe('resolved')
  })

  it('appends websocket payload without refresh', () => {
    const payload = {
      type: 'event.created',
      payload: {
        event: {
          id: 'EVT-WS-1',
          event_type: 'ANIMAL_ENTER',
          camera_id: 'CAM-001',
          zone_name: 'Zone',
          severity: 'HIGH',
          status: 'OPEN',
          confidence: 0.8,
          started_at: '2026-06-20T12:00:00+00:00',
        },
      },
    }

    const normalized = normalizeWsPayload(payload)
    const events = upsertEvent([], normalized)

    expect(events[0].eventType).toBe('ANIMAL_ENTER')
  })

  it('resolves alternate event id fields from websocket payload', () => {
    const payload = {
      type: 'event.created',
      payload: {
        event: {
          event_id: 'EVT-ALT-1',
          event_type: 'PERSON_ENTER',
          severity: 'HIGH',
          status: 'OPEN',
          started_at: '2026-06-20T12:00:00+00:00',
        },
      },
    }

    expect(resolveEventId(payload.payload.event)).toBe('EVT-ALT-1')
    expect(normalizeWsPayload(payload)?.id).toBe('EVT-ALT-1')
  })

  it('merges api reload with websocket-only events', () => {
    const merged = mergeEventLists(
      [{ id: 'A', occurredAt: '2026-06-20T10:00:00+00:00' }],
      [{ id: 'B', occurredAt: '2026-06-20T11:00:00+00:00' }],
    )

    expect(merged.map((item) => item.id)).toEqual(['B', 'A'])
  })

  it('computes dashboard metrics', () => {
    const today = '2026-06-20'
    const metrics = computeEventMetrics(
      [
        {
          id: '1',
          statusRaw: 'OPEN',
          status: 'new',
          severityRaw: 'CRITICAL',
          occurredAt: `${today}T09:00:00`,
        },
        {
          id: '2',
          statusRaw: 'RESOLVED',
          status: 'resolved',
          severityRaw: 'MEDIUM',
          occurredAt: `${today}T08:00:00`,
        },
      ],
      [{ status: 'online' }, { status: 'offline' }],
      today,
    )

    expect(metrics.openEvents).toBe(1)
    expect(metrics.criticalEvents).toBe(1)
    expect(metrics.totalEventsToday).toBe(2)
    expect(metrics.onlineCameras).toBe(1)
    expect(metrics.totalCameras).toBe(2)
  })
})
