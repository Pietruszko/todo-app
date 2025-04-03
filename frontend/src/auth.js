import axios from 'axios'

const api = axios.create({
    baseURL: 'https://todo-app-5v21.onrender.com/api',
    headers: {
        'Content-Type': 'application/json',
    }
})

const SKIP_AUTH_URLS = ['register', 'login']

api.interceptors.request.use(config => {
    if (SKIP_AUTH_URLS.some(url => config.url.includes(url))) {
        return config
      }
    
      // Add token for all other requests
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
})

export default api