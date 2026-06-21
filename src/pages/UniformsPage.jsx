import { useEffect, useState } from 'react'
import { RefreshCw, Shirt, Trash2 } from 'lucide-react'
import UniformInUseDialog from '../components/uniforms/UniformInUseDialog'
import { deleteUniform, listUniforms, UniformInUseError } from '../services/uniformService'

function UniformsPage() {
  const [uniforms, setUniforms] = useState([])
  const [loading, setLoading] = useState(true)
  const [status, setStatus] = useState('')
  const [blockedZones, setBlockedZones] = useState([])
  const [showBlockedDialog, setShowBlockedDialog] = useState(false)

  const loadUniforms = async () => {
    setLoading(true)
    try {
      const data = await listUniforms()
      setUniforms(data)
      setStatus(`${data.length} uniform`)
    } catch (error) {
      setStatus(error.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadUniforms()
  }, [])

  const handleDelete = async (uniform) => {
    if (!window.confirm(`Xóa uniform "${uniform.name}"?`)) return

    try {
      await deleteUniform(uniform.id)
      setUniforms((prev) => prev.filter((item) => item.id !== uniform.id))
      setStatus(`Đã xóa: ${uniform.name}`)
    } catch (error) {
      if (error instanceof UniformInUseError) {
        setBlockedZones(error.zones)
        setShowBlockedDialog(true)
        return
      }
      setStatus(error.message)
    }
  }

  return (
    <div className="page page--uniforms">
      <header className="page__header">
        <div>
          <h1>Đồng phục (Uniform)</h1>
          <p>Quản lý template đồng phục cho các vùng ATSH.</p>
        </div>
        <button type="button" className="btn btn--outline" onClick={loadUniforms}>
          <RefreshCw size={16} />
          Tải lại
        </button>
      </header>

      {status ? <p className="page__status">{status}</p> : null}

      {loading ? (
        <p>Đang tải...</p>
      ) : uniforms.length === 0 ? (
        <p>Chưa có uniform nào.</p>
      ) : (
        <div className="uniforms-list">
          {uniforms.map((uniform) => (
            <article key={uniform.id} className="uniforms-list__item">
              <div className="uniforms-list__icon">
                <Shirt size={20} />
              </div>
              <div className="uniforms-list__body">
                <h2>{uniform.name}</h2>
                <p>{uniform.description || '—'}</p>
                <span className="uniforms-list__meta">{uniform.id}</span>
              </div>
              <button
                type="button"
                className="btn btn--outline btn--danger"
                onClick={() => handleDelete(uniform)}
                aria-label={`Xóa ${uniform.name}`}
              >
                <Trash2 size={16} />
                Xóa
              </button>
            </article>
          ))}
        </div>
      )}

      <UniformInUseDialog
        open={showBlockedDialog}
        zones={blockedZones}
        onClose={() => setShowBlockedDialog(false)}
      />
    </div>
  )
}

export default UniformsPage
