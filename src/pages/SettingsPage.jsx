import { useState } from 'react'
import { Mail, Send, ShieldCheck, SlidersHorizontal, Users } from 'lucide-react'
import { Link } from 'react-router-dom'
import { alertSettings, cameras as initialCameras, severityLabels, users } from '../data/mockData'

function SettingsPage() {
  const [cameras, setCameras] = useState(initialCameras)

  const toggleEnabled = (id) => {
    setCameras((prev) =>
      prev.map((cam) => (cam.id === id ? { ...cam, enabled: !cam.enabled } : cam)),
    )
  }

  return (
    <div className="settings-page">
      <div className="settings-grid">
        <section className="panel">
          <div className="panel__header">
            <div>
              <h2><Users size={18} /> Danh sách người dùng</h2>
              <p>5 người dùng mẫu và trạng thái tài khoản</p>
            </div>
          </div>
          <div className="settings-list">
            {users.map((user) => (
              <div key={user.id} className="settings-list__item">
                <div>
                  <strong>{user.name}</strong>
                  <span>{user.email}</span>
                </div>
                <span className={`status-tag status-tag--${user.status === 'active' ? 'resolved' : 'new'}`}>
                  {user.status === 'active' ? 'Hoạt động' : 'Tạm khóa'}
                </span>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2><ShieldCheck size={18} /> Phân quyền</h2>
              <p>Vai trò và phạm vi truy cập</p>
            </div>
          </div>
          <div className="role-grid">
            {['Quản trị viên', 'Giám sát ca', 'Kỹ thuật camera', 'Thú y', 'Chỉ xem'].map((role) => (
              <div key={role} className="role-card">
                <strong>{role}</strong>
                <span>{role === 'Chỉ xem' ? 'Xem dữ liệu' : 'Xem, xử lý và cấu hình'}</span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="settings-sections">
        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Quản lý camera</h2>
              <p className="panel__desc">Bật/tắt và cấu hình camera trong hệ thống AMS</p>
            </div>
            <button type="button" className="btn btn--primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              Thêm camera
            </button>
            <Link to="/settings/zones" className="btn btn--outline">
              Zone Designer
            </Link>
          </div>

          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Mã</th>
                  <th>Tên camera</th>
                  <th>Khu vực</th>
                  <th>Địa chỉ IP</th>
                  <th>Độ phân giải</th>
                  <th>FPS</th>
                  <th>Trạng thái</th>
                  <th>Kích hoạt</th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {cameras.map((camera) => (
                  <tr key={camera.id}>
                    <td className="data-table__mono">{camera.id}</td>
                    <td className="data-table__desc">{camera.name}</td>
                    <td>{camera.zone}</td>
                    <td className="data-table__mono">{camera.ip}</td>
                    <td>{camera.resolution}</td>
                    <td>{camera.fps}</td>
                    <td>
                      <span className={`status-pill status-pill--${camera.status}`}>
                        {camera.status === 'online' ? 'Online' : 'Offline'}
                      </span>
                    </td>
                    <td>
                      <label className="toggle">
                        <input
                          type="checkbox"
                          checked={camera.enabled}
                          onChange={() => toggleEnabled(camera.id)}
                        />
                        <span className="toggle__slider" />
                      </label>
                    </td>
                    <td>
                      <div className="action-group">
                        <button type="button" className="btn-icon" aria-label="Chỉnh sửa">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                          </svg>
                        </button>
                        <button type="button" className="btn-icon btn-icon--danger" aria-label="Xóa">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polyline points="3 6 5 6 21 6" />
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title"><SlidersHorizontal size={18} /> Thiết lập cảnh báo</h2>
              <p className="panel__desc">Bật/tắt và ngưỡng tin cậy AI theo từng loại cảnh báo</p>
            </div>
          </div>
          <div className="settings-list">
            {alertSettings.map((setting) => (
              <div key={setting.id} className="settings-list__item">
                <div>
                  <strong>{setting.name}</strong>
                  <span>Ngưỡng: {setting.threshold} · Mức độ: {severityLabels[setting.severity]}</span>
                </div>
                <label className="toggle">
                  <input type="checkbox" defaultChecked={setting.enabled} />
                  <span className="toggle__slider" />
                </label>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Kênh nhận cảnh báo</h2>
              <p className="panel__desc">Email và Telegram nhận cảnh báo AI tức thời</p>
            </div>
          </div>
          <div className="settings-form">
            <label className="settings-form__label">
              <span><Mail size={15} /> Email nhận cảnh báo</span>
              <input type="email" className="settings-form__input" defaultValue="ops@ams-farm.vn" />
            </label>
            <label className="settings-form__label">
              <span><Send size={15} /> Telegram nhận cảnh báo</span>
              <input type="text" className="settings-form__input" defaultValue="@ams_farm_alerts" />
            </label>
            <div className="settings-form__actions">
              <button type="button" className="btn btn--outline">Gửi thử</button>
              <button type="button" className="btn btn--primary">Lưu cấu hình</button>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default SettingsPage
