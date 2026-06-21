import { useEffect, useState } from 'react'
import {
  exportConfigBundle,
  fetchDiagnostics,
  importConfigBundle,
  testComplianceRule,
  testZone,
} from '../services/deploymentService'
import { COMPLIANCE_EVENT_TYPE_OPTIONS } from '../data/complianceCenter'

function DiagnosticsPage() {
  const [diagnostics, setDiagnostics] = useState(null)
  const [zoneId, setZoneId] = useState('')
  const [zoneResult, setZoneResult] = useState(null)
  const [ruleType, setRuleType] = useState('UNIFORM_VIOLATION')
  const [ruleResult, setRuleResult] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchDiagnostics().then(setDiagnostics).catch(() => setDiagnostics(null))
  }, [])

  const handleZoneTest = async () => {
    try {
      setZoneResult(await testZone(zoneId))
    } catch (error) {
      setMessage(error.message)
    }
  }

  const handleRuleTest = async () => {
    try {
      setRuleResult(await testComplianceRule({ ruleType, trackId: 101, score: 0.72 }))
    } catch (error) {
      setMessage(error.message)
    }
  }

  const handleExport = async () => {
    try {
      const bundle = await exportConfigBundle()
      const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'ams-config-bundle.json'
      link.click()
      URL.revokeObjectURL(url)
      setMessage('Đã xuất cấu hình')
    } catch (error) {
      setMessage(error.message)
    }
  }

  const handleImport = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return
    try {
      const text = await file.text()
      const payload = JSON.parse(text)
      const result = await importConfigBundle(payload)
      setMessage(`Import OK: ${JSON.stringify(result.counts)}`)
    } catch (error) {
      setMessage(error.message)
    }
  }

  return (
    <div className="deployment-page">
      <header className="deployment-page__head">
        <h1>System Diagnostics</h1>
        <p>Disk, memory, CPU, network, camera reachability, test modes</p>
      </header>
      {message ? <p className="panel__meta">{message}</p> : null}

      <section className="panel">
        <h2>Diagnostics</h2>
        <pre className="deployment-pre">{JSON.stringify(diagnostics, null, 2)}</pre>
      </section>

      <section className="dashboard-grid dashboard-grid--lists">
        <article className="panel">
          <h2>Zone Test Mode</h2>
          <input className="settings-form__input" placeholder="Zone ID" value={zoneId} onChange={(e) => setZoneId(e.target.value)} />
          <button type="button" className="btn btn--primary" onClick={handleZoneTest}>Test Zone</button>
          {zoneResult ? (
            <div className="deployment-test-result">
              <strong>{zoneResult.zoneName}</strong>
              <p>Overlay points: {zoneResult.coordinates?.length ?? 0}</p>
              <pre className="deployment-pre">{JSON.stringify(zoneResult, null, 2)}</pre>
            </div>
          ) : null}
        </article>

        <article className="panel">
          <h2>Rule Test Mode</h2>
          <select className="settings-form__input" value={ruleType} onChange={(e) => setRuleType(e.target.value)}>
            {COMPLIANCE_EVENT_TYPE_OPTIONS.filter((item) => item.value !== 'all').map((item) => (
              <option key={item.value} value={item.value}>{item.label}</option>
            ))}
          </select>
          <button type="button" className="btn btn--primary" onClick={handleRuleTest}>Test Compliance Rule</button>
          {ruleResult ? (
            <div className="deployment-test-result">
              <p>Score: {ruleResult.output?.score} · Violated: {String(ruleResult.output?.violated)}</p>
              <pre className="deployment-pre">{JSON.stringify(ruleResult, null, 2)}</pre>
            </div>
          ) : null}
        </article>
      </section>

      <section className="panel">
        <h2>Export / Import Config</h2>
        <div className="settings-form__actions">
          <button type="button" className="btn btn--outline" onClick={handleExport}>Export Config Bundle</button>
          <label className="btn btn--primary">
            Import Config
            <input type="file" accept="application/json" hidden onChange={handleImport} />
          </label>
        </div>
      </section>
    </div>
  )
}

export default DiagnosticsPage
