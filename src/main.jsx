import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { EventStoreProvider } from './context/EventStore.jsx'
import { NotificationProvider } from './providers/NotificationProvider.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <EventStoreProvider>
        <NotificationProvider>
          <App />
        </NotificationProvider>
      </EventStoreProvider>
    </AuthProvider>
  </StrictMode>,
)
