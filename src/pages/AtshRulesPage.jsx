import { useEffect, useState } from 'react'
import { RefreshCw } from 'lucide-react'
import {
  ATSH_RULE_SEVERITY,
  DEFAULT_ATSH_RULES,
  mergeRules,
} from '../data/atshRules'

const API_BASE_URL = 'http://127.0.0.1:8000'

function AtshRulesPage() {
  const [rules, setRules] = useState(DEFAULT_ATSH_RULES)
  const [selectedId, setSelectedId] = useState(DEFAULT_ATSH_RULES[0].id)
  const [status, setStatus] = useState('Sẵn sàng')

  const selected = rules.find((item) => item.id === selectedId) || rules[0]
  const severity = ATSH_RULE_SEVERITY[selected?.severity] || ATSH_RULE_SEVERITY.WARNING

  const loadRules = async () => {
    try {
      setStatus('Đang tải quy tắc...')
      const response = await fetch(`${API_BASE_URL}/api/biosecurity-rules`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      const merged = mergeRules(data)
      setRules(merged)
      setSelectedId(merged[0]?.id ?? DEFAULT_ATSH_RULES[0].id)
      setStatus(`${merged.length} quy tắc ATSH`)
    } catch {
      setRules(DEFAULT_ATSH_RULES)
      setStatus('Dùng danh sách quy tắc mặc định')
    }
  }

  useEffect(() => {
    loadRules()
  }, [])

  const toggleRule = async (rule) => {
    const nextEnabled = !rule.enabled
    setRules((prev) => prev.map((item) =>
      item.id === rule.id ? { ...item, enabled: nextEnabled } : item,
    ))

    if (!rule.fromApi) {
      setStatus(nextEnabled ? `Đã bật: ${rule.name}` : `Đã tắt: ${rule.name}`)
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/biosecurity-rules/${rule.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled: nextEnabled }),
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      setStatus(nextEnabled ? `Đã bật: ${rule.name}` : `Đã tắt: ${rule.name}`)
    } catch (error) {
      setRules((prev) => prev.map((item) =>
        item.id === rule.id ? { ...item, enabled: rule.enabled } : item,
      ))
      setStatus(`Không cập nhật được: ${error.message}`)
    }
  }

  return (
    <div className="atsh-rules">
      <header className="atsh-rules__hero">
        <div>
          <h1>Quy tắc ATSH</h1>
          <p>Danh sách quy tắc an toàn sinh học — bật hoặc tắt theo nhu cầu trại.</p>
        </div>
        <button type="button" className="btn btn--outline" onClick={loadRules}>
          <RefreshCw size={16} /> Tải lại
        </button>
      </header>

      <p className="atsh-rules__status">{status}</p>

      <div className="atsh-rules__layout">
        <section className="atsh-rules__list panel">
          <h2>Danh sách quy tắc</h2>
          <ul>
            {rules.map((rule) => {
              const ruleSeverity = ATSH_RULE_SEVERITY[rule.severity] || ATSH_RULE_SEVERITY.WARNING
              return (
                <li key={rule.id}>
                  <button
                    type="button"
                    className={`atsh-rule-item${selectedId === rule.id ? ' atsh-rule-item--active' : ''}`}
                    onClick={() => setSelectedId(rule.id)}
                  >
                    <span className={`atsh-rule-item__dot atsh-rule-item__dot--${ruleSeverity.tone}`} />
                    <span>
                      <strong>{rule.name}</strong>
                      <small>{rule.enabled ? 'Đang bật' : 'Đang tắt'}</small>
                    </span>
                  </button>
                </li>
              )
            })}
          </ul>
        </section>

        <aside className="atsh-rules__detail panel">
          <h2>Thông tin quy tắc</h2>

          <dl className="atsh-rules-info">
            <div>
              <dt>Tên quy tắc</dt>
              <dd>{selected.name}</dd>
            </div>
            <div>
              <dt>Mô tả</dt>
              <dd>{selected.description}</dd>
            </div>
            <div>
              <dt>Mức độ</dt>
              <dd>
                <span className={`atsh-severity atsh-severity--${severity.tone}`}>{severity.label}</span>
              </dd>
            </div>
            <div>
              <dt>Khu vực áp dụng</dt>
              <dd>
                <div className="atsh-rules-zones">
                  {selected.zones.map((zone) => (
                    <span key={zone} className="atsh-rules-zone-chip">{zone}</span>
                  ))}
                </div>
              </dd>
            </div>
          </dl>

          <div className="atsh-rules-toggle">
            <span>Cho phép</span>
            <div className="atsh-rules-toggle__actions">
              <button
                type="button"
                className={`atsh-toggle-btn${selected.enabled ? ' atsh-toggle-btn--active' : ''}`}
                onClick={() => !selected.enabled && toggleRule(selected)}
              >
                Bật
              </button>
              <button
                type="button"
                className={`atsh-toggle-btn${!selected.enabled ? ' atsh-toggle-btn--active' : ''}`}
                onClick={() => selected.enabled && toggleRule(selected)}
              >
                Tắt
              </button>
            </div>
          </div>

          <div className="atsh-rules-legend">
            <span><i className="atsh-rule-item__dot atsh-rule-item__dot--info" /> Thông tin</span>
            <span><i className="atsh-rule-item__dot atsh-rule-item__dot--warning" /> Cảnh báo</span>
            <span><i className="atsh-rule-item__dot atsh-rule-item__dot--critical" /> Nghiêm trọng</span>
          </div>
        </aside>
      </div>
    </div>
  )
}

export default AtshRulesPage
