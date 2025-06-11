export const API_URL = 'http://localhost:8000/api'
export const AUTH_URL = `${API_URL}/auth`

// Настройки для axios
export const axiosConfig = {
  headers: {
    'Content-Type': 'application/json',
  },
}

// Функция для получения токена из localStorage
export const getToken = () => {
  return localStorage.getItem('token')
}

// Функция для установки токена в localStorage
export const setToken = (token) => {
  localStorage.setItem('token', token)
}

// Функция для удаления токена
export const removeToken = () => {
  localStorage.removeItem('token')
}

// Функция для проверки, авторизован ли пользователь
export const isAuthenticated = () => {
  return !!getToken()
} 