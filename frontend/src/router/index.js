import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TaskList from '@/views/TaskList.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { forGuestsOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { forGuestsOnly: true  }
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: TaskList,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  if (isAuthenticated && to.meta.forGuestsOnly) {
    next('/tasks')
    return
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  next()
})

export default router
