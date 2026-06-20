import { getRuleTypeLabel, getSeverityLabel, getSeverityTone } from '../../config/rules'

function RuleCard({ rule, zoneName, onEdit, onDelete, onToggle, onTest, testing }) {
  return (
    <article className={`rule-card${rule.enabled ? '' : ' rule-card--disabled'}`}>
      <header className="rule-card__header">
        <div>
          <h3 className="rule-card__title">{rule.name}</h3>
          <p className="rule-card__meta">{getRuleTypeLabel(rule.rule_type)} · {zoneName || rule.zone_id}</p>
        </div>
        <span className={`badge badge--${getSeverityTone(rule.severity)}`}>
          {getSeverityLabel(rule.severity)}
        </span>
      </header>

      {rule.description ? (
        <p className="rule-card__desc">{rule.description}</p>
      ) : null}

      <dl className="rule-card__stats">
        <div><dt>Cooldown</dt><dd>{rule.cooldown_seconds}s</dd></div>
        <div><dt>Trạng thái</dt><dd>{rule.enabled ? 'Enabled' : 'Disabled'}</dd></div>
      </dl>

      <div className="rule-card__actions">
        <button type="button" className="btn btn--primary" onClick={() => onTest(rule)} disabled={testing}>
          {testing ? 'Testing...' : 'Test Rule'}
        </button>
        <button type="button" className="btn btn--outline" onClick={() => onToggle(rule)}>
          {rule.enabled ? 'Disable' : 'Enable'}
        </button>
        <button type="button" className="btn btn--outline" onClick={() => onEdit(rule)}>Edit</button>
        <button type="button" className="btn btn--ghost" onClick={() => onDelete(rule.id)}>Delete</button>
      </div>
    </article>
  )
}

export default RuleCard
