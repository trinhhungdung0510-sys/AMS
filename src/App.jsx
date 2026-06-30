import { RouterProvider } from 'react-router-dom'
import { router } from './routes/router'
import './App.css'
import './styles/ams-brand.css'
import './styles/ams-extensions.css'

function App() {
  return <RouterProvider router={router} />
}

export default App
