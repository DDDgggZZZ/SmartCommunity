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
          name: 'Buildings',
          component: () => import('../views/building/BuildingList.vue')
        },
        {
          path: 'units',
          name: 'Units',
          component: () => import('../views/unit/UnitList.vue')
        },
        {
          path: 'rooms',
          name: 'Rooms',
          component: () => import('../views/room/RoomList.vue')
        },
        {
          path: 'parkings',
          name: 'Parkings',
          component: () => import('../views/parking/ParkingList.vue')
        },
        {
          path: 'owners',
          name: 'Owners',
          component: () => import('../views/owner/OwnerList.vue')
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