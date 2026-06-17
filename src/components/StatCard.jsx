function StatCard({ value, label, icon, variant = 'default' }) {
  return (
    <div className={`stat-card stat-card--${variant}`}>
      <div className="stat-card__icon">{icon}</div>
      <div className="stat-card__content">
        <span className="stat-card__value">{value}</span>
        <span className="stat-card__label">{label}</span>
      </div>
    </div>
  )
}

export default StatCard
