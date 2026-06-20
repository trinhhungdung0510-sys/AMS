import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { mapObservationToZones } from '../../core/zoneMapper'
import { runObservationPipeline } from '../../core/observationPipeline'
import { generateMockObservation, listMockScenarios } from '../../mock/mockDetector'
import { useRealtimeEvents } from '../../hooks/useRealtimeEvents'
import { listObservations } from '../../services/observationService'
import { getRules } from '../../services/ruleService'
import { getZones } from '../../services/zoneService'
import { formatDateTime } from '../../utils/formatters'

const SOURCE_LABELS = {
  MOCK: 'Mock',
  YOLO: 'YOLO',
  OPENVINO: 'OpenVINO',
  MANUAL: 'Manual',
}

function ObservationViewer({ cameraId, onEventsCreated }) {
  const mountedRef = useRef(true)
  const [observations, setObservations] = useState([])
  const [zones, setZones] = useState([])
  const [rules, setRules] = useState([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [selectedScenario, setSelectedScenario] = useState('one_person')

  const scenarios = useMemo(() => listMockScenarios(), [])

  const zoneMatchSummary = useMemo(() => {
    return observations.map((observation) => {
      const mappings = mapObservationToZones(observation, zones)
      const matchedZoneIds = [...new Set(mappings.flatMap((item) => [...item.zones, ...item.subzones]))]
      return {
        observationId: observation.id,
        matchedZoneIds,
      }
    })
  }, [observations, zones])

  const matchByObservationId = useMemo(
    () => Object.fromEntries(zoneMatchSummary.map((item) => [item.observationId, item.matchedZoneIds])),
    [zoneMatchSummary],
  )

  useEffect(() => {
    mountedRef.current = true
    return () => {
      mountedRef.current = false
    }
  }, [])

  const loadData = useCallback(async () => {
    if (!cameraId) return
    setLoading(true)
    setError('')

    try {
      const [observationData, zoneData, ruleData] = await Promise.all([
        listObservations(cameraId),
        getZones(cameraId),
        getRules(cameraId),
      ])
      if (!mountedRef.current) return
      setObservations(observationData)
      setZones(zoneData)
      setRules(ruleData)
    } catch (loadError) {
      if (!mountedRef.current) return
      setError(loadError.message)
    } finally {
      if (mountedRef.current) setLoading(false)
    }
  }, [cameraId])

  useEffect(() => {
    loadData()
  }, [loadData])

  useRealtimeEvents({
    filterCameraId: cameraId,
    eventTypes: ['observation.created', 'event.created'],
    onMessage: (payload) => {
      if (payload.type === 'observation.created') {
        const observation = payload.payload?.observation
        if (!observation) return
        setObservations((current) => [observation, ...current.filter((item) => item.id !== observation.id)])
      }
      if (payload.type === 'event.created') {
        onEventsCreated?.([payload.payload?.event].filter(Boolean))
      }
    },
  })

  const handleRunPipeline = async () => {
    setRunning(true)
    setError('')
    setSuccess('')

    try {
      const payload = generateMockObservation(cameraId, selectedScenario)
      const result = await runObservationPipeline({
        observationPayload: payload,
      })
      if (!mountedRef.current) return
      setObservations((current) => [result.observation, ...current.filter((item) => item.id !== result.observation.id)])
      setSuccess('Observation đã gửi — pipeline realtime qua EventBus')
    } catch (pipelineError) {
      if (!mountedRef.current) return
      setError(pipelineError.message)
    } finally {
      if (mountedRef.current) setRunning(false)
    }
  }

  return (
    <section className="observation-viewer">
      <div className="observation-viewer__toolbar panel panel--compact">
        <div className="panel__header">
          <h3 className="panel__title">Mock Detector → Pipeline</h3>
          <p className="panel__desc">Observation → Zone Mapper → Evaluator → Event</p>
        </div>

        {error ? <div className="rule-manager__error">{error}</div> : null}
        {success ? <div className="rule-manager__success">{success}</div> : null}

        <div className="observation-viewer__actions">
          <label>
            <span>Kịch bản mock</span>
            <select
              className="settings-form__input"
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
            >
              {scenarios.map((scenario) => (
                <option key={scenario.key} value={scenario.key}>{scenario.label}</option>
              ))}
            </select>
          </label>
          <button
            type="button"
            className="btn btn--primary"
            onClick={handleRunPipeline}
            disabled={running || loading}
          >
            {running ? 'Đang chạy pipeline...' : 'Chạy Mock Pipeline'}
          </button>
          <button type="button" className="btn btn--outline" onClick={loadData} disabled={loading}>
            Tải lại
          </button>
        </div>
      </div>

      <div className="panel">
        <div className="panel__header">
          <h3 className="panel__title">Observations</h3>
          <span className="panel__meta">{observations.length} bản ghi</span>
        </div>

        {loading ? <div className="violation-empty">Đang tải observations...</div> : null}

        {!loading && observations.length === 0 ? (
          <div className="violation-empty">Chưa có observation. Chạy Mock Pipeline để test.</div>
        ) : null}

        {!loading && observations.length > 0 ? (
          <div className="observation-table-wrap">
            <table className="observation-table">
              <thead>
                <tr>
                  <th>Thời gian</th>
                  <th>Source</th>
                  <th>Objects</th>
                  <th>Zones Matched</th>
                  <th>ID</th>
                </tr>
              </thead>
              <tbody>
                {observations.map((observation) => {
                  const matched = matchByObservationId[observation.id] || []
                  const zoneLabels = matched.map((zoneId) => {
                    const zone = zones.find((item) => item.id === zoneId)
                    return zone?.name || zoneId
                  })

                  return (
                    <tr key={observation.id}>
                      <td>{formatDateTime(observation.timestamp.slice(0, 10), observation.timestamp.slice(11, 19))}</td>
                      <td>{SOURCE_LABELS[observation.source] || observation.source}</td>
                      <td>{observation.objects?.length || 0}</td>
                      <td>{zoneLabels.length ? zoneLabels.join(', ') : '—'}</td>
                      <td><code>{observation.id}</code></td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : null}
      </div>
    </section>
  )
}

export default ObservationViewer
