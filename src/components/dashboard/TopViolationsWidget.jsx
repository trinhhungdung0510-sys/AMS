import { SEVERITY_LABELS } from '../../data/eventCatalog'

function TopViolationsWidget({ items, loading }) {
  return (
    <article className="panel panel--compact">
      <div className="panel__header">
        <div>
          <h2>Top vi phạm</h2>
          <p>7 ngày gần nhất</p>
        </div>
      </div>
      <div className="rank-list">
        {loading ? (
          <p className="crossing-list__empty">Đang tải…</p>
        ) : !items?.length ? (
          <p className="crossing-list__empty">Chưa có vi phạm trong 7 ngày qua.</p>
        ) : (
          items.map((item, index) => (
            <div key={item.eventType} className="rank-item">
              <span className="rank-item__index">{index + 1}</span>
              <div>
                <strong>{item.title || item.eventType}</strong>
                <p>
                  {item.classification} · {SEVERITY_LABELS[item.severity] || item.severity}
                </p>
              </div>
              <span>{item.count} lần</span>
            </div>
          ))
        )}
      </div>
    </article>
  )
}

export default TopViolationsWidget
