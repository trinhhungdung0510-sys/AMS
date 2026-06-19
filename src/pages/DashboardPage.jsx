import { useEffect, useState } from 'react'
import { Activity, ArrowRightLeft, Camera, GitBranch, ShieldAlert, Wifi } from 'lucide-react'
import {
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  alertDistribution,
  alertTrend,
  cameras,
  events,
  getTopCameras,
  getTopZones,
  onlineCameraCount,
} from '../data/mockData'

import { LOGO_SRC } from '../components/BrandLogo'
import { API_BASE_URL } from '../config/api'

const COLORS = ['#0B6B1B', '#F36A10', '#dc2626', '#facc15', '#64748b']

const zoneLabels = {
  parking_zone: 'Bãi đỗ xe',
  gestation_barn: 'Chuồng nái bầu',
  person_disinfection_zone: 'Khu sát trùng người',
  vehicle_disinfection_zone: 'Khu sát trùng xe',
  reception_zone: 'Khu tiếp khách',
  farrowing_barn: 'Chuồng nái đẻ',
  pig_loading_zone: 'Khu xuất nhập heo',
  worker_housing: 'Nhà ở công nhân',
  shower_room: 'Nhà tắm',
  handwash_zone: 'Khu rửa tay',
  boot_disinfection_tray: 'Khay sát trùng ủng',
}

function formatZone(zone) {
  return zoneLabels[zone] || zone
}

function formatCrossTime(value) {
  if (!value) return '--'
  return new Date(value).toLocaleString('vi-VN')
}

function DashboardPage() {
  const [recentCrossings, setRecentCrossings] = useState([])
  const [workflowCompliance, setWorkflowCompliance] = useState(null)
  const [workflowDashboard, setWorkflowDashboard] = useState(null)
  const [atshSummary, setAtshSummary] = useState(null)
  const criticalCount = events.filter((event) => ['danger', 'critical'].includes(event.severity)).length
  const stats = [
    { label: 'Camera', value: cameras.length, icon: Camera, tone: 'green' },
    { label: 'Sự kiện AI', value: events.length, icon: ShieldAlert, tone: 'orange' },
    { label: 'Cảnh báo nghiêm trọng', value: criticalCount, icon: Activity, tone: 'red' },
    { label: 'Camera trực tuyến', value: `${onlineCameraCount}/${cameras.length}`, icon: Wifi, tone: 'green' },
  ]

  useEffect(() => {
    const loadRecentCrossings = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/transitions/recent?limit=8`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const data = await response.json()
        setRecentCrossings(data.items || [])
      } catch {
        setRecentCrossings([])
      }
    }

    loadRecentCrossings()
    const timer = setInterval(loadRecentCrossings, 15000)

    const loadWorkflowCompliance = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/workflows/compliance/summary`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const data = await response.json()
        setWorkflowCompliance(data)
      } catch {
        setWorkflowCompliance(null)
      }
    }

    const loadWorkflowDashboard = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/workflows/dashboard`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const data = await response.json()
        setWorkflowDashboard(data)
      } catch {
        setWorkflowDashboard(null)
      }
    }

    const loadAtshSummary = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/dashboard/summary`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const data = await response.json()
        setAtshSummary(data)
      } catch {
        setAtshSummary(null)
      }
    }

    loadWorkflowCompliance()
    loadWorkflowDashboard()
    loadAtshSummary()
    const workflowTimer = setInterval(() => {
      loadWorkflowCompliance()
      loadWorkflowDashboard()
      loadAtshSummary()
    }, 15000)
    return () => {
      clearInterval(timer)
      clearInterval(workflowTimer)
    }
  }, [])

  return (
    <div className="dashboard-page">
      <img src={LOGO_SRC} alt="TIN NGHIA AMS" className="dashboard-page__brand-mark" />
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

      <section className="dashboard-grid">
        <article className="panel panel--chart">
          <div className="panel__header">
            <div>
              <h2>Biểu đồ cảnh báo 7 ngày</h2>
              <p>Xu hướng cảnh báo AI theo ngày</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={alertTrend}>
              <XAxis dataKey="day" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="alerts"
                stroke="#f97316"
                strokeWidth={3}
                dot={{ r: 4, fill: '#14532d' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="panel panel--chart">
          <div className="panel__header">
            <div>
              <h2>Phân bố cảnh báo</h2>
              <p>Theo loại cảnh báo AI</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={alertDistribution} dataKey="value" nameKey="name" innerRadius={58} outerRadius={92}>
                {alertDistribution.map((entry, index) => (
                  <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </article>
      </section>

      <section className="dashboard-grid dashboard-grid--lists">
        <article className="panel panel--workflow">
          <div className="panel__header">
            <div>
              <h2>Vi phạm ATSH (Biosecurity AI)</h2>
              <p>AMS v4.0 — phát hiện vi phạm an toàn sinh học</p>
            </div>
            <span className="panel__badge panel__badge--score">
              <ShieldAlert size={16} />
              {atshSummary?.vi_pham_atsh_hom_nay ?? '--'}
            </span>
          </div>
          {atshSummary ? (
            <>
              <div className="workflow-stats">
                <div>
                  <strong>{atshSummary.vi_pham_atsh_hom_nay ?? 0}</strong>
                  <span>Hôm nay</span>
                </div>
                <div>
                  <strong>{atshSummary.vi_pham_atsh_critical ?? 0}</strong>
                  <span>CRITICAL</span>
                </div>
                <div>
                  <strong>{atshSummary.vi_pham_atsh_warning ?? 0}</strong>
                  <span>WARNING</span>
                </div>
                <div>
                  <strong>{atshSummary.vi_pham_atsh_info ?? 0}</strong>
                  <span>INFO</span>
                </div>
              </div>
              <div className="rank-list">
                {(atshSummary.top_quy_tac_atsh || []).slice(0, 5).map((item, index) => (
                  <div key={item.ma_quy_tac} className="rank-item">
                    <span className="rank-item__index">{index + 1}</span>
                    <div>
                      <strong>{item.ma_quy_tac}</strong>
                      <p>Quy tắc ATSH v4.0</p>
                    </div>
                    <span>{item.so_vi_pham} vi phạm</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="crossing-list__empty">Chưa tải được thống kê vi phạm ATSH.</p>
          )}
        </article>
      </section>

      <section className="dashboard-grid dashboard-grid--lists">
        <article className="panel panel--workflow">
          <div className="panel__header">
            <div>
              <h2>Tuân thủ quy trình ATSH</h2>
              <p>{workflowCompliance?.workflow_name || 'Quy trình vào khu sản xuất'}</p>
            </div>
            <span className="panel__badge panel__badge--score">
              <GitBranch size={16} />
              {workflowCompliance ? `${workflowCompliance.compliance_score}%` : '--'}
            </span>
          </div>
          {workflowCompliance ? (
            <>
              <div className="workflow-score-ring">
                <strong>{workflowCompliance.compliance_score}%</strong>
                <span>Tuân thủ quy trình</span>
              </div>
              <div className="workflow-steps">
                {workflowCompliance.expected_steps.map((step, index) => (
                  <span key={step} className="workflow-step-chip">
                    {index + 1}. {step}
                  </span>
                ))}
              </div>
              <div className="workflow-stats">
                <div>
                  <strong>{workflowCompliance.compliant_tracks}</strong>
                  <span>Track đúng quy trình</span>
                </div>
                <div>
                  <strong>{workflowCompliance.violation_count}</strong>
                  <span>Vi phạm quy trình</span>
                </div>
              </div>
              <div className="workflow-violations">
                {(workflowCompliance.recent_violations || []).slice(0, 3).map((item) => (
                  <div key={item.event_id} className="workflow-violation-item">
                    <strong>{item.ten_vi_pham || item.alert_type}</strong>
                    <span>{item.ten_vung || formatZone(item.zone)} · {formatCrossTime(item.thoi_gian || item.occurred_at)}</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="crossing-list__empty">Chưa tải được dữ liệu workflow compliance.</p>
          )}
        </article>

        <article className="panel panel--workflow">
          <div className="panel__header">
            <div>
              <h2>Vi phạm quy trình ATSH hôm nay</h2>
              <p>Theo dõi vi phạm quy trình an toàn sinh học trong ngày</p>
            </div>
            <span className="panel__badge panel__badge--score">
              <ShieldAlert size={16} />
              {workflowDashboard?.vi_pham_hom_nay ?? workflowCompliance?.vi_pham_hom_nay ?? '--'}
            </span>
          </div>
          {workflowDashboard || workflowCompliance ? (
            <>
              <div className="workflow-stats">
                <div>
                  <strong>{workflowDashboard?.vi_pham_hom_nay ?? workflowCompliance?.vi_pham_hom_nay ?? 0}</strong>
                  <span>Vi phạm hôm nay</span>
                </div>
              </div>
              <div className="workflow-violations">
                {(workflowDashboard?.chi_tiet_hom_nay || workflowCompliance?.recent_violations || [])
                  .slice(0, 5)
                  .map((item) => (
                    <div key={item.event_id} className="workflow-violation-item">
                      <strong>{item.ten_vi_pham}</strong>
                      <span>{item.ten_vung || formatZone(item.zone)} · {formatCrossTime(item.thoi_gian || item.occurred_at)}</span>
                    </div>
                  ))}
              </div>
            </>
          ) : (
            <p className="crossing-list__empty">Chưa tải được dữ liệu vi phạm quy trình.</p>
          )}
        </article>

        <article className="panel">
          <div className="panel__header">
            <div>
              <h2>Top quy trình bị vi phạm</h2>
              <p>Quy trình ATSH bị vi phạm nhiều nhất hôm nay</p>
            </div>
          </div>
          <div className="rank-list">
            {(workflowDashboard?.top_quy_trinh_bi_vi_pham || workflowCompliance?.top_quy_trinh_bi_vi_pham || []).length === 0 ? (
              <p className="crossing-list__empty">Chưa có vi phạm quy trình hôm nay.</p>
            ) : (
              (workflowDashboard?.top_quy_trinh_bi_vi_pham || workflowCompliance?.top_quy_trinh_bi_vi_pham || []).map(
                (item, index) => (
                  <div key={item.ten_quy_trinh} className="rank-item">
                    <span className="rank-item__index">{index + 1}</span>
                    <div>
                      <strong>{item.ten_quy_trinh}</strong>
                      <p>Quy trình ATSH</p>
                    </div>
                    <span>{item.so_vi_pham} vi phạm</span>
                  </div>
                ),
              )
            )}
          </div>
        </article>

        <article className="panel">
          <div className="panel__header">
            <div>
              <h2>Chuyển vùng gần đây</h2>
              <p>Đối tượng vừa chuyển zone trên camera</p>
            </div>
            <span className="panel__badge">
              <ArrowRightLeft size={16} />
              {recentCrossings.length} gần nhất
            </span>
          </div>
          <div className="crossing-list">
            {recentCrossings.length === 0 ? (
              <p className="crossing-list__empty">Chưa có dữ liệu zone crossing từ backend.</p>
            ) : (
              recentCrossings.map((crossing) => (
                <div key={crossing.id} className="crossing-item">
                  <div className="crossing-item__meta">
                    <strong>{crossing.object_type}</strong>
                    <span>Track #{crossing.track_id}</span>
                    <span>{crossing.camera_id}</span>
                  </div>
                  <div className="crossing-item__route">
                    <span>{formatZone(crossing.from_zone)}</span>
                    <ArrowRightLeft size={14} />
                    <span>{formatZone(crossing.to_zone)}</span>
                  </div>
                  <span className="crossing-item__time">{formatCrossTime(crossing.cross_time)}</span>
                </div>
              ))
            )}
          </div>
        </article>

        <article className="panel">
          <div className="panel__header">
            <div>
              <h2>Top camera nhiều vi phạm</h2>
              <p>Camera có số sự kiện cao nhất</p>
            </div>
          </div>
          <div className="rank-list">
            {getTopCameras().map((camera, index) => (
              <div key={camera.id} className="rank-item">
                <span className="rank-item__index">{index + 1}</span>
                <div>
                  <strong>{camera.name}</strong>
                  <p>{camera.zone}</p>
                </div>
                <span>{camera.totalEvents} sự kiện</span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <div className="panel__header">
            <div>
              <h2>Top khu vực rủi ro</h2>
              <p>Khu vực cần ưu tiên giám sát</p>
            </div>
          </div>
          <div className="rank-list">
            {getTopZones().map((zone, index) => (
              <div key={zone.zone} className="rank-item">
                <span className="rank-item__index">{index + 1}</span>
                <div>
                  <strong>{zone.zone}</strong>
                  <p>Rủi ro vận hành</p>
                </div>
                <span>{zone.totalEvents} cảnh báo</span>
              </div>
            ))}
          </div>
        </article>
      </section>
    </div>
  )
}

export default DashboardPage
