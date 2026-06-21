import { ShieldAlert, PawPrint, Truck, Gauge } from 'lucide-react'

function ComplianceKpiWidgets({ kpis, loading }) {
  const cards = [
    {
      label: 'Tổng vi phạm hôm nay',
      value: kpis?.totalViolationsToday ?? 0,
      icon: ShieldAlert,
      tone: 'orange',
    },
    {
      label: 'Vi phạm an toàn sinh học',
      value: kpis?.biosecurityViolations ?? 0,
      icon: ShieldAlert,
      tone: 'red',
    },
    {
      label: 'Vi phạm động vật',
      value: kpis?.animalViolations ?? 0,
      icon: PawPrint,
      tone: 'amber',
    },
    {
      label: 'Vi phạm phương tiện',
      value: kpis?.vehicleViolations ?? 0,
      icon: Truck,
      tone: 'blue',
    },
    {
      label: 'Mức tuân thủ',
      value: `${kpis?.complianceScore ?? 0}%`,
      icon: Gauge,
      tone: 'green',
    },
  ]

  return (
    <section className="compliance-kpi-grid">
      {cards.map((card) => (
        <article key={card.label} className={`metric-card metric-card--${card.tone}`}>
          <div>
            <span className="metric-card__label">{card.label}</span>
            <strong>{loading ? '…' : card.value}</strong>
          </div>
          <span className="metric-card__icon">
            <card.icon size={22} />
          </span>
        </article>
      ))}
    </section>
  )
}

export default ComplianceKpiWidgets
