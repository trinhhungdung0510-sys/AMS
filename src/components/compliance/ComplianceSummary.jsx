function ComplianceSummary({ summary, loading }) {
  const cards = [
    { label: 'Tổng vi phạm', value: summary?.total ?? 0 },
    { label: 'Sai đồng phục', value: summary?.uniform_violation ?? 0 },
    { label: 'Xâm nhập vùng cấm', value: summary?.zone_intrusion ?? 0 },
    { label: 'Vi phạm quy trình', value: summary?.biosecurity_process_violation ?? 0 },
    { label: 'Động vật xâm nhập', value: summary?.animal_intrusion ?? 0 },
    { label: 'Xe vi phạm', value: summary?.vehicle_intrusion ?? 0 },
  ]

  return (
    <section className="compliance-summary">
      <div className="compliance-summary__head">
        <strong>Hôm nay</strong>
        <span>{summary?.date || new Date().toISOString().slice(0, 10)}</span>
      </div>
      <div className="compliance-summary__grid">
        {cards.map((card) => (
          <div key={card.label} className="compliance-summary__item">
            <span>{card.label}</span>
            <strong>{loading ? '…' : card.value}</strong>
          </div>
        ))}
      </div>
    </section>
  )
}

export default ComplianceSummary
