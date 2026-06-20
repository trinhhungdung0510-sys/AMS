import { useCallback, useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  Activity,
  AlertTriangle,
  Camera,
  LayoutDashboard,
  Map,
  PenLine,
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
import SmartFarmDesigner from '../components/farmGis/SmartFarmDesigner'
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
import { atshViolations, computeAtshKpis } from '../data/atshViolations'
import { useEventStore } from '../context/EventStore'
import { API_BASE_URL } from '../config/api'

function FarmControlDashboardPage() {
  const { feedEvents, metrics, connected, loading: eventsLoading } = useEventStore()
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
  const [mapData, setMapData] = useState(() => getDashboardMapFromDesigner())

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
      const [summaryRes, dashRes, zonesRes, rulesRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/compliance/summary`),
        fetch(`${API_BASE_URL}/api/dashboard/summary`),
        fetch(`${API_BASE_URL}/api/compliance/top-zones`),
        fetch(`${API_BASE_URL}/api/compliance/top-violations`),
      ])

      if (summaryRes.ok) {
        const summary = await summaryRes.json()
        setAtshScore(summary.diem_atsh ?? computeFarmAtshScore())
        setViolationsToday(summary.vi_pham_hom_nay ?? computeAtshKpis(atshViolations).totalToday)
        if (summary.camera_rui_ro_cao?.length) {
          setTopCameras(summary.camera_rui_ro_cao.map((item) => ({
            name: item.ten_camera,
            count: item.so_vi_pham,
          })))
        }
      }

      if (dashRes.ok) {
        await dashRes.json()
      }

      if (zonesRes.ok) {
        const zones = await zonesRes.json()
        if (zones.length) {
          setTopZones(zones.map((item) => ({ name: item.ten_vung, count: item.so_vi_pham })))
        }
      }

      if (rulesRes.ok) {
        const rules = await rulesRes.json()
        if (rules.length) {
          setTopRules(rules.map((item) => ({ name: item.ten_vi_pham, count: item.so_vi_pham })))
        }
      }
    } catch {
      refreshFromData(atshViolations)
    }
  }, [refreshFromData])

  useEffect(() => {
    loadDashboard()
    const timer = setInterval(loadDashboard, 30000)
    return () => clearInterval(timer)
  }, [loadDashboard])

  useEffect(() => subscribeFarmMapUpdates(setMapData), [])

  const chartData = CHART_DATA[chartRange]
  const scoreTone = atshScore >= 80 ? 'safe' : atshScore >= 60 ? 'attention' : 'risk'

  const stats = [
    { label: 'Điểm ATSH', value: `${atshScore}`, suffix: '/100', icon: ShieldCheck, tone: scoreTone },
    { label: 'Event đang mở', value: metrics.openEvents, icon: AlertTriangle, tone: metrics.openEvents > 0 ? 'attention' : 'safe' },
    { label: 'Event nghiêm trọng', value: metrics.criticalEvents, icon: Activity, tone: metrics.criticalEvents > 0 ? 'risk' : 'safe' },
    { label: 'Camera online', value: `${metrics.onlineCameras}/${metrics.totalCameras}`, icon: Camera, tone: 'safe' },
  ]

  return (
    <div className="farm-control">
      <header className="farm-control__hero">
        <div>
          <span className="farm-control__eyebrow">Dành cho chủ trại</span>
          <h1>Bảng điều khiển chủ trại</h1>
          <p>Tổng quan ATSH, bản đồ trang trại và vi phạm — đơn giản, dễ hiểu.</p>
        </div>
        <div className={`farm-control__live${connected ? ' farm-control__live--on' : ''}`}>
          {connected ? <Wifi size={16} /> : <WifiOff size={16} />}
          <span>{connected ? 'Cập nhật thời gian thực' : 'Đang kết nối WebSocket...'}</span>
          <small>{metrics.totalEventsToday} sự kiện hôm nay</small>
        </div>
      </header>

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

      {activeTab === 'ban-do' ? (
        <SmartFarmDesigner embedded />
      ) : (
        <>
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

          <div className="farm-control__layout">
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
                {mapData.zones.map((zone) => (
                  <div
                    key={zone.id}
                    className={`farm-control-zone farm-control-zone--${zone.risk}`}
                    style={{
                      left: `${zone.x}%`,
                      top: `${zone.y}%`,
                      width: `${zone.width}%`,
                      height: `${zone.height}%`,
                      transform: zone.rotation ? `rotate(${zone.rotation}deg)` : undefined,
                    }}
                  >
                    <strong>{zone.name}</strong>
                    <small>{RISK_LABELS[zone.risk]}</small>
                  </div>
                ))}
                {mapData.cameras.map((cam) => (
                  <div
                    key={cam.id}
                    className={`farm-control-camera farm-control-camera--${cam.status === 'online' ? 'online' : 'offline'}`}
                    style={{ left: `${cam.x + cam.width / 2}%`, top: `${cam.y + cam.height / 2}%` }}
                    title={cam.name}
                  />
                ))}
              </div>
            </section>

            <aside className="farm-control__score panel">
              <h2>Điểm ATSH</h2>
              <p>Bắt đầu 100 điểm · Trừ theo vi phạm hôm nay</p>
              <div className={`farm-score-ring farm-score-ring--${scoreTone}`}>
                <strong>{atshScore}</strong>
                <span>/ 100</span>
              </div>
              <ul className="farm-deductions">
                {deductions.map((item) => (
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
          </div>

          <section className="farm-control__tops">
            {[
              ['Top khu vực vi phạm', topZones],
              ['Top camera vi phạm', topCameras],
              ['Top quy tắc bị vi phạm', topRules],
            ].map(([title, items]) => (
              <article key={title} className="farm-top panel">
                <h2>{title}</h2>
                <ul>
                  {items.map((item, index) => (
                    <li key={`${item.name}-${index}`}>
                      <span>{index + 1}. {item.name}</span>
                      <strong>{item.count}</strong>
                    </li>
                  ))}
                </ul>
              </article>
            ))}
          </section>

          <section className="panel panel--compact farm-control__events">
            <div className="panel__header">
              <h2>Sự kiện AI realtime</h2>
              <span className={`realtime-feed__status${connected ? ' realtime-feed__status--online' : ''}`}>
                {connected ? 'Live' : 'Reconnecting...'}
              </span>
            </div>
            {eventsLoading && feedEvents.length === 0 ? (
              <p className="realtime-feed__empty">Đang tải sự kiện...</p>
            ) : null}
            {feedEvents.length === 0 && !eventsLoading ? (
              <p className="realtime-feed__empty">Chưa có sự kiện AI.</p>
            ) : (
              <ul className="realtime-feed__list">
                {feedEvents.slice(0, 8).map((event) => (
                  <li key={event.id} className="realtime-feed__item">
                    <strong>{event.typeLabel || event.eventType}</strong>
                    <span>{event.zoneName || event.cameraName}</span>
                    <small>{event.occurredAt ? new Date(event.occurredAt).toLocaleString('vi-VN') : `${event.date} ${event.time}`}</small>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="farm-control__chart panel panel--chart">
            <div className="panel__header">
              <div>
                <h2>Biểu đồ vi phạm</h2>
                <p>Theo dõi xu hướng vi phạm ATSH</p>
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
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="4 4" stroke="#e5e7eb" />
                  <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="value" stroke="#0B6B1B" strokeWidth={3} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </section>
        </>
      )}
    </div>
  )
}

export default FarmControlDashboardPage
