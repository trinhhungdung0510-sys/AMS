export function formatDateTime(date, time) {
  const [year, month, day] = date.split('-')
  return `${time} · ${day}/${month}/${year}`
}

export function getRiskLabel(risk) {
  const labels = {
    online: 'Trực tuyến',
    warning: 'Cảnh báo',
    danger: 'Mức cao',
    offline: 'Ngoại tuyến',
  }

  return labels[risk] ?? 'Trực tuyến'
}

export function exportRowsAsExcel(filename, rows) {
  const header = Object.keys(rows[0] ?? {})
  const csv = [
    header.join('\t'),
    ...rows.map((row) => header.map((key) => String(row[key]).replaceAll('\t', ' ')).join('\t')),
  ].join('\n')

  const blob = new Blob([csv], { type: 'application/vnd.ms-excel;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
