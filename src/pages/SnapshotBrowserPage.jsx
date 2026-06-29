import EvidenceBrowserPanel from '../components/evidence/EvidenceBrowserPanel'

function SnapshotBrowserPage() {
  return (
    <div className="deployment-page">
      <header className="deployment-page__head">
        <h1>Bằng chứng</h1>
        <p>Duyệt bằng chứng vi phạm an toàn sinh học theo trang trại, camera, ngày và quy tắc</p>
      </header>
      <EvidenceBrowserPanel />
    </div>
  )
}

export default SnapshotBrowserPage
