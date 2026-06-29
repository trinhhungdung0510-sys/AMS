import { useEffect, useMemo, useState } from 'react'
import { GitBranch, ShieldCheck } from 'lucide-react'
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { API_BASE_URL } from '../../config/api'
import { useDashboardBootstrap } from '../../context/DashboardBootstrapStore'

function hasComplianceData({ complianceRate, completedTracks, violatedTracks, violationsToday, trendData }) {
  const hasMetrics =
    complianceRate != null ||
    completedTracks != null ||
    violatedTracks != null ||
    violationsToday != null

  return hasMetrics || (trendData?.length ?? 0) > 0
}

function BiosecurityCompliancePanel() {
  const { data, loading: bootstrapLoading } = useDashboardBootstrap()
  const workflowCompliance = data?.workflowSummary?.compliance ?? null
  const atshSummary = data?.dashboardSummary ?? null
  const complianceKpis = data?.complianceSummary?.kpis ?? null

  const [summary, setSummary] = useState(null)
  const [trendData, setTrendData] = useState([])
  const [apiLoading, setApiLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    async function loadComplianceTrends() {
      setApiLoading(true)
      try {
        const [summaryRes, trendsRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/compliance/summary`),
          fetch(`${API_BASE_URL}/api/compliance/trends`),
        ])

        if (cancelled) return

        if (summaryRes.ok) {
          setSummary(await summaryRes.json())
        } else {
          setSummary(null)
        }

        if (trendsRes.ok) {
          const trends = await trendsRes.json()
          setTrendData(trends.xu_huong_7_ngay || [])
        } else {
          setTrendData([])
        }
      } catch {
        if (!cancelled) {
          setSummary(null)
          setTrendData([])
        }
      } finally {
        if (!cancelled) setApiLoading(false)
      }
    }

    loadComplianceTrends()
    return () => {
      cancelled = true
    }
  }, [])

  const complianceRate =
    workflowCompliance?.compliance_score ??
    summary?.diem_atsh ??
    complianceKpis?.complianceScore ??
    null

  const completedTracks = workflowCompliance?.compliant_tracks ?? null
  const violatedTracks = workflowCompliance?.violation_count ?? null
  const violationsToday =
    summary?.vi_pham_hom_nay ??
    atshSummary?.vi_pham_atsh_hom_nay ??
    complianceKpis?.totalViolationsToday ??
    null

  const loading = bootstrapLoading || apiLoading
  const showData = hasComplianceData({
    complianceRate,
    completedTracks,
    violatedTracks,
    violationsToday,
    trendData,
  })

  const chartData = useMemo(
    () =>
      trendData.map((item) => ({
        ngay: item.ngay?.slice(5) || item.ngay,
        vi_pham: item.vi_pham,
      })),
    [trendData],
  )

  return (
    <section className="panel panel--workflow biosecurity-compliance-panel">
      <div className="panel__header">
        <div>
          <h2>Tuân thủ an toàn sinh học</h2>
          <p>Tổng hợp tuân thủ quy trình và vi phạm ATSH</p>
        </div>
        <span className="panel__badge panel__badge--score">
          <ShieldCheck size={16} />
          {complianceRate != null ? `${complianceRate}%` : '--'}
        </span>
      </div>

      {loading ? (
        <p className="crossing-list__empty">Đang tải dữ liệu tuân thủ…</p>
      ) : !showData ? (
        <p className="crossing-list__empty">Chưa có dữ liệu</p>
      ) : (
        <>
          <div className="workflow-stats biosecurity-compliance-panel__stats">
            <div>
              <strong>{complianceRate ?? '--'}{complianceRate != null ? '%' : ''}</strong>
              <span>Tỷ lệ tuân thủ</span>
            </div>
            <div>
              <strong>{completedTracks ?? '--'}</strong>
              <span>Số quy trình hoàn thành</span>
            </div>
            <div>
              <strong>{violatedTracks ?? '--'}</strong>
              <span>Số quy trình vi phạm</span>
            </div>
            <div>
              <strong>{violationsToday ?? '--'}</strong>
              <span>Số vi phạm hôm nay</span>
            </div>
          </div>

          <div className="biosecurity-compliance-panel__trend">
            <div className="biosecurity-compliance-panel__trend-head">
              <GitBranch size={16} />
              <strong>Xu hướng 7 ngày</strong>
            </div>
            {chartData.length === 0 ? (
              <p className="crossing-list__empty">Chưa có dữ liệu xu hướng.</p>
            ) : (
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={chartData}>
                  <XAxis dataKey="ngay" tickLine={false} axisLine={false} />
                  <YAxis tickLine={false} axisLine={false} allowDecimals={false} />
                  <Tooltip />
                  <Line type="monotone" dataKey="vi_pham" stroke="#ef4444" strokeWidth={3} dot={{ r: 3 }} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </>
      )}
    </section>
  )
}

export default BiosecurityCompliancePanel
