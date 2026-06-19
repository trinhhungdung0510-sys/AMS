import { useEffect, useState } from 'react'
import { Plus, RefreshCw, Save, Trash2 } from 'lucide-react'
import { API_BASE_URL } from '../config/api'

const defaultRule = {
  rule_name: 'Person Dirty Zone to Safe Zone without Disinfection Zone',
  object_type: 'person',
  from_zone: 'dirty_zone',
  to_zone: 'safe_zone',
  required_zone: 'disinfection_zone',
  severity: 'critical',
  enabled: true,
}

const objectTypes = ['person', 'vehicle', 'dog', 'cat', 'bird']
const zones = [
  'any_zone',
  'outside_zone',
  'dirty_zone',
  'safe_zone',
  'disinfection_zone',
  'vehicle_disinfection_zone',
  'production_zone',
  'restricted_zone',
  'feed_storage_zone',
  'parking_zone',
]
const severities = ['critical', 'high', 'warning']

function RuleManagementPage() {
  const [rules, setRules] = useState([])
  const [form, setForm] = useState(defaultRule)
  const [editingId, setEditingId] = useState(null)
  const [status, setStatus] = useState('Đang tải rules...')

  const loadRules = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/rules`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      setRules(data)
      setStatus(`Đã tải ${data.length} rules từ backend`)
    } catch (error) {
      setStatus(`Không tải được rules: ${error.message}`)
    }
  }

  useEffect(() => {
    loadRules()
  }, [])

  const updateForm = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const resetForm = () => {
    setEditingId(null)
    setForm(defaultRule)
  }

  const submitRule = async (event) => {
    event.preventDefault()
    const payload = {
      ...form,
      required_zone: form.required_zone === 'none' ? null : form.required_zone,
    }
    const url = editingId ? `${API_BASE_URL}/api/rules/${editingId}` : `${API_BASE_URL}/api/rules`
    const method = editingId ? 'PUT' : 'POST'

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      await loadRules()
      resetForm()
      setStatus(editingId ? 'Đã cập nhật rule' : 'Đã tạo rule mới')
    } catch (error) {
      setStatus(`Không lưu được rule: ${error.message}`)
    }
  }

  const editRule = (rule) => {
    setEditingId(rule.id)
    setForm({
      rule_name: rule.rule_name,
      object_type: rule.object_type,
      from_zone: rule.from_zone,
      to_zone: rule.to_zone,
      required_zone: rule.required_zone ?? 'none',
      severity: rule.severity,
      enabled: rule.enabled,
    })
  }

  const deleteRule = async (ruleId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/rules/${ruleId}`, { method: 'DELETE' })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      await loadRules()
      setStatus('Đã xóa rule')
    } catch (error) {
      setStatus(`Không xóa được rule: ${error.message}`)
    }
  }

  return (
    <div className="rule-page">
      <section className="panel">
        <div className="panel__header">
          <div>
            <h2>Rule Designer</h2>
            <p>{status}</p>
          </div>
          <button type="button" className="btn btn--outline" onClick={loadRules}>
            <RefreshCw size={16} /> Đồng bộ
          </button>
        </div>

        <form className="rule-form" onSubmit={submitRule}>
          <label className="rule-form__wide">
            <span>Rule name</span>
            <input value={form.rule_name} onChange={(event) => updateForm('rule_name', event.target.value)} />
          </label>
          <label>
            <span>Object type</span>
            <select value={form.object_type} onChange={(event) => updateForm('object_type', event.target.value)}>
              {objectTypes.map((type) => <option key={type} value={type}>{type}</option>)}
            </select>
          </label>
          <label>
            <span>From zone</span>
            <select value={form.from_zone} onChange={(event) => updateForm('from_zone', event.target.value)}>
              {zones.map((zone) => <option key={zone} value={zone}>{zone}</option>)}
            </select>
          </label>
          <label>
            <span>To zone</span>
            <select value={form.to_zone} onChange={(event) => updateForm('to_zone', event.target.value)}>
              {zones.filter((zone) => zone !== 'any_zone').map((zone) => <option key={zone} value={zone}>{zone}</option>)}
            </select>
          </label>
          <label>
            <span>Required zone</span>
            <select value={form.required_zone ?? 'none'} onChange={(event) => updateForm('required_zone', event.target.value)}>
              <option value="none">none</option>
              {zones.filter((zone) => zone !== 'any_zone').map((zone) => <option key={zone} value={zone}>{zone}</option>)}
            </select>
          </label>
          <label>
            <span>Severity</span>
            <select value={form.severity} onChange={(event) => updateForm('severity', event.target.value)}>
              {severities.map((severity) => <option key={severity} value={severity}>{severity}</option>)}
            </select>
          </label>
          <label className="rule-form__toggle">
            <span>Enabled</span>
            <input
              type="checkbox"
              checked={form.enabled}
              onChange={(event) => updateForm('enabled', event.target.checked)}
            />
          </label>
          <div className="rule-form__actions">
            <button type="button" className="btn btn--outline" onClick={resetForm}>Reset</button>
            <button type="submit" className="btn btn--primary">
              {editingId ? <Save size={16} /> : <Plus size={16} />}
              {editingId ? 'Cập nhật rule' : 'Tạo rule'}
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel__header">
          <div>
            <h2>Rule Management</h2>
            <p>Danh sách rule biosecurity đang cấu hình</p>
          </div>
        </div>
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Rule</th>
                <th>Object</th>
                <th>Flow</th>
                <th>Required</th>
                <th>Severity</th>
                <th>Enabled</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((rule) => (
                <tr key={rule.id}>
                  <td className="data-table__desc">{rule.rule_name}</td>
                  <td>{rule.object_type}</td>
                  <td className="data-table__mono">{rule.from_zone} → {rule.to_zone}</td>
                  <td>{rule.required_zone ?? 'none'}</td>
                  <td><span className={`badge badge--${rule.severity}`}>{rule.severity}</span></td>
                  <td>{rule.enabled ? 'On' : 'Off'}</td>
                  <td>
                    <div className="action-group">
                      <button type="button" className="btn btn--outline" onClick={() => editRule(rule)}>Sửa</button>
                      <button type="button" className="btn-icon btn-icon--danger" onClick={() => deleteRule(rule.id)} aria-label="Xóa rule">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default RuleManagementPage
