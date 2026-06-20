export const OBJECT_CLASSES = [
  { value: 'PERSON', label: 'Người' },
  { value: 'ANIMAL', label: 'Động vật' },
  { value: 'VEHICLE', label: 'Phương tiện' },
]

export const OBSERVATION_SOURCES = [
  { value: 'MOCK', label: 'Mock' },
  { value: 'YOLO', label: 'YOLO' },
  { value: 'OPENVINO', label: 'OpenVINO' },
  { value: 'MANUAL', label: 'Manual' },
]

export function getObjectClassLabel(value) {
  return OBJECT_CLASSES.find((item) => item.value === value)?.label || value
}

export function getObservationSourceLabel(value) {
  return OBSERVATION_SOURCES.find((item) => item.value === value)?.label || value
}
