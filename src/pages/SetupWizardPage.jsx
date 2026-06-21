import { useEffect, useState } from 'react'
import { CheckCircle2, Circle } from 'lucide-react'
import { createCamera, buildCameraPayload } from '../services/cameraService'
import {
  createCameraZone,
  createFarm,
  createUniform,
  fetchSetupStatus,
} from '../services/deploymentService'

const STEPS = [
  { id: 1, title: 'Tạo Farm', key: 'farm' },
  { id: 2, title: 'Thêm Camera', key: 'camera' },
  { id: 3, title: 'Tạo Zone', key: 'zone' },
  { id: 4, title: 'Gán Uniform', key: 'uniform' },
  { id: 5, title: 'Kiểm tra hệ thống', key: 'systemCheck' },
]

function SetupWizardPage() {
  const [step, setStep] = useState(1)
  const [status, setStatus] = useState(null)
  const [message, setMessage] = useState('')
  const [farmForm, setFarmForm] = useState({ id: 'FARM-001', name: 'AMS Farm', code: 'FARM-001', address: '' })
  const [cameraForm, setCameraForm] = useState({
    id: 'CAM-001',
    name: 'Camera Cổng trại',
    farm_id: 'FARM-001',
    zone: 'farm_gate',
    ip: '192.168.1.100',
    port: 554,
    resolution: '1080p',
    fps: 25,
  })
  const [zoneForm, setZoneForm] = useState({
    cameraId: 'CAM-001',
    name: 'Vùng giám sát cổng',
    type: 'monitoring',
    color: '#16a34a',
    points: [{ x: 0.1, y: 0.1 }, { x: 0.9, y: 0.1 }, { x: 0.9, y: 0.9 }, { x: 0.1, y: 0.9 }],
  })
  const [uniformForm, setUniformForm] = useState({ name: 'Đồng phục vùng sạch', farm_id: 'FARM-001' })

  useEffect(() => {
    fetchSetupStatus().then(setStatus).catch(() => setStatus(null))
  }, [step, message])

  const refresh = async () => {
    const next = await fetchSetupStatus()
    setStatus(next)
  }

  const handleFarm = async () => {
    try {
      await createFarm({
        id: farmForm.id,
        name: farmForm.name,
        code: farmForm.code,
        address: farmForm.address,
        location: farmForm.address,
      })
      setMessage('Đã tạo farm')
      await refresh()
      setStep(2)
    } catch (error) {
      setMessage(error.message)
    }
  }

  const handleCamera = async () => {
    try {
      await createCamera(buildCameraPayload(cameraForm))
      setMessage('Đã thêm camera')
      setZoneForm((prev) => ({ ...prev, cameraId: cameraForm.id }))
      await refresh()
      setStep(3)
    } catch (error) {
      setMessage(error.message)
    }
  }

  const handleZone = async () => {
    try {
      await createCameraZone(zoneForm.cameraId, {
        name: zoneForm.name,
        type: zoneForm.type,
        color: zoneForm.color,
        points: zoneForm.points,
        reference_width: 1920,
        reference_height: 1080,
      })
      setMessage('Đã tạo zone')
      await refresh()
      setStep(4)
    } catch (error) {
      setMessage(error.message)
    }
  }

  const handleUniform = async () => {
    try {
      await createUniform(uniformForm)
      setMessage('Đã tạo uniform template')
      await refresh()
      setStep(5)
    } catch (error) {
      setMessage(error.message)
    }
  }

  return (
    <div className="deployment-page">
      <header className="deployment-page__head">
        <h1>Setup Wizard</h1>
        <p>Cài đặt AMS trong 5 bước — triển khai trong 1 ngày</p>
      </header>

      <ol className="setup-steps">
        {STEPS.map((item) => (
          <li key={item.id} className={`setup-steps__item${step === item.id ? ' setup-steps__item--active' : ''}`}>
            {status?.steps?.[item.key]?.completed ? <CheckCircle2 size={18} /> : <Circle size={18} />}
            <span>{item.title}</span>
          </li>
        ))}
      </ol>

      {message ? <p className="panel__meta">{message}</p> : null}

      {step === 1 ? (
        <section className="panel setup-panel">
          <h2>Bước 1 — Tạo Farm</h2>
          <label>Mã farm<input value={farmForm.id} onChange={(e) => setFarmForm({ ...farmForm, id: e.target.value })} /></label>
          <label>Tên farm<input value={farmForm.name} onChange={(e) => setFarmForm({ ...farmForm, name: e.target.value })} /></label>
          <label>Địa chỉ<input value={farmForm.address} onChange={(e) => setFarmForm({ ...farmForm, address: e.target.value })} /></label>
          <button type="button" className="btn btn--primary" onClick={handleFarm}>Tạo Farm</button>
        </section>
      ) : null}

      {step === 2 ? (
        <section className="panel setup-panel">
          <h2>Bước 2 — Thêm Camera</h2>
          <label>Mã camera<input value={cameraForm.id} onChange={(e) => setCameraForm({ ...cameraForm, id: e.target.value })} /></label>
          <label>Tên<input value={cameraForm.name} onChange={(e) => setCameraForm({ ...cameraForm, name: e.target.value })} /></label>
          <label>IP<input value={cameraForm.ip} onChange={(e) => setCameraForm({ ...cameraForm, ip: e.target.value })} /></label>
          <button type="button" className="btn btn--primary" onClick={handleCamera}>Thêm Camera</button>
        </section>
      ) : null}

      {step === 3 ? (
        <section className="panel setup-panel">
          <h2>Bước 3 — Tạo Zone</h2>
          <label>Camera ID<input value={zoneForm.cameraId} onChange={(e) => setZoneForm({ ...zoneForm, cameraId: e.target.value })} /></label>
          <label>Tên zone<input value={zoneForm.name} onChange={(e) => setZoneForm({ ...zoneForm, name: e.target.value })} /></label>
          <button type="button" className="btn btn--primary" onClick={handleZone}>Tạo Zone</button>
        </section>
      ) : null}

      {step === 4 ? (
        <section className="panel setup-panel">
          <h2>Bước 4 — Gán Uniform</h2>
          <label>Tên uniform<input value={uniformForm.name} onChange={(e) => setUniformForm({ ...uniformForm, name: e.target.value })} /></label>
          <button type="button" className="btn btn--primary" onClick={handleUniform}>Tạo Uniform</button>
        </section>
      ) : null}

      {step === 5 ? (
        <section className="panel setup-panel">
          <h2>Bước 5 — Kiểm tra hệ thống</h2>
          <pre className="deployment-pre">{JSON.stringify(status?.health || status, null, 2)}</pre>
          <button type="button" className="btn btn--outline" onClick={refresh}>Chạy lại kiểm tra</button>
        </section>
      ) : null}
    </div>
  )
}

export default SetupWizardPage
