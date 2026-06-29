import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { DashboardBootstrapProvider } from './context/DashboardBootstrapStore.jsx'
import { EventStoreProvider } from './context/EventStore.jsx'
import { NotificationProvider } from './providers/NotificationProvider.jsx'
import { ViolationProcessingProvider } from './context/ViolationProcessingContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <DashboardBootstrapProvider>
        <EventStoreProvider>
          <ViolationProcessingProvider>
            <NotificationProvider>
              <App />
            </NotificationProvider>
          </ViolationProcessingProvider>
        </EventStoreProvider>
      </DashboardBootstrapProvider>
    </AuthProvider>
  </StrictMode>,
)
