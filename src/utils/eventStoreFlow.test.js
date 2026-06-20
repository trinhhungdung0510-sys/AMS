import { describe, expect, it } from 'vitest'
import {
  computeEventMetrics,
  normalizeWsPayload,
  upsertEvent,
} from './eventNormalizer'

const REPLAY_FIXTURE = {
  type: 'event.created',
  payload: {
    event: {
      id: 'EVT-REPLAY-1',
      event_type: 'PERSON_ENTER',
      camera_id: 'CAM-001',
      zone_name: 'Entrance',
      severity: 'MEDIUM',
      status: 'OPEN',
      confidence: 0.95,
      started_at: '2026-06-20T10:00:00+00:00',
    },
  },
}

const YOLO_DETECTION = {
  type: 'event.created',
  payload: {
    event: {
      id: 'EVT-YOLO-1',
      event_type: 'PERSON_COUNT',
      camera_id: 'CAM-001',
      zone_name: 'ZONE-TEST-MAIN',
      severity: 'HIGH',
      status: 'OPEN',
      confidence: 0.88,
      started_at: '2026-06-20T10:05:00+00:00',
    },
  },
}

function applyWsMessage(events, payload) {
  const normalized = normalizeWsPayload(payload)
  if (!normalized) return events
  return upsertEvent(events, normalized)
}

describe('event store flow (no page refresh)', () => {
  it('appends replay fixture event to feed', () => {
    let events = []
    events = applyWsMessage(events, REPLAY_FIXTURE)

    expect(events).toHaveLength(1)
    expect(events[0].eventType).toBe('PERSON_ENTER')
  })

  it('appends YOLO detection event without replacing replay event', () => {
    let events = applyWsMessage([], REPLAY_FIXTURE)
    events = applyWsMessage(events, YOLO_DETECTION)

    expect(events).toHaveLength(2)
    expect(events.map((item) => item.eventType)).toEqual(['PERSON_COUNT', 'PERSON_ENTER'])
  })

  it('updates counters when new events arrive', () => {
    const today = '2026-06-20'
    let events = applyWsMessage([], REPLAY_FIXTURE)
    events = applyWsMessage(events, YOLO_DETECTION)

    const metrics = computeEventMetrics(events, [{ status: 'online' }], today)

    expect(metrics.openEvents).toBe(2)
    expect(metrics.criticalEvents).toBe(0)
    expect(metrics.totalEventsToday).toBe(2)
    expect(metrics.onlineCameras).toBe(1)
  })

  it('deduplicates event.updated without growing the list', () => {
    let events = applyWsMessage([], YOLO_DETECTION)
    events = applyWsMessage(events, {
      type: 'event.updated',
      payload: {
        event: {
          ...YOLO_DETECTION.payload.event,
          status: 'RESOLVED',
        },
      },
    })

    expect(events).toHaveLength(1)
    expect(events[0].status).toBe('resolved')
    expect(computeEventMetrics(events, [], '2026-06-20').openEvents).toBe(0)
  })
})
