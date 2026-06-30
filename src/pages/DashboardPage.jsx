import { ArrowRightLeft, GitBranch, ShieldAlert } from 'lucide-react'
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
  getTopCameras,
  getTopZones,
} from '../data/mockData'
import ComplianceKpiWidgets from '../components/dashboard/ComplianceKpiWidgets'
import BiosecurityCompliancePanel from '../components/dashboard/BiosecurityCompliancePanel'
import TopViolationsWidget from '../components/dashboard/TopViolationsWidget'
import CameraHealthWidget from '../components/dashboard/CameraHealthWidget'
import GmailDeliveryWidget from '../components/dashboard/GmailDeliveryWidget'
import DashboardLiveSection from '../components/dashboard/DashboardLiveSection'
import CollapsibleRealtimeEventPanel from '../components/realtime/CollapsibleRealtimeEventPanel'
import EventsListPanel from '../components/EventsListPanel'
import ErrorBoundary from '../components/common/ErrorBoundary'
import { useDashboardBootstrap } from '../context/DashboardBootstrapStore'
import { useEventStore } from '../context/EventStore'

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

function healthTone(value) {
  if (value === 'ok' || value === true) return 'ok'
  if (value === 'degraded' || value === 'warn' || value === 'warning') return 'warn'
  if (value == null || value === '—') return 'warn'
  return 'risk'
}

function formatHealthValue(value) {
  if (value == null || value === '') return '—'
  if (typeof value === 'boolean') return value ? 'Hoạt động' : 'Ngưng'
  if (value === 'ok') return 'Bình thường'
  if (value === 'degraded') return 'Suy giảm'
  if (value === 'unavailable') return 'Không khả dụng'
  return String(value)
}

function DashboardSystemStatusPanel({
  systemHealth,
  connected,
  cameraHealth,
  notificationSummary,
  loading,
}) {
  const items = [
    {
      label: 'AI Engine',
      value: connected ? 'Hoạt động' : 'Đang kết nối…',
      tone: connected ? 'ok' : 'warn',
    },
    {
      label: 'Database',
      value: formatHealthValue(systemHealth?.database),
      tone: healthTone(systemHealth?.database),
    },
    {
      label: 'Redis',
      value: formatHealthValue(systemHealth?.redis),
      tone: healthTone(systemHealth?.redis),
    },
    {
      label: 'Camera Online',
      value: loading ? '…' : `${cameraHealth?.online ?? 0}/${cameraHealth?.total ?? 0}`,
      tone: 'ok',
    },
    {
      label: 'Gateway',
      value: formatHealthValue(systemHealth?.websocket),
      tone: healthTone(systemHealth?.websocket),
    },
    {
      label: 'Notification',
      value: notificationSummary?.gmail?.connected ? 'Gmail kết nối' : 'Chưa kết nối',
      tone: notificationSummary?.gmail?.connected ? 'ok' : 'warn',
    },
  ]

  return (
    <article className="panel dashboard-system-status">
      <div className="panel__header">
        <div>
          <h2>Trạng thái hệ thống</h2>
          <p>AI, cơ sở dữ liệu và kênh thông báo</p>
        </div>
      </div>
      <ul className="dashboard-system-status__list">
        {items.map((item) => (
          <li
            key={item.label}
            className={`dashboard-system-status__item dashboard-system-status__item--${item.tone}`}
          >
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </li>
        ))}
      </ul>
    </article>
  )
}

function DashboardPage() {
  const { data, loading } = useDashboardBootstrap()
  const { cameras, connected } = useEventStore()

  const atshSummary = data?.dashboardSummary ?? null
  const complianceKpis = data?.complianceSummary?.kpis ?? null
  const topViolations = data?.complianceSummary?.topViolations?.items ?? []
  const cameraHealth = data?.cameraSummary?.health ?? null
  const notificationSummary = data?.notificationSummary ?? null
  const workflowCompliance = data?.workflowSummary?.compliance ?? null
  const workflowDashboard = data?.workflowSummary?.dashboard ?? null
  const recentCrossings = data?.workflowSummary?.recentCrossings?.items ?? []
  const systemHealth = data?.systemHealth ?? null
  const liveCameras = cameras?.length ? cameras : data?.cameraSummary?.cameras

  return (
    <div className="dashboard-page dashboard-enterprise">
      <section className="dashboard-enterprise__row dashboard-enterprise__row--stats">
        <ComplianceKpiWidgets kpis={complianceKpis} loading={loading} />
      </section>

      <ErrorBoundary fallbackTitle="Không thể hiển thị camera live">
        <section className="dashboard-enterprise__row dashboard-enterprise__row--primary">
          <DashboardLiveSection cameras={liveCameras} />
          <div className="dashboard-enterprise__stack">
            <CollapsibleRealtimeEventPanel defaultExpanded variant="page" limit={12} />
            <TopViolationsWidget items={topViolations} loading={loading} />
          </div>
        </section>
      </ErrorBoundary>

      <ErrorBoundary fallbackTitle="Không thể hiển thị sự kiện">
        <section className="dashboard-enterprise__row dashboard-enterprise__row--secondary">
          <EventsListPanel />
          <div className="dashboard-enterprise__stack">
            <DashboardSystemStatusPanel
              systemHealth={systemHealth}
              connected={connected}
              cameraHealth={cameraHealth}
              notificationSummary={notificationSummary}
              loading={loading}
            />
            <CameraHealthWidget summary={cameraHealth} loading={loading} />
            <GmailDeliveryWidget summary={notificationSummary} loading={loading} />
          </div>
        </section>
      </ErrorBoundary>

      <section className="dashboard-enterprise__row dashboard-enterprise__row--charts">
        <article className="panel panel--chart">
          <div className="panel__header">
            <div>
              <h2>Biểu đồ cảnh báo 7 ngày</h2>
              <p>Vi phạm theo ngày</p>
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
              <p>Vi phạm theo loại</p>
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

        <article className="panel">
          <div className="panel__header">
            <div>
              <h2>Top camera nhiều vi phạm</h2>
              <p>Camera phát sinh nhiều cảnh báo</p>
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
      </section>

      <section className="dashboard-enterprise__row dashboard-enterprise__row--details-wide">
        <BiosecurityCompliancePanel />
      </section>

      <section className="dashboard-enterprise__row dashboard-enterprise__row--details">
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
                {(workflowCompliance.expected_steps || []).map((step, index) => (
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
      </section>

      <section className="dashboard-enterprise__row dashboard-enterprise__row--details">
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
      </section>

      <section className="dashboard-enterprise__row dashboard-enterprise__row--details">
        <article className="panel">
          <div className="panel__header">
            <div>
              <h2>Chuyển vùng gần đây</h2>
              <p>Sự kiện gần đây — đối tượng chuyển zone trên camera</p>
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
