import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { DEFAULT_RULE_FORM, RULE_SEVERITIES, RULE_TYPES } from '../../config/rules'
import { getZones } from '../../services/zoneService'
import {
  createRule,
  deleteRule,
  getRules,
  toggleRule,
  updateRule,
} from '../../services/ruleService'
import { triggerRule } from '../../services/mockRuleEngine'
import RuleList from './RuleList'

function RuleEditor({ cameraId, onEventCreated }) {
  const mountedRef = useRef(true)
  const [rules, setRules] = useState([])
  const [zones, setZones] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [testingRuleId, setTestingRuleId] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [editingRuleId, setEditingRuleId] = useState(null)
  const [form, setForm] = useState(DEFAULT_RULE_FORM)

  const zoneMap = useMemo(
    () => Object.fromEntries(zones.map((zone) => [zone.id, zone])),
    [zones],
  )

  const zoneOptions = useMemo(() => {
    const roots = zones.filter((zone) => !zone.parent_zone_id)
    const options = []
    roots.forEach((root) => {
      options.push({ value: root.id, label: root.name })
      zones
        .filter((zone) => zone.parent_zone_id === root.id)
        .forEach((sub) => options.push({ value: sub.id, label: `— ${sub.name}` }))
    })
    zones
      .filter((zone) => zone.parent_zone_id && !roots.find((root) => root.id === zone.parent_zone_id))
      .forEach((zone) => options.push({ value: zone.id, label: zone.name }))
    return options
  }, [zones])

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
      const [rulesData, zonesData] = await Promise.all([
        getRules(cameraId),
        getZones(cameraId),
      ])
      if (!mountedRef.current) return
      setRules(rulesData)
      setZones(zonesData)
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

  const resetForm = () => {
    setEditingRuleId(null)
    setForm({ ...DEFAULT_RULE_FORM, zone_id: zoneOptions[0]?.value || '' })
    setSuccess('')
  }

  useEffect(() => {
    if (!editingRuleId && zoneOptions.length > 0 && !form.zone_id) {
      setForm((current) => ({ ...current, zone_id: zoneOptions[0].value }))
    }
  }, [zoneOptions, editingRuleId, form.zone_id])

  const validateForm = () => {
    if (!form.name.trim()) return 'Tên rule không được để trống'
    if (!form.zone_id) return 'Chọn zone gắn với rule'
    if (!form.rule_type) return 'Chọn loại rule'
    if (!form.severity) return 'Chọn mức độ nghiêm trọng'
    if (form.cooldown_seconds < 0) return 'Cooldown phải >= 0'
    return ''
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const validationError = validateForm()
    if (validationError) {
      setError(validationError)
      return
    }

    setSaving(true)
    setError('')
    setSuccess('')

    const payload = {
      name: form.name.trim(),
      description: form.description.trim() || null,
      zone_id: form.zone_id,
      rule_type: form.rule_type,
      severity: form.severity,
      enabled: form.enabled,
      cooldown_seconds: Number(form.cooldown_seconds),
      config: form.config || {},
    }

    try {
      if (editingRuleId) {
        const updated = await updateRule(editingRuleId, payload)
        if (!mountedRef.current) return
        setRules((current) => current.map((rule) => (rule.id === updated.id ? updated : rule)))
        setSuccess('Đã cập nhật rule')
      } else {
        const created = await createRule(cameraId, payload)
        if (!mountedRef.current) return
        setRules((current) => [created, ...current])
        setSuccess('Đã tạo rule mới')
      }
      resetForm()
    } catch (saveError) {
      if (!mountedRef.current) return
      setError(saveError.message)
    } finally {
      if (mountedRef.current) setSaving(false)
    }
  }

  const handleEdit = (rule) => {
    setEditingRuleId(rule.id)
    setForm({
      name: rule.name,
      description: rule.description || '',
      zone_id: rule.zone_id,
      rule_type: rule.rule_type,
      severity: rule.severity,
      enabled: rule.enabled,
      cooldown_seconds: rule.cooldown_seconds,
      config: rule.config || {},
    })
    setError('')
    setSuccess('')
  }

  const handleDelete = async (ruleId) => {
    if (!window.confirm('Xóa rule này?')) return
    try {
      await deleteRule(ruleId)
      if (!mountedRef.current) return
      setRules((current) => current.filter((rule) => rule.id !== ruleId))
      if (editingRuleId === ruleId) resetForm()
    } catch (deleteError) {
      if (!mountedRef.current) return
      setError(deleteError.message)
    }
  }

  const handleToggle = async (rule) => {
    try {
      const result = await toggleRule(rule.id)
      if (!mountedRef.current) return
      setRules((current) => current.map((item) => (
        item.id === rule.id ? { ...item, enabled: result.enabled } : item
      )))
    } catch (toggleError) {
      if (!mountedRef.current) return
      setError(toggleError.message)
    }
  }

  const handleTest = async (rule) => {
    setTestingRuleId(rule.id)
    setError('')
    setSuccess('')

    try {
      const event = await triggerRule(rule.id)
      if (!mountedRef.current) return
      setSuccess(`Đã sinh event ${event.id}`)
      onEventCreated?.(event)
    } catch (testError) {
      if (!mountedRef.current) return
      setError(testError.message)
    } finally {
      if (mountedRef.current) setTestingRuleId(null)
    }
  }

  return (
    <section className="rule-manager">
      <div className="rule-manager__layout">
        <form className="rule-manager__form panel panel--compact" onSubmit={handleSubmit}>
          <div className="panel__header">
            <h3 className="panel__title">{editingRuleId ? 'Chỉnh sửa Rule' : 'Tạo Rule mới'}</h3>
          </div>

          {error ? <div className="rule-manager__error">{error}</div> : null}
          {success ? <div className="rule-manager__success">{success}</div> : null}

          <label>
            <span>Tên Rule *</span>
            <input
              className="settings-form__input"
              value={form.name}
              onChange={(e) => setForm((current) => ({ ...current, name: e.target.value }))}
              required
            />
          </label>

          <label>
            <span>Mô tả</span>
            <textarea
              className="settings-form__input"
              rows={2}
              value={form.description}
              onChange={(e) => setForm((current) => ({ ...current, description: e.target.value }))}
            />
          </label>

          <label>
            <span>Zone *</span>
            <select
              className="settings-form__input"
              value={form.zone_id}
              onChange={(e) => setForm((current) => ({ ...current, zone_id: e.target.value }))}
              required
            >
              <option value="">— Chọn zone —</option>
              {zoneOptions.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>

          <label>
            <span>Rule Type *</span>
            <select
              className="settings-form__input"
              value={form.rule_type}
              onChange={(e) => setForm((current) => ({ ...current, rule_type: e.target.value }))}
            >
              {RULE_TYPES.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>

          <label>
            <span>Severity *</span>
            <select
              className="settings-form__input"
              value={form.severity}
              onChange={(e) => setForm((current) => ({ ...current, severity: e.target.value }))}
            >
              {RULE_SEVERITIES.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>

          <label>
            <span>Cooldown (seconds)</span>
            <input
              type="number"
              min={0}
              max={86400}
              className="settings-form__input"
              value={form.cooldown_seconds}
              onChange={(e) => setForm((current) => ({
                ...current,
                cooldown_seconds: Number(e.target.value),
              }))}
            />
          </label>

          {form.rule_type === 'PERSON_COUNT' ? (
            <label>
              <span>Max Persons (config.maxPersons)</span>
              <input
                type="number"
                min={1}
                className="settings-form__input"
                value={form.config?.maxPersons ?? 2}
                onChange={(e) => setForm((current) => ({
                  ...current,
                  config: { ...current.config, maxPersons: Number(e.target.value) },
                }))}
              />
            </label>
          ) : null}

          {form.rule_type === 'PPE_REQUIRED' ? (
            <fieldset className="rule-manager__config">
              <legend>Required PPE</legend>
              {['helmet', 'mask', 'coverall'].map((item) => (
                <label key={item} className="rule-manager__checkbox">
                  <input
                    type="checkbox"
                    checked={(form.config?.requiredPPE || []).includes(item)}
                    onChange={(e) => {
                      const current = form.config?.requiredPPE || []
                      const next = e.target.checked
                        ? [...current, item]
                        : current.filter((value) => value !== item)
                      setForm((prev) => ({
                        ...prev,
                        config: { ...prev.config, requiredPPE: next },
                      }))
                    }}
                  />
                  <span>{item}</span>
                </label>
              ))}
            </fieldset>
          ) : null}

          <label className="rule-manager__checkbox">
            <input
              type="checkbox"
              checked={form.enabled}
              onChange={(e) => setForm((current) => ({ ...current, enabled: e.target.checked }))}
            />
            <span>Enabled</span>
          </label>

          <div className="rule-manager__form-actions">
            <button type="submit" className="btn btn--primary" disabled={saving || loading}>
              {saving ? 'Đang lưu...' : editingRuleId ? 'Cập nhật Rule' : 'Tạo Rule'}
            </button>
            {editingRuleId ? (
              <button type="button" className="btn btn--outline" onClick={resetForm} disabled={saving}>
                Hủy
              </button>
            ) : null}
          </div>
        </form>

        <div className="rule-manager__list-wrap">
          <RuleList
            rules={rules}
            zoneMap={zoneMap}
            loading={loading}
            testingRuleId={testingRuleId}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onToggle={handleToggle}
            onTest={handleTest}
          />
        </div>
      </div>
    </section>
  )
}

export default RuleEditor
