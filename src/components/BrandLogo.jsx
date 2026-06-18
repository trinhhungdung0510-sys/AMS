import { Link } from 'react-router-dom'

export const LOGO_SRC = '/logo-ams.png'

export function BrandWordmark({ className = '', size = 'md' }) {
  const sizeClass = `brand-wordmark--${size}`

  return (
    <span className={`brand-wordmark ${sizeClass} ${className}`.trim()}>
      <span className="brand-wordmark__tin-nghia">TIN NGHIA</span>{' '}
      <span className="brand-wordmark__ams">AMS</span>
    </span>
  )
}

export function BrandLogo({
  className = '',
  imageClassName = '',
  height = 48,
  showWordmark = true,
  wordmarkSize = 'md',
  tagline,
  to = '/dashboard',
  onDark = false,
}) {
  const content = (
    <>
      <img
        src={LOGO_SRC}
        alt="TIN NGHIA AMS"
        className={`brand-logo__image ${imageClassName}`.trim()}
        style={{ height: `${height}px`, width: 'auto' }}
      />
      {(showWordmark || tagline) && (
        <div className={`brand-logo__text${onDark ? ' brand-logo__text--dark' : ''}`}>
          {showWordmark ? <BrandWordmark size={wordmarkSize} /> : null}
          {tagline ? <span className="brand-logo__tagline">{tagline}</span> : null}
        </div>
      )}
    </>
  )

  const rootClass = `brand-logo brand-logo--${wordmarkSize}${onDark ? ' brand-logo--dark' : ''} ${className}`.trim()

  if (to) {
    return (
      <Link to={to} className={rootClass} aria-label="TIN NGHIA AMS - về Tổng quan">
        {content}
      </Link>
    )
  }

  return <div className={rootClass}>{content}</div>
}

export default BrandLogo
