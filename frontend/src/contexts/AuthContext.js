import React, { createContext, useState, useContext, useEffect } from 'react'
import axios from 'axios'
import { API_URL, AUTH_URL, setToken, removeToken, getToken } from '../config'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Настройка перехватчика для обновления токена
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config

        // Если ошибка 401 и это не запрос на обновление токена
        if (error.response.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            // Пытаемся обновить токен
            const refreshToken = localStorage.getItem('refreshToken')
            if (!refreshToken) {
              throw new Error('Нет refresh токена')
            }

            const response = await axios.post(`${AUTH_URL}/jwt/refresh/`, {
              refresh: refreshToken
            })

            const { access } = response.data
            setToken(access)
            axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
            originalRequest.headers['Authorization'] = `Bearer ${access}`

            return axios(originalRequest)
          } catch (refreshError) {
            // Если не удалось обновить токен, выходим
            logout()
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(error)
      }
    )

    return () => {
      axios.interceptors.response.eject(interceptor)
    }
  }, [])

  // Проверяем токен при загрузке
  useEffect(() => {
    const token = getToken()
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${AUTH_URL}/users/me/`)
      setUser(response.data)
      setError(null)
    } catch (error) {
      console.error('Ошибка при получении данных пользователя:', error)
      setError(error.response?.data?.detail || 'Ошибка при получении данных пользователя')
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${AUTH_URL}/jwt/create/`, {
        email,
        password,
      })
      
      const { access, refresh } = response.data
      setToken(access)
      localStorage.setItem('refreshToken', refresh)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      await fetchUser()
      setError(null)
      return true
    } catch (error) {
      console.error('Ошибка при входе:', error)
      setError(error.response?.data?.detail || 'Ошибка при входе')
      return false
    }
  }

  const register = async (username, email, password) => {
    try {
      await axios.post(`${AUTH_URL}/users/`, {
        username,
        email,
        password,
      })
      setError(null)
      return true
    } catch (error) {
      console.error('Ошибка при регистрации:', error)
      setError(error.response?.data?.detail || 'Ошибка при регистрации')
      return false
    }
  }

  const logout = () => {
    removeToken()
    localStorage.removeItem('refreshToken')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
    setError(null)
  }

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth должен использоваться внутри AuthProvider')
  }
  return context
} 