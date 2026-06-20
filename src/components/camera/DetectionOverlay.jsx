import { useCallback, useEffect, useRef, useState } from 'react'
import {
  bboxToScreen,
  DEMO_DETECTION,
  formatConfidence,
  formatDetectionLabel,
  getDetectionColor,
} from '../../utils/detectionCoordinates'
import { createCameraDetection, getCameraDetections } from '../../services/aiDetectionService'

function DetectionOverlay({ cameraId, snapshotUrl }) {
  const containerRef = useRef(null)
  const [detections, setDetections] = useState([])
  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 })
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState('')

  const updateCanvasSize = useCallback(() => {
    const node = containerRef.current
    if (!node) return
    const rect = node.getBoundingClientRect()
    setCanvasSize({ width: rect.width, height: rect.height })
  }, [])

  const loadDetections = useCallback(async () => {
    if (!cameraId) return

    setLoading(true)
    setError('')

    try {
      const data = await getCameraDetections(cameraId)
      setDetections(data)
    } catch (loadError) {
      setError(loadError.message)
    } finally {
      setLoading(false)
    }
  }, [cameraId])

  useEffect(() => {
    loadDetections()
  }, [loadDetections])

  useEffect(() => {
    updateCanvasSize()
    window.addEventListener('resize', updateCanvasSize)
    return () => window.removeEventListener('resize', updateCanvasSize)
  }, [updateCanvasSize, snapshotUrl])

  const handleGenerateDemo = async () => {
    setCreating(true)
    setError('')

    try {
      const created = await createCameraDetection(cameraId, DEMO_DETECTION)
      setDetections((current) => [created, ...current])
    } catch (createError) {
      setError(createError.message)
    } finally {
      setCreating(false)
    }
  }

  return (
    <section className="panel detection-overlay">
      <div className="panel__header">
        <div>
          <h2 className="panel__title">AI Overlay Engine v1.0</h2>
          <p className="panel__desc">Hiển thị phát hiện AI trên snapshot (bbox chuẩn hóa 0–1)</p>
        </div>
        <div className="detection-overlay__toolbar">
          <button
            type="button"
            className="btn btn--primary"
            onClick={handleGenerateDemo}
            disabled={creating || !snapshotUrl}
          >
            {creating ? 'Đang tạo...' : 'Generate Demo Detection'}
          </button>
        </div>
      </div>

      {error ? <div className="detection-overlay__error">{error}</div> : null}
      {loading ? <div className="detection-overlay__loading">Đang tải phát hiện...</div> : null}

      <div className="detection-overlay__layout">
        <div className="detection-overlay__canvas-wrap" ref={containerRef}>
          {snapshotUrl ? (
            <>
              <img
                src={snapshotUrl}
                alt="Camera snapshot with AI detections"
                className="detection-overlay__image"
                onLoad={updateCanvasSize}
              />
              {canvasSize.width > 0 ? (
                <svg
                  className="detection-overlay__svg"
                  viewBox={`0 0 ${canvasSize.width} ${canvasSize.height}`}
                  aria-hidden="true"
                >
                  {detections.map((detection) => {
                    const box = bboxToScreen(detection.bbox, canvasSize.width, canvasSize.height)
                    const color = getDetectionColor(detection.label)
                    const labelText = `${formatDetectionLabel(detection.label)} ${formatConfidence(detection.confidence)}`
                    const labelY = Math.max(16, box.y - 6)

                    return (
                      <g key={detection.id} className="detection-overlay__item">
                        <rect
                          x={box.x}
                          y={box.y}
                          width={box.width}
                          height={box.height}
                          fill="none"
                          stroke={color}
                          strokeWidth={2}
                        />
                        <rect
                          x={box.x}
                          y={labelY - 14}
                          width={Math.max(72, labelText.length * 7.2)}
                          height={18}
                          fill={color}
                          rx={4}
                        />
                        <text
                          x={box.x + 6}
                          y={labelY}
                          fill="#ffffff"
                          fontSize={11}
                          fontWeight="700"
                          letterSpacing="0.04em"
                        >
                          {labelText}
                        </text>
                      </g>
                    )
                  })}
                </svg>
              ) : null}
            </>
          ) : (
            <div className="detection-overlay__empty">Chụp snapshot trước khi hiển thị overlay AI.</div>
          )}
        </div>

        <aside className="detection-overlay__sidebar">
          <h3>Phát hiện ({detections.length})</h3>
          {detections.length === 0 ? (
            <p className="detection-overlay__list-empty">Chưa có phát hiện nào.</p>
          ) : (
            <ul className="detection-overlay__list">
              {detections.map((detection) => (
                <li key={detection.id} className="detection-overlay__list-item">
                  <span
                    className="detection-overlay__swatch"
                    style={{ backgroundColor: getDetectionColor(detection.label) }}
                  />
                  <span>
                    <strong>{formatDetectionLabel(detection.label)}</strong>
                    <small>{formatConfidence(detection.confidence)}</small>
                  </span>
                </li>
              ))}
            </ul>
          )}
        </aside>
      </div>
    </section>
  )
}

export default DetectionOverlay
