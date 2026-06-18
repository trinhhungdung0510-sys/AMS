import { BrowserRouter } from 'react-router-dom'
import AppRoutes from './routes/AppRoutes'
import './App.css'
import './styles/ams-brand.css'
import './styles/ams-extensions.css'

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  )
}

export default App
