import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidCatch(error, info) {
    if (import.meta.env.DEV) {
      console.error('[ErrorBoundary]', error, info)
    }
  }

  render() {
    const { error } = this.state
    const { children, fallbackTitle = 'Không thể hiển thị nội dung' } = this.props

    if (error) {
      return (
        <div className="atsh-soc__empty panel" role="alert">
          <p className="atsh-soc__empty-title">{fallbackTitle}</p>
          <p>{error?.message || 'Đã xảy ra lỗi giao diện. Vui lòng tải lại trang.'}</p>
          <button
            type="button"
            className="btn btn--outline btn--sm"
            onClick={() => this.setState({ error: null })}
          >
            Thử lại
          </button>
        </div>
      )
    }

    return children
  }
}

export default ErrorBoundary
