import RuleCard from './RuleCard'

function RuleList({
  rules,
  zoneMap,
  loading,
  testingRuleId,
  onEdit,
  onDelete,
  onToggle,
  onTest,
}) {
  if (loading) {
    return <div className="rule-list__loading">Đang tải rules...</div>
  }

  if (rules.length === 0) {
    return <p className="rule-list__empty">Chưa có rule nào. Tạo rule đầu tiên để bắt đầu.</p>
  }

  return (
    <div className="rule-list">
      {rules.map((rule) => (
        <RuleCard
          key={rule.id}
          rule={rule}
          zoneName={zoneMap[rule.zone_id]?.name}
          onEdit={onEdit}
          onDelete={onDelete}
          onToggle={onToggle}
          onTest={onTest}
          testing={testingRuleId === rule.id}
        />
      ))}
    </div>
  )
}

export default RuleList
