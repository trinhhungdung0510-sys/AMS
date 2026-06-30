import { useCallback, useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  AlertTriangle,
  Camera,
  Inbox,
  LayoutDashboard,
  Map,
  PenLine,
  Settings,
  ShieldCheck,
  Wifi,
  WifiOff,
} from 'lucide-react'
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import ErrorBoundary from '../components/common/ErrorBoundary'
import SmartFarmDesigner from '../components/farmGis/SmartFarmDesigner'
import DashboardLiveSection from '../components/dashboard/DashboardLiveSection'
import CollapsibleRealtimeEventPanel from '../components/realtime/CollapsibleRealtimeEventPanel'
import EventsListPanel from '../components/EventsListPanel'
import {
  ATSH_DEDUCTIONS,
  CHART_DATA,
  RISK_LABELS,
  buildTopCameras,
  buildTopRules,
  buildTopZones,
  computeDiseaseRisk,
  computeFarmAtshScore,
  countDeductions,
  getDefaultDashboardState,
} from '../data/farmControlDashboard'
import { getDashboardMapFromDesigner, subscribeFarmMapUpdates } from '../data/farmMapSync'
import { getDefaultDesignerState } from '../data/smartFarmDesigner'
import { atshViolations, computeAtshKpis } from '../data/atshViolations'
import { useEventStore } from '../context/EventStore'
import { useViolationProcessing } from '../context/ViolationProcessingContext'
import { useDashboardBootstrap } from '../context/DashboardBootstrapStore'
import { API_BASE_URL } from '../config/api'

function asList(value) {
  return Array.isArray(value) ? value : []
}

function FarmControlDashboardPage() {
  const { metrics, connected, cameras } = useEventStore()
  const { data: bootstrapData } = useDashboardBootstrap()
  const { openMetrics } = useViolationProcessing()
  const [searchParams, setSearchParams] = useSearchParams()
  const activeTab = searchParams.get('tab') === 'ban-do' ? 'ban-do' : 'tong-quan'

  const defaults = useMemo(() => getDefaultDashboardState(), [])
  const [atshScore, setAtshScore] = useState(defaults.atshScore)
  const [violationsToday, setViolationsToday] = useState(defaults.violationsToday)
  const [diseaseRisk, setDiseaseRisk] = useState(defaults.diseaseRisk)
  const [deductions, setDeductions] = useState(defaults.deductions)
  const [topZones, setTopZones] = useState(defaults.topZones)
  const [topCameras, setTopCameras] = useState(defaults.topCameras)
  const [topRules, setTopRules] = useState(defaults.topRules)
  const [chartRange, setChartRange] = useState('day')
  const [mapData, setMapData] = useState(() => {
    try {
      return getDashboardMapFromDesigner()
    } catch {
      return getDashboardMapFromDesigner(getDefaultDesignerState())
    }
  })
  const [loadNotice, setLoadNotice] = useState(null)

  const refreshFromData = useCallback((violations) => {
    const kpis = computeAtshKpis(violations)
    setAtshScore(computeFarmAtshScore(violations))
    setViolationsToday(kpis.totalToday)
    setDiseaseRisk(computeDiseaseRisk(violations))
    setDeductions(countDeductions(violations))
    setTopZones(buildTopZones(violations))
    setTopCameras(buildTopCameras(violations))
    setTopRules(buildTopRules(violations))
  }, [])

  const loadDashboard = useCallback(async () => {
    try {
      setLoadNotice(null)
      const [summaryRes, dashRes, zonesRes, rulesRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/compliance/summary`),
        fetch(`${API_BASE_URL}/api/dashboard/summary`),
        fetch(`${API_BASE_URL}/api/compliance/top-zones`),
        fetch(`${API_BASE_URL}/api/compliance/top-violations`),
      ])

      if (summaryRes.ok) {
        const summary = await summaryRes.json()
        setAtshScore(summary?.diem_atsh ?? computeFarmAtshScore())
        setViolationsToday(summary?.vi_pham_hom_nay ?? computeAtshKpis(atshViolations).totalToday)
        const riskyCameras = asList(summary?.camera_rui_ro_cao)
        if (riskyCameras.length) {
          setTopCameras(riskyCameras.map((item) => ({
            name: item?.ten_camera || 'Chưa có dữ liệu',
            count: item?.so_vi_pham ?? 0,
          })))
        }
      }

      if (dashRes.ok) {
        await dashRes.json()
      }

      if (zonesRes.ok) {
        const zones = await zonesRes.json()
        const zoneList = asList(zones)
        if (zoneList.length) {
          setTopZones(zoneList.map((item) => ({
            name: item?.ten_vung || 'Chưa có dữ liệu',
            count: item?.so_vi_pham ?? 0,
          })))
        }
      }

      if (rulesRes.ok) {
        const rules = await rulesRes.json()
        const ruleList = asList(rules)
        if (ruleList.length) {
          setTopRules(ruleList.map((item) => ({
            name: item?.ten_vi_pham || 'Chưa có dữ liệu',
            count: item?.so_vi_pham ?? 0,
          })))
        }
      }
    } catch {
      refreshFromData(atshViolations)
      setLoadNotice('Không tải được dữ liệu từ API. Đang hiển thị dữ liệu cục bộ.')
    }
  }, [refreshFromData])

  useEffect(() => {
    loadDashboard()
    const timer = setInterval(loadDashboard, 30000)
    return () => clearInterval(timer)
  }, [loadDashboard])

  useEffect(() => {
    return subscribeFarmMapUpdates((nextMap) => {
      try {
        setMapData(getDashboardMapFromDesigner(nextMap))
      } catch {
        setMapData(getDashboardMapFromDesigner())
      }
    })
  }, [])

  const chartData = CHART_DATA[chartRange] || CHART_DATA.day
  const scoreTone = atshScore >= 80 ? 'safe' : atshScore >= 60 ? 'attention' : 'risk'
  const violationMetrics = openMetrics || {}
  const eventMetrics = metrics || {}
  const openToday = violationMetrics.openToday ?? 0
  const openCritical = violationMetrics.openCritical ?? 0
  const onlineCameras = eventMetrics.onlineCameras ?? 0
  const totalCameras = eventMetrics.totalCameras ?? 0
  const offlineCameras = Math.max(0, totalCameras - onlineCameras)
  const alertsToday = eventMetrics.totalEventsToday ?? violationsToday
  const camerasNeedConfig = bootstrapData?.cameraSummary?.health?.warning ?? 0
  const mapZones = asList(mapData?.zones)
  const mapCameras = asList(mapData?.cameras)
  const safeDeductions = asList(deductions)
  const liveCameras = cameras?.length ? cameras : bootstrapData?.cameraSummary?.cameras

  const stats = [
    { label: 'Tổng Camera', value: totalCameras, icon: Camera, tone: 'safe' },
    { label: 'Camera Online', value: onlineCameras, icon: Wifi, tone: 'safe' },
    { label: 'Camera Offline', value: offlineCameras, icon: WifiOff, tone: offlineCameras > 0 ? 'attention' : 'safe' },
    { label: 'Cảnh báo hôm nay', value: alertsToday, icon: AlertTriangle, tone: alertsToday > 0 ? 'attention' : 'safe' },
    { label: 'Vi phạm ATSH hôm nay', value: violationsToday, icon: ShieldCheck, tone: violationsToday > 0 ? 'attention' : 'safe' },
    { label: 'Camera cần cấu hình', value: camerasNeedConfig, icon: Settings, tone: camerasNeedConfig > 0 ? 'attention' : 'safe' },
  ]

  return (
    <div className="farm-control farm-control--enterprise">
      <div className="farm-control__toolbar">
        <header className="farm-control__hero">
          <div>
            <h1>Bảng điều khiển</h1>
            <p>Tổng quan giám sát ATSH — camera, cảnh báo và trạng thái hệ thống</p>
          </div>
        </header>
        <div className={`farm-control__live${connected ? ' farm-control__live--on' : ''}`}>
          {connected ? <Wifi size={16} /> : <WifiOff size={16} />}
          <span>{connected ? 'Cập nhật thời gian thực' : 'Đang kết nối WebSocket...'}</span>
        </div>
      </div>

      <nav className="farm-control__tabs">
        <button
          type="button"
          className={`farm-control__tab${activeTab === 'tong-quan' ? ' farm-control__tab--active' : ''}`}
          onClick={() => setSearchParams({})}
        >
          <LayoutDashboard size={16} /> Tổng quan
        </button>
        <button
          type="button"
          className={`farm-control__tab${activeTab === 'ban-do' ? ' farm-control__tab--active' : ''}`}
          onClick={() => setSearchParams({ tab: 'ban-do' })}
        >
          <Map size={16} /> Bản đồ trang trại
        </button>
      </nav>

      {loadNotice ? (
        <p className="atsh-soc__notice panel" role="status">{loadNotice}</p>
      ) : null}

      <ErrorBoundary fallbackTitle="Không thể hiển thị bảng điều khiển">
        {activeTab === 'ban-do' ? (
          <SmartFarmDesigner embedded />
        ) : (
          <div className="dashboard-enterprise">
            <section className="farm-control__kpis">
              {stats.map((item) => {
                const Icon = item.icon
                return (
                  <article key={item.label} className={`farm-kpi farm-kpi--${item.tone}`}>
                    <div className="farm-kpi__icon"><Icon size={22} /></div>
                    <div>
                      <span>{item.label}</span>
                      <strong>{item.value}{item.suffix || ''}</strong>
                    </div>
                  </article>
                )
              })}
            </section>

            <ErrorBoundary fallbackTitle="Không thể hiển thị camera live">
              <section className="dashboard-enterprise__row dashboard-enterprise__row--primary">
                <DashboardLiveSection cameras={liveCameras} />
                <div className="dashboard-enterprise__stack">
                  <CollapsibleRealtimeEventPanel defaultExpanded variant="page" limit={12} />
                </div>
              </section>
            </ErrorBoundary>

            <ErrorBoundary fallbackTitle="Không thể hiển thị sự kiện">
              <section className="dashboard-enterprise__row dashboard-enterprise__row--secondary">
                <EventsListPanel />
                <div className="dashboard-enterprise__stack">
                  <aside className="farm-control__score panel">
                  <h2>Điểm ATSH</h2>
                  <p>Bắt đầu 100 điểm · Trừ theo vi phạm hôm nay</p>
                  <div className={`farm-score-ring farm-score-ring--${scoreTone}`}>
                    <strong>{atshScore}</strong>
                    <span>/ 100</span>
                  </div>
                  <ul className="farm-deductions">
                    {safeDeductions.map((item) => (
                      <li key={item.key}>
                        <span>{item.label}</span>
                        <span>-{item.points} đ · ×{item.count}</span>
                      </li>
                    ))}
                  </ul>
                  <div className="farm-deductions__note">
                    {ATSH_DEDUCTIONS.map((item) => item.label).join(' · ')}
                  </div>
                </aside>

                <article className="panel dashboard-system-status">
                  <div className="panel__header">
                    <div>
                      <h2>Trạng thái hệ thống</h2>
                      <p>Giám sát vận hành thời gian thực</p>
                    </div>
                  </div>
                  <ul className="dashboard-system-status__list">
                    <li className={`dashboard-system-status__item dashboard-system-status__item--${connected ? 'ok' : 'warn'}`}>
                      <span>AI Engine</span>
                      <strong>{connected ? 'Hoạt động' : 'Đang kết nối…'}</strong>
                    </li>
                    <li className="dashboard-system-status__item dashboard-system-status__item--ok">
                      <span>Camera Online</span>
                      <strong>{onlineCameras}/{totalCameras}</strong>
                    </li>
                    <li className={`dashboard-system-status__item dashboard-system-status__item--${openCritical > 0 ? 'risk' : 'ok'}`}>
                      <span>Vi phạm nghiêm trọng</span>
                      <strong>{openCritical}</strong>
                    </li>
                    <li className={`dashboard-system-status__item dashboard-system-status__item--${openToday > 0 ? 'warn' : 'ok'}`}>
                      <span>Vi phạm chưa xử lý</span>
                      <strong>{openToday}</strong>
                    </li>
                    <li className={`dashboard-system-status__item dashboard-system-status__item--${connected ? 'ok' : 'warn'}`}>
                      <span>Gateway</span>
                      <strong>{connected ? 'WebSocket OK' : 'Đang kết nối…'}</strong>
                    </li>
                    <li className={`dashboard-system-status__item dashboard-system-status__item--${camerasNeedConfig > 0 ? 'warn' : 'ok'}`}>
                      <span>Notification</span>
                      <strong>{camerasNeedConfig > 0 ? `${camerasNeedConfig} camera cần cấu hình` : 'Ổn định'}</strong>
                    </li>
                  </ul>
                </article>
              </div>
            </section>
            </ErrorBoundary>

            <ErrorBoundary fallbackTitle="Không thể hiển thị biểu đồ">
              <section className="dashboard-enterprise__row dashboard-enterprise__row--charts">
              <section className="farm-control__chart panel panel--chart">
                <div className="panel__header">
                  <div>
                    <h2>Biểu đồ vi phạm</h2>
                    <p>Vi phạm theo ngày</p>
                  </div>
                  <div className="farm-chart-tabs">
                    {[
                      ['day', 'Theo ngày'],
                      ['week', 'Theo tuần'],
                      ['month', 'Theo tháng'],
                    ].map(([value, label]) => (
                      <button
                        key={value}
                        type="button"
                        className={`farm-chart-tabs__btn${chartRange === value ? ' farm-chart-tabs__btn--active' : ''}`}
                        onClick={() => setChartRange(value)}
                      >
                        {label}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="farm-chart">
                  {asList(chartData).length === 0 ? (
                    <div className="atsh-soc__empty">
                      <Inbox size={28} />
                      <p>Chưa có dữ liệu.</p>
                    </div>
                  ) : (
                    <ResponsiveContainer width="100%" height={280}>
                      <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="4 4" stroke="#e5e7eb" />
                        <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Line type="monotone" dataKey="value" stroke="#0B6B1B" strokeWidth={3} dot={{ r: 4 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </section>

              {[
                ['Top khu vực vi phạm', topZones],
                ['Top camera vi phạm', topCameras],
              ].map(([title, items]) => {
                const list = asList(items)
                return (
                  <article key={title} className="farm-top panel">
                    <h2>{title}</h2>
                    {list.length === 0 ? (
                      <p className="farm-top__empty">Chưa có dữ liệu.</p>
                    ) : (
                      <ul>
                        {list.map((item, index) => (
                          <li key={`${item?.name || 'item'}-${index}`}>
                            <span>{index + 1}. {item?.name || 'Chưa có dữ liệu'}</span>
                            <strong>{item?.count ?? 0}</strong>
                          </li>
                        ))}
                      </ul>
                    )}
                  </article>
                )
              })}
            </section>
            </ErrorBoundary>

            <ErrorBoundary fallbackTitle="Không thể hiển thị top quy tắc">
              <section className="dashboard-enterprise__row dashboard-enterprise__row--details-wide">
              <article className="farm-top panel">
                <h2>Top quy tắc bị vi phạm</h2>
                {asList(topRules).length === 0 ? (
                  <p className="farm-top__empty">Chưa có dữ liệu.</p>
                ) : (
                  <ul>
                    {asList(topRules).map((item, index) => (
                      <li key={`${item?.name || 'item'}-${index}`}>
                        <span>{index + 1}. {item?.name || 'Chưa có dữ liệu'}</span>
                        <strong>{item?.count ?? 0}</strong>
                      </li>
                    ))}
                  </ul>
                )}
              </article>
            </section>
            </ErrorBoundary>

            <ErrorBoundary fallbackTitle="Không thể hiển thị bản đồ trang trại">
              <section className="dashboard-enterprise__row dashboard-enterprise__row--details-wide">
              <section className="farm-control__map panel">
                <div className="panel__header">
                  <div>
                    <h2>Bản đồ trang trại</h2>
                    <p>Xem nhanh trạng thái ATSH theo khu vực</p>
                  </div>
                  <div className="farm-control__map-actions">
                    <button type="button" className="btn btn--outline" onClick={() => setSearchParams({ tab: 'ban-do' })}>
                      <PenLine size={15} /> Mở bản đồ đầy đủ
                    </button>
                    <div className="farm-control__legend">
                      <span><i className="farm-risk-dot farm-risk-dot--safe" /> Xanh · An toàn</span>
                      <span><i className="farm-risk-dot farm-risk-dot--attention" /> Vàng · Cần chú ý</span>
                      <span><i className="farm-risk-dot farm-risk-dot--risk" /> Đỏ · Nguy cơ</span>
                    </div>
                  </div>
                </div>
                <div className="farm-control-map">
                  {mapZones.length === 0 ? (
                    <div className="atsh-soc__empty">
                      <Inbox size={28} />
                      <p>Chưa có dữ liệu.</p>
                    </div>
                  ) : (
                    <>
                      {mapZones.map((zone) => (
                        <div
                          key={zone.id}
                          className={`farm-control-zone farm-control-zone--${zone.risk || 'safe'}`}
                          style={{
                            left: `${zone.x ?? 0}%`,
                            top: `${zone.y ?? 0}%`,
                            width: `${zone.width ?? 10}%`,
                            height: `${zone.height ?? 10}%`,
                            transform: zone.rotation ? `rotate(${zone.rotation}deg)` : undefined,
                          }}
                        >
                          <strong>{zone.name || 'Khu vực'}</strong>
                          <small>{RISK_LABELS[zone.risk] || RISK_LABELS.safe}</small>
                        </div>
                      ))}
                      {mapCameras.map((cam) => (
                        <div
                          key={cam.id}
                          className={`farm-control-camera farm-control-camera--${cam.status === 'online' ? 'online' : 'offline'}`}
                          style={{
                            left: `${(cam.x ?? 0) + (cam.width ?? 0) / 2}%`,
                            top: `${(cam.y ?? 0) + (cam.height ?? 0) / 2}%`,
                          }}
                          title={cam.name || cam.id}
                        />
                      ))}
                    </>
                  )}
                </div>
              </section>
              </section>
            </ErrorBoundary>
          </div>
        )}
      </ErrorBoundary>
    </div>
  )
}

export default FarmControlDashboardPage
