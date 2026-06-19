import { createContext, useContext, useEffect, useState } from 'react'
import {
  getCurrentUser,
  getToken,
  logout as authLogout,
} from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadUser() {
      const token = getToken()

      if (!token) {
        setLoading(false)
        return
      }

      try {
        const profile = await getCurrentUser()
        setUser(profile)
      } catch {
        authLogout()
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [])

  function logout() {
    authLogout()
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
