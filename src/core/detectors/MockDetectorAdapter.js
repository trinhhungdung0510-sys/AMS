import { DetectorAdapter } from './DetectorAdapter'

const SCENARIOS = {
  one_person: {
    label: '1 người',
    objects: [
      {
        trackId: 'T-001',
        class: 'person',
        confidence: 0.94,
        bbox: { x: 0.35, y: 0.2, width: 0.12, height: 0.45 },
        attributes: { helmet: true, mask: true, coverall: true },
      },
    ],
  },
  three_persons: {
    label: '3 người',
    objects: [
      {
        trackId: 'T-101',
        class: 'person',
        confidence: 0.91,
        bbox: { x: 0.1, y: 0.25, width: 0.1, height: 0.4 },
        attributes: { helmet: true, mask: false, coverall: true },
      },
      {
        trackId: 'T-102',
        class: 'person',
        confidence: 0.88,
        bbox: { x: 0.35, y: 0.22, width: 0.11, height: 0.42 },
        attributes: { helmet: true, mask: true, coverall: true },
      },
      {
        trackId: 'T-103',
        class: 'person',
        confidence: 0.86,
        bbox: { x: 0.62, y: 0.28, width: 0.1, height: 0.38 },
        attributes: { helmet: false, mask: true, coverall: true },
      },
    ],
  },
  one_animal: {
    label: '1 động vật',
    objects: [
      {
        trackId: 'T-AN-01',
        class: 'animal',
        confidence: 0.89,
        bbox: { x: 0.45, y: 0.55, width: 0.18, height: 0.25 },
        attributes: {},
      },
    ],
  },
  ppe_violation: {
    label: 'Vi phạm PPE',
    objects: [
      {
        trackId: 'T-PPE-01',
        class: 'person',
        confidence: 0.93,
        bbox: { x: 0.4, y: 0.18, width: 0.14, height: 0.48 },
        attributes: { helmet: false, mask: false, coverall: true },
      },
    ],
  },
}

export function listMockScenarios() {
  return Object.entries(SCENARIOS).map(([key, value]) => ({
    key,
    label: value.label,
  }))
}

export class MockDetectorAdapter extends DetectorAdapter {
  constructor(scenarioKey = 'one_person') {
    super()
    this.scenarioKey = scenarioKey
  }

  get id() {
    return 'mock-detector-v1'
  }

  get source() {
    return 'MOCK'
  }

  detect({
    cameraId,
    frameWidth = 1920,
    frameHeight = 1080,
    scenarioKey = this.scenarioKey,
    timestamp = new Date().toISOString(),
  }) {
    const scenario = SCENARIOS[scenarioKey]
    if (!scenario) {
      throw new Error(`Unknown mock scenario: ${scenarioKey}`)
    }

    return {
      cameraId,
      timestamp,
      source: this.source,
      frameWidth,
      frameHeight,
      objects: scenario.objects.map((item) => ({ ...item })),
    }
  }
}

export const defaultMockDetectorAdapter = new MockDetectorAdapter()
