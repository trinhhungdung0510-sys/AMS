import { useEffect, useMemo, useState } from 'react'
import { Activity, AlertTriangle, Camera, ShieldCheck } from 'lucide-react'
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { API_BASE_URL } from '../config/api'

const fallbackSummary = {
  diem_atsh: 92,
  vi_pham_hom_nay: 5,
  tong_vi_pham: 18,
  nghiem_trong: 3,
  muc_cao: 1,
  canh_bao: 1,
  camera_rui_ro_cao: [
    { camera_id: 'CAM-001', ten_camera: 'Camera Cổng trại', ten_vung: 'Cổng trại', so_vi_pham: 5 },
  ],
}

const fallbackTrends = {
  xu_huong_7_ngay: [
    { ngay: '2026-06-11', vi_pham: 1 },
    { ngay: '2026-06-12', vi_pham: 2 },
    { ngay: '2026-06-13', vi_pham: 1 },
    { ngay: '2026-06-14', vi_pham: 3 },
    { ngay: '2026-06-15', vi_pham: 2 },
    { ngay: '2026-06-16', vi_pham: 4 },
    { ngay: '2026-06-17', vi_pham: 5 },
  ],
  xu_huong_30_ngay: [
    { ngay: '2026-05-19', vi_pham: 2 },
    { ngay: '2026-05-25', vi_pham: 4 },
    { ngay: '2026-06-01', vi_pham: 3 },
    { ngay: '2026-06-08', vi_pham: 6 },
    { ngay: '2026-06-17', vi_pham: 5 },
  ],
}

const fallbackZones = [
  { ten_vung: 'Khu sản xuất', so_vi_pham: 3, nghiem_trong: 2, muc_cao: 1, canh_bao: 0 },
  { ten_vung: 'Khu an toàn', so_vi_pham: 1, nghiem_trong: 1, muc_cao: 0, canh_bao: 0 },
  { ten_vung: 'Kho cám', so_vi_pham: 1, nghiem_trong: 0, muc_cao: 0, canh_bao: 1 },
]

const fallbackViolations = [
  { ten_vi_pham: 'Di chuyển từ vùng bẩn sang vùng sạch', so_vi_pham: 1, muc_do: 'Nghiêm trọng' },
  { ten_vi_pham: 'Xe chưa sát trùng', so_vi_pham: 1, muc_do: 'Nghiêm trọng' },
  { ten_vi_pham: 'Chó xâm nhập khu chăn nuôi', so_vi_pham: 1, muc_do: 'Nghiêm trọng' },
]

function ComplianceDashboardPage() {
  const [summary, setSummary] = useState(fallbackSummary)
  const [trends, setTrends] = useState(fallbackTrends)
  const [zones, setZones] = useState(fallbackZones)
  const [violations, setViolations] = useState(fallbackViolations)
  const [status, setStatus] = useState('Đang đồng bộ dữ liệu tuân thủ ATSH...')

  useEffect(() => {
    async function loadCompliance() {
      try {
        const [summaryRes, trendsRes, zonesRes, violationsRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/compliance/summary`),
          fetch(`${API_BASE_URL}/api/compliance/trends`),
          fetch(`${API_BASE_URL}/api/compliance/top-zones`),
          fetch(`${API_BASE_URL}/api/compliance/top-violations`),
        ])
        if (![summaryRes, trendsRes, zonesRes, violationsRes].every((res) => res.ok)) {
          throw new Error('API tuân thủ ATSH chưa sẵn sàng')
        }
        setSummary(await summaryRes.json())
        setTrends(await trendsRes.json())
        setZones(await zonesRes.json())
        setViolations(await violationsRes.json())
        setStatus('Đã đồng bộ dữ liệu tuân thủ ATSH từ backend')
      } catch (error) {
        setStatus(`Đang dùng dữ liệu mẫu: ${error.message}`)
      }
    }

    loadCompliance()
  }, [])

  const stats = useMemo(
    () => [
      { label: 'Điểm ATSH', value: summary.diem_atsh, icon: ShieldCheck, tone: 'green' },
      { label: 'Vi phạm hôm nay', value: summary.vi_pham_hom_nay, icon: AlertTriangle, tone: 'red' },
      { label: 'Nghiêm trọng', value: summary.nghiem_trong, icon: Activity, tone: 'orange' },
      { label: 'Tổng vi phạm', value: summary.tong_vi_pham, icon: Camera, tone: 'green' },
    ],
    [summary],
  )

  return (
    <div className="compliance-page">
      <section className="stat-grid">
        {stats.map((stat) => (
          <article key={stat.label} className={`metric-card metric-card--${stat.tone}`}>
            <div>
              <span className="metric-card__label">{stat.label}</span>
              <strong>{stat.value}</strong>
            </div>
            <span className="metric-card__icon">
              <stat.icon size={24} />
            </span>
          </article>
        ))}
      </section>

      <section className="panel compliance-score-panel">
        <div className="panel__header">
          <div>
            <h2>Bảng tuân thủ ATSH</h2>
            <p>{status}</p>
          </div>
        </div>
        <div className="compliance-score">
          <div className="compliance-score__ring" style={{ '--score': summary.diem_atsh }}>
            <strong>{summary.diem_atsh}</strong>
            <span>/100</span>
          </div>
          <div>
            <h3>Điểm tuân thủ ATSH</h3>
            <p>Điểm tuân thủ được tính từ số lượng và mức độ nghiêm trọng của các vi phạm an toàn sinh học.</p>
          </div>
        </div>
      </section>

      <section className="dashboard-grid">
        <article className="panel panel--chart">
          <div className="panel__header">
            <div>
              <h2>Xu hướng 7 ngày</h2>
              <p>Số vi phạm ATSH theo ngày</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={trends.xu_huong_7_ngay}>
              <XAxis dataKey="ngay" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} />
              <Tooltip />
              <Line type="monotone" dataKey="vi_pham" stroke="#ef4444" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="panel panel--chart">
          <div className="panel__header">
            <div>
              <h2>Xu hướng 30 ngày</h2>
              <p>Xu hướng dài hạn rủi ro ATSH</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={trends.xu_huong_30_ngay}>
              <XAxis dataKey="ngay" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} />
              <Tooltip />
              <Line type="monotone" dataKey="vi_pham" stroke="#f97316" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </article>
      </section>

      <section className="dashboard-grid dashboard-grid--lists compliance-lists">
        <ComplianceList title="Loại vi phạm nhiều nhất" items={violations} nameKey="ten_vi_pham" valueKey="so_vi_pham" detailKey="muc_do" />
        <ComplianceList title="Khu vực rủi ro cao" items={zones} nameKey="ten_vung" valueKey="so_vi_pham" detailKey="nghiem_trong" detailSuffix=" nghiêm trọng" />
        <ComplianceList title="Camera vi phạm nhiều nhất" items={summary.camera_rui_ro_cao} nameKey="ten_camera" valueKey="so_vi_pham" detailKey="ten_vung" />
      </section>
    </div>
  )
}

function ComplianceList({ title, items = [], nameKey, valueKey, detailKey, detailSuffix = '' }) {
  return (
    <article className="panel">
      <div className="panel__header">
        <div>
          <h2>{title}</h2>
          <p>Xếp hạng rủi ro tuân thủ ATSH</p>
        </div>
      </div>
      <div className="rank-list">
        {items.map((item, index) => (
          <div key={`${title}-${item[nameKey]}`} className="rank-item">
            <span className="rank-item__index">{index + 1}</span>
            <div>
              <strong>{item[nameKey]}</strong>
              <p>{item[detailKey] ? `${item[detailKey]}${detailSuffix}` : 'Rủi ro ATSH'}</p>
            </div>
            <span>{item[valueKey]} vi phạm</span>
          </div>
        ))}
      </div>
    </article>
  )
}

export default ComplianceDashboardPage
