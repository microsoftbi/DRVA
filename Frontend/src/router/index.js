import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import StudentHome from '../views/StudentHome.vue'
import CoachHome from '../views/CoachHome.vue'
import AdminHome from '../views/AdminHome.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/student/home',
    name: 'StudentHome',
    component: StudentHome
  },
  {
    path: '/coach/home',
    name: 'CoachHome',
    component: CoachHome
  },
  {
    path: '/admin/home',
    name: 'AdminHome',
    component: AdminHome
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router