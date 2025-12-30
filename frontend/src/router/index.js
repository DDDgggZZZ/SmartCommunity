import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../layout/AppLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'Dashboard',
          component: () => import('../views/Dashboard.vue')
        },
        {
          path: 'buildings',
          name: 'Building Manager',
          component: () => import('../views/building/BuildingList.vue')
        },
        {
          path: 'users',
          name: 'System Users',
          component: () => import('../views/user/UserList.vue')
        }
      ]
    }
  ]
})

export default router