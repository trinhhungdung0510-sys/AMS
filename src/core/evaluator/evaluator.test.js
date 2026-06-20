import { describe, expect, it, beforeEach } from 'vitest'
import { EvaluatorEngine } from './EvaluatorEngine'
import {
  PersonCountEvaluator,
  PersonDwellEvaluator,
  PersonEnterEvaluator,
} from './RuleEvaluator'
import { TrackStore } from '../tracking/TrackStore'
import { StateEngine } from '../runtime/StateEngine'
import { syncRuntimeFromObservation } from '../runtime/syncRuntime'

const zone = { id: 'CZ-1', name: 'Main' }
const ruleEnter = {
  id: 'ZR-ENTER',
  rule_type: 'PERSON_ENTER',
  severity: 'MEDIUM',
  enabled: true,
  zone_id: 'CZ-1',
}
const ruleCount = {
  id: 'ZR-COUNT',
  rule_type: 'PERSON_COUNT',
  severity: 'HIGH',
  enabled: true,
  zone_id: 'CZ-1',
  config: { maxPersons: 2 },
}
const ruleDwell = {
  id: 'ZR-DWELL',
  rule_type: 'PERSON_DWELL',
  severity: 'HIGH',
  enabled: true,
  zone_id: 'CZ-1',
  config: { minDwellSeconds: 30 },
}

function buildObservation(objects, timestamp = '2026-06-22T10:00:00Z') {
  return {
    id: 'OBS-1',
    camera_id: 'CAM-1',
    timestamp,
    objects,
  }
}

describe('PersonEnterEvaluator (track + state context)', () => {
  const evaluator = new PersonEnterEvaluator()

  it('fires once per track per zone using state', () => {
    const track = {
      trackId: 'T-1',
      cameraId: 'CAM-1',
      class: 'person',
      firstSeenAt: '2026-06-22T10:00:00Z',
      currentZoneId: 'CZ-1',
    }
    const objectItem = {
      trackId: 'T-1',
      class: 'person',
      confidence: 0.9,
      bbox: { x: 0.1, y: 0.1, width: 0.1, height: 0.2 },
    }
    const context = {
      track,
      state: {},
      observation: buildObservation([objectItem]),
      rule: ruleEnter,
      zone,
      zoneMapping: { objectId: 'T-1', zones: ['CZ-1'], subzones: [] },
      object: objectItem,
      tracksInZone: [],
      stateEngine: null,
    }

    const first = evaluator.evaluate(context)
    expect(first).toHaveLength(1)

    const second = evaluator.evaluate({
      ...context,
      state: { ruleStates: { 'ZR-ENTER': { enterTriggered: true, zoneId: 'CZ-1' } } },
    })
    expect(second).toHaveLength(0)
  })
})

describe('PersonCountEvaluator (zone context)', () => {
  const evaluator = new PersonCountEvaluator()

  it('creates violation when person count exceeds maxPersons', () => {
    const hits = evaluator.evaluate({
      track: null,
      state: {},
      observation: buildObservation([]),
      rule: ruleCount,
      zone,
      zoneMapping: null,
      object: null,
      tracksInZone: [
        { trackId: 'A', class: 'person', metadata: { confidence: 0.9 } },
        { trackId: 'B', class: 'person', metadata: { confidence: 0.85 } },
        { trackId: 'C', class: 'person', metadata: { confidence: 0.8 } },
      ],
      stateEngine: null,
    })

    expect(hits).toHaveLength(1)
    expect(hits[0].metadata.personCount).toBe(3)
  })
})

describe('PersonDwellEvaluator', () => {
  const evaluator = new PersonDwellEvaluator()
  let stateEngine

  beforeEach(() => {
    stateEngine = new StateEngine()
  })

  it('fires after min dwell seconds', () => {
    stateEngine.processTrackUpdate({
      track: {
        trackId: 'T-1',
        cameraId: 'CAM-1',
        currentZoneId: 'CZ-1',
      },
      previousTrack: null,
      timestamp: '2026-06-22T10:00:00Z',
      zones: [zone],
    })

    const track = {
      trackId: 'T-1',
      cameraId: 'CAM-1',
      class: 'person',
      currentZoneId: 'CZ-1',
    }
    const objectItem = {
      trackId: 'T-1',
      class: 'person',
      confidence: 0.92,
      bbox: { x: 0.1, y: 0.1, width: 0.1, height: 0.2 },
    }

    const tooEarly = evaluator.evaluate({
      track,
      state: stateEngine.getState('CAM-1', 'T-1'),
      observation: buildObservation([objectItem], '2026-06-22T10:00:10Z'),
      rule: ruleDwell,
      zone,
      zoneMapping: { objectId: 'T-1', zones: ['CZ-1'], subzones: [] },
      object: objectItem,
      tracksInZone: [],
      stateEngine,
    })
    expect(tooEarly).toHaveLength(0)

    const ready = evaluator.evaluate({
      track,
      state: stateEngine.getState('CAM-1', 'T-1'),
      observation: buildObservation([objectItem], '2026-06-22T10:00:35Z'),
      rule: ruleDwell,
      zone,
      zoneMapping: { objectId: 'T-1', zones: ['CZ-1'], subzones: [] },
      object: objectItem,
      tracksInZone: [],
      stateEngine,
    })
    expect(ready).toHaveLength(1)
    expect(ready[0].metadata.dwellSeconds).toBeGreaterThanOrEqual(30)
  })
})

describe('EvaluatorEngine runtime integration', () => {
  it('uses TrackStore and StateEngine during evaluation', () => {
    const trackStore = new TrackStore()
    const stateEngine = new StateEngine()
    const engine = new EvaluatorEngine([new PersonEnterEvaluator(), new PersonCountEvaluator()])

    const observation = buildObservation([
      { trackId: 'A', class: 'person', confidence: 0.9, bbox: { x: 0.1, y: 0.1, width: 0.1, height: 0.2 } },
      { trackId: 'B', class: 'person', confidence: 0.85, bbox: { x: 0.3, y: 0.1, width: 0.1, height: 0.2 } },
      { trackId: 'C', class: 'person', confidence: 0.8, bbox: { x: 0.5, y: 0.1, width: 0.1, height: 0.2 } },
    ])

    const zoneMappings = [
      { objectId: 'A', zones: ['CZ-1'], subzones: [] },
      { objectId: 'B', zones: ['CZ-1'], subzones: [] },
      { objectId: 'C', zones: ['CZ-1'], subzones: [] },
    ]

    syncRuntimeFromObservation({
      observation,
      zones: [zone],
      zoneMappings,
      trackStore,
      stateEngine,
    })

    const hits = engine.evaluate({
      observation,
      rules: [ruleEnter, ruleCount],
      zones: [zone],
      zoneMappings,
      trackStore,
      stateEngine,
    })

    expect(hits.some((hit) => hit.eventType === 'PERSON_ENTER')).toBe(true)
    expect(hits.some((hit) => hit.eventType === 'PERSON_COUNT')).toBe(true)
    expect(trackStore.getTracksByCamera('CAM-1')).toHaveLength(3)
  })
})
