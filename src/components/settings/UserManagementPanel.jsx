import { useMemo, useState } from 'react'
import { Lock, Pencil, Plus, Unlock, UserPlus } from 'lucide-react'
import { usePermissions } from '../../hooks/usePermissions'
import { createUser, updateUser } from '../../services/userService'

const ROLE_OPTIONS = [
  ['FARM_ADMIN', 'Chủ trại'],
  ['VIEWER', 'Chỉ xem'],
]

const EMPTY_FORM = {
  email: '',
  full_name: '',
  password: '',
  role: 'VIEWER',
}

function UserManagementPanel({ users, onUsersChange, onStatus }) {
  const { hasPermission } = usePermissions()
  const canManage = hasPermission('users.manage_own_farm')
  const canRead = hasPermission('users.read')
  const [formOpen, setFormOpen] = useState(false)
  const [editingUser, setEditingUser] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)

  const sortedUsers = useMemo(
    () => [...(users || [])].sort((a, b) => String(a.full_name).localeCompare(String(b.full_name))),
    [users],
  )

  if (!canRead) {
    return <p className="panel__meta">Bạn không có quyền xem danh sách người dùng.</p>
  }

  const openCreate = () => {
    setEditingUser(null)
    setForm(EMPTY_FORM)
    setFormOpen(true)
  }

  const openEdit = (user) => {
    setEditingUser(user)
    setForm({
      email: user.email,
      full_name: user.full_name,
      password: '',
      role: user.role,
    })
    setFormOpen(true)
  }

  const closeForm = () => {
    setFormOpen(false)
    setEditingUser(null)
    setForm(EMPTY_FORM)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!canManage) return

    setSaving(true)
    try {
      if (editingUser) {
        const payload = {
          full_name: form.full_name.trim(),
          role: form.role,
        }
        if (form.password.trim()) {
          payload.password = form.password
        }
        const updated = await updateUser(editingUser.id, payload)
        onUsersChange((current) => current.map((item) => (item.id === updated.id ? updated : item)))
        onStatus?.(`Đã cập nhật ${updated.full_name}`)
      } else {
        const created = await createUser({
          email: form.email.trim(),
          full_name: form.full_name.trim(),
          password: form.password,
          role: form.role,
        })
        onUsersChange((current) => [...current, created])
        onStatus?.(`Đã thêm ${created.full_name}`)
      }
      closeForm()
    } catch (error) {
      onStatus?.(error instanceof Error ? error.message : 'Không lưu được người dùng')
    } finally {
      setSaving(false)
    }
  }

  const toggleActive = async (user) => {
    if (!canManage) return

    setSaving(true)
    try {
      const updated = await updateUser(user.id, { is_active: !user.is_active })
      onUsersChange((current) => current.map((item) => (item.id === updated.id ? updated : item)))
      onStatus?.(updated.is_active ? `Đã mở khóa ${updated.full_name}` : `Đã khóa ${updated.full_name}`)
    } catch (error) {
      onStatus?.(error instanceof Error ? error.message : 'Không cập nhật được trạng thái')
    } finally {
      setSaving(false)
    }
  }

  const resetPassword = async (user) => {
    if (!canManage) return
    const password = window.prompt(`Đặt mật khẩu mới cho ${user.full_name}:`, '')
    if (!password || password.length < 6) {
      if (password !== null) onStatus?.('Mật khẩu phải có ít nhất 6 ký tự')
      return
    }

    setSaving(true)
    try {
      await updateUser(user.id, { password })
      onStatus?.(`Đã đặt lại mật khẩu cho ${user.full_name}`)
    } catch (error) {
      onStatus?.(error instanceof Error ? error.message : 'Không đặt lại được mật khẩu')
    } finally {
      setSaving(false)
    }
  }

  return (
    <>
      <div className="panel__header">
        <div>
          <h2><UserPlus size={18} /> Danh sách người dùng</h2>
          <p>{sortedUsers.length} tài khoản · quản lý qua API `/users`</p>
        </div>
        {canManage ? (
          <button type="button" className="btn btn--primary btn--sm" onClick={openCreate} disabled={saving}>
            <Plus size={14} /> Thêm người dùng
          </button>
        ) : null}
      </div>

      <div className="settings-list">
        {sortedUsers.map((user) => (
          <div key={user.id} className="settings-list__item settings-list__item--actions">
            <div>
              <strong>{user.full_name}</strong>
              <span>{user.email} · {user.role}</span>
            </div>
            <div className="settings-list__item-controls">
              <span className={`status-tag status-tag--${user.is_active ? 'resolved' : 'new'}`}>
                {user.is_active ? 'Hoạt động' : 'Tạm khóa'}
              </span>
              {canManage ? (
                <>
                  <button type="button" className="btn btn--ghost btn--sm" onClick={() => openEdit(user)} disabled={saving}>
                    <Pencil size={14} /> Sửa
                  </button>
                  <button type="button" className="btn btn--ghost btn--sm" onClick={() => resetPassword(user)} disabled={saving}>
                    Mật khẩu
                  </button>
                  <button type="button" className="btn btn--outline btn--sm" onClick={() => toggleActive(user)} disabled={saving}>
                    {user.is_active ? <Lock size={14} /> : <Unlock size={14} />}
                    {user.is_active ? 'Khóa' : 'Mở khóa'}
                  </button>
                </>
              ) : null}
            </div>
          </div>
        ))}
        {!sortedUsers.length ? (
          <p className="panel__meta">Chưa tải được danh sách user từ API.</p>
        ) : null}
      </div>

      {formOpen ? (
        <div className="settings-modal" role="dialog" aria-modal="true">
          <button type="button" className="settings-modal__backdrop" onClick={closeForm} aria-label="Đóng" />
          <form className="settings-modal__panel panel" onSubmit={handleSubmit}>
            <h3>{editingUser ? 'Sửa người dùng' : 'Thêm người dùng'}</h3>
            {!editingUser ? (
              <label className="settings-form__label">
                <span>Email</span>
                <input
                  type="email"
                  required
                  className="settings-form__input"
                  value={form.email}
                  onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
                />
              </label>
            ) : null}
            <label className="settings-form__label">
              <span>Họ tên</span>
              <input
                type="text"
                required
                className="settings-form__input"
                value={form.full_name}
                onChange={(event) => setForm((prev) => ({ ...prev, full_name: event.target.value }))}
              />
            </label>
            <label className="settings-form__label">
              <span>{editingUser ? 'Mật khẩu mới (tùy chọn)' : 'Mật khẩu'}</span>
              <input
                type="password"
                required={!editingUser}
                minLength={6}
                className="settings-form__input"
                value={form.password}
                onChange={(event) => setForm((prev) => ({ ...prev, password: event.target.value }))}
              />
            </label>
            <label className="settings-form__label">
              <span>Vai trò</span>
              <select
                className="settings-form__input"
                value={form.role}
                onChange={(event) => setForm((prev) => ({ ...prev, role: event.target.value }))}
              >
                {ROLE_OPTIONS.map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </label>
            <div className="settings-modal__actions">
              <button type="button" className="btn btn--ghost" onClick={closeForm} disabled={saving}>Hủy</button>
              <button type="submit" className="btn btn--primary" disabled={saving}>
                {saving ? 'Đang lưu...' : 'Lưu'}
              </button>
            </div>
          </form>
        </div>
      ) : null}
    </>
  )
}

export default UserManagementPanel
