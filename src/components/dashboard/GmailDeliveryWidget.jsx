import { Link } from 'react-router-dom'
import { AlertTriangle, CheckCircle2, Clock3, Mail } from 'lucide-react'

function formatSentAt(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('vi-VN')
}

function GmailDeliveryWidget({ summary, loading }) {
  const gmail = summary?.gmail ?? {}
  const cards = [
    { label: 'Đã gửi hôm nay', value: gmail.sentToday ?? 0, icon: CheckCircle2, tone: 'green' },
    { label: 'Đang chờ', value: gmail.pending ?? 0, icon: Clock3, tone: 'amber' },
    { label: 'Lỗi hôm nay', value: gmail.errorsToday ?? 0, icon: AlertTriangle, tone: 'red' },
  ]

  return (
    <article className="panel panel--compact">
      <div className="panel__header">
        <div>
          <h2>Kênh thông báo</h2>
          <p>Gmail — cảnh báo vi phạm ATSH tự động</p>
        </div>
        <span className="panel__badge panel__badge--gmail">
          <Mail size={14} /> Gmail
        </span>
      </div>

      {!loading && !gmail.connected ? (
        <p className="gmail-delivery-widget__hint">
          Gmail chưa kết nối.{' '}
          <Link to="/settings" className="gmail-delivery-widget__link">
            Cấu hình trong Cài đặt
          </Link>
        </p>
      ) : null}

      <div className="gmail-delivery-grid">
        {cards.map((card) => (
          <div key={card.label} className={`gmail-delivery-item gmail-delivery-item--${card.tone}`}>
            <card.icon size={18} />
            <div>
              <strong>{loading ? '…' : card.value}</strong>
              <span>{card.label}</span>
            </div>
          </div>
        ))}
      </div>

      <p className="gmail-delivery-widget__meta">
        <strong>Lần gửi cuối:</strong> {loading ? '…' : formatSentAt(gmail.lastSentAt)}
        {!loading && gmail.lastStatus ? (
          <span className={`gmail-delivery-widget__status gmail-delivery-widget__status--${gmail.lastStatus}`}>
            {gmail.lastStatus === 'success' ? ' ✓ Thành công' : ' ✗ Lỗi'}
          </span>
        ) : null}
      </p>
    </article>
  )
}

export default GmailDeliveryWidget
