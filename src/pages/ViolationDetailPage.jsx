import { useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  ArrowLeft,
  Bell,
  Check,
  CheckCircle2,
  Download,
  FileText,
  SkipForward,
} from 'lucide-react'
import AtshViolationSnapshot from '../components/AtshViolationSnapshot'
import {
  ATSH_SEVERITY,
  ATSH_STATUS,
  VI_PHAM_ATSH_ROUTE,
  atshViolations,
  getViolationById,
  getViolationTimeline,
} from '../data/atshViolations'
import { exportRowsAsExcel, formatDateTime } from '../utils/formatters'

function ViolationDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const base = getViolationById(id)
  const [violation, setViolation] = useState(base ?? atshViolations[0])
  const [notice, setNotice] = useState('')
  const timeline = useMemo(() => getViolationTimeline(violation), [violation])

  if (!base && !atshViolations.length) {
    return (
      <div className="atsh-detail atsh-detail--empty panel">
        <p>Không tìm thấy vi phạm.</p>
        <Link to={VI_PHAM_ATSH_ROUTE} className="btn btn--outline">Quay lại</Link>
      </div>
    )
  }

  const severity = ATSH_SEVERITY[violation.severity] || ATSH_SEVERITY.WARNING

  const updateStatus = (status) => {
    setViolation((prev) => ({
      ...prev,
      status,
      handler: status === 'new' ? 'Chưa phân công' : 'Trần Bảo Long',
    }))
    setNotice(`Trạng thái: ${ATSH_STATUS[status]}`)
  }

  const generateReport = () => {
    exportRowsAsExcel(
      `bao-cao-vi-pham-${violation.id}.xls`,
      [{
        ID: violation.id,
        Camera: violation.cameraName,
        'Khu vực': violation.zone,
        'Loại vi phạm': violation.typeLabel,
        'Độ tin cậy': `${violation.confidence}%`,
        'Mức độ': severity.label,
        'Thời gian': formatDateTime(violation.date, violation.time),
        'Mô tả': violation.description,
        'Trạng thái': ATSH_STATUS[violation.status],
      }],
    )
    setNotice('Đã tạo báo cáo Excel')
  }

  const sendNotification = () => {
    setNotice(`Đã gửi cảnh báo · ${violation.typeLabel} · ${violation.cameraName}`)
  }

  const exportPdf = () => window.print()

  return (
    <div className="atsh-detail">
      <header className="atsh-detail__top">
        <button type="button" className="btn btn--ghost atsh-detail__back" onClick={() => navigate(VI_PHAM_ATSH_ROUTE)}>
          <ArrowLeft size={16} /> Trung tâm vi phạm ATSH
        </button>
        <div className="atsh-detail__actions">
          <button type="button" className="btn btn--outline" onClick={() => updateStatus('confirmed')}>
            <Check size={16} /> Xác nhận
          </button>
          <button type="button" className="btn btn--outline" onClick={() => updateStatus('resolved')}>
            <CheckCircle2 size={16} /> Đã xử lý
          </button>
          <button type="button" className="btn btn--outline" onClick={() => updateStatus('dismissed')}>
            <SkipForward size={16} /> Bỏ qua
          </button>
          <button type="button" className="btn btn--primary" onClick={generateReport}>
            <FileText size={16} /> Tạo báo cáo
          </button>
          <button type="button" className="btn btn--outline" onClick={sendNotification}>
            <Bell size={16} /> Gửi cảnh báo
          </button>
          <button type="button" className="btn btn--outline" onClick={exportPdf}>
            <Download size={16} /> PDF
          </button>
        </div>
      </header>

      {notice && <div className="atsh-detail__notice panel">{notice}</div>}

      <div className="atsh-detail__layout">
        <section className="atsh-detail__visual panel">
          <AtshViolationSnapshot violation={violation} large showMeta />
          <div className="atsh-detail__visual-meta">
            <span className={`atsh-severity atsh-severity--${severity.tone}`}>{severity.label}</span>
            <strong>{violation.typeLabel}</strong>
            <span>{formatDateTime(violation.date, violation.time)}</span>
          </div>
        </section>

        <aside className="atsh-detail__info panel">
          <h2>Chi tiết vi phạm</h2>
          <dl className="atsh-info-list">
            <div><dt>Tên camera</dt><dd>{violation.cameraName}</dd></div>
            <div><dt>Khu vực</dt><dd>{violation.zone}</dd></div>
            <div><dt>Loại vi phạm</dt><dd>{violation.typeLabel}</dd></div>
            <div><dt>Độ tin cậy</dt><dd>{violation.confidence}%</dd></div>
            <div><dt>Thời gian</dt><dd>{formatDateTime(violation.date, violation.time)}</dd></div>
            <div><dt>Mức độ</dt><dd><span className={`atsh-severity atsh-severity--${severity.tone}`}>{severity.label}</span></dd></div>
            <div><dt>Trạng thái</dt><dd><span className={`atsh-status atsh-status--${violation.status}`}>{ATSH_STATUS[violation.status]}</span></dd></div>
            <div><dt>Người xử lý</dt><dd>{violation.handler}</dd></div>
          </dl>

          <div className="atsh-detail__description">
            <h3>Mô tả</h3>
            <p>{violation.description}</p>
          </div>
        </aside>

        <section className="atsh-detail__timeline panel">
          <h2>Timeline ATSH</h2>
          <p className="atsh-detail__timeline-sub">Sự kiện theo thời gian · {violation.date}</p>
          <div className="atsh-timeline">
            {timeline.map((item) => {
              const active = item.id === violation.id
              const itemSeverity = ATSH_SEVERITY[item.severity] || ATSH_SEVERITY.WARNING
              return (
                <Link
                  key={item.id}
                  to={`${VI_PHAM_ATSH_ROUTE}/${item.id}`}
                  className={`atsh-timeline__item${active ? ' atsh-timeline__item--active' : ''}`}
                >
                  <span className="atsh-timeline__time">{item.time}</span>
                  <span className={`atsh-timeline__dot atsh-timeline__dot--${itemSeverity.tone}`} />
                  <div>
                    <strong>{item.typeLabel}</strong>
                    <small>{item.cameraName} · {item.zone} · {item.confidence}%</small>
                  </div>
                </Link>
              )
            })}
          </div>
        </section>
      </div>
    </div>
  )
}

export default ViolationDetailPage
