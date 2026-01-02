import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../layout/AppLayout.vue'
import { ElMessage } from 'element-plus'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 1. 登录页 (无需权限)
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
    // 2. 主应用布局
    {
      path: '/',
      component: AppLayout,
      children: [
        // === 公共区域 (所有角色可见) ===
        {
          path: '',
          name: 'Dashboard',
          component: () => import('../views/Dashboard.vue'),
          // 允许 admin 和 staff 访问
          meta: { roles: ['admin', 'staff'] } 
        },
        
        // === 基础数据 (仅 Admin) ===
        {
          path: 'buildings',
          name: 'Buildings',
          component: () => import('../views/building/BuildingList.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'units',
          name: 'Units',
          component: () => import('../views/unit/UnitList.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'rooms',
          name: 'Rooms',
          component: () => import('../views/room/RoomList.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'parkings',
          name: 'Parkings',
          component: () => import('../views/parking/ParkingList.vue'),
          meta: { roles: ['admin'] }
        },

        // === 核心管理 (仅 Admin) ===
        {
          path: 'owners',
          name: 'Owners',
          component: () => import('../views/owner/OwnerList.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'users',
          name: 'System Users',
          component: () => import('../views/user/UserList.vue'),
          meta: { roles: ['admin'] }
        },

        // === 业务模块 (混合权限) ===
        
        // 公告：所有人可见
        {
          path: 'notices',
          name: 'Notices',
          component: () => import('../views/notice/NoticeList.vue'),
          meta: { roles: ['admin', 'staff'] }
        },
        
        // 费用类型配置：仅 Admin
        {
          path: 'fees/types',
          name: 'Fee Types',
          component: () => import('../views/fee/FeeTypeList.vue'),
          meta: { roles: ['admin'] }
        },
        
        // 账单：所有人 (页面内部逻辑区分：Admin看全部，Staff看自己)
        {
          path: 'fees/bills',
          name: 'Fee Bills',
          component: () => import('../views/fee/FeeBillList.vue'),
          meta: { roles: ['admin', 'staff'] }
        },
        
        // 报修：所有人
        {
          path: 'repairs',
          name: 'Repairs',
          component: () => import('../views/repair/RepairList.vue'),
          meta: { roles: ['admin', 'staff'] }
        }
      ]
    }
  ]
})

// === 全局路由守卫 (权限核心逻辑) ===
router.beforeEach((to, from, next) => {
  // 1. 读取 Session 中的用户信息
  const userStr = sessionStorage.getItem('user_info')
  const user = userStr ? JSON.parse(userStr) : null
  
  // 数据库默认角色是 'staff'，如果未定义则默认为 'staff' 以防万一
  const currentRole = user?.role || 'staff'

  // 2. 未登录拦截：尝试进入非登录页 -> 跳登录
  if (to.name !== 'Login' && !user) {
    next({ name: 'Login' })
    return
  }

  // 3. 已登录拦截：尝试进入登录页 -> 跳 Dashboard
  if (to.name === 'Login' && user) {
    next({ name: 'Dashboard' })
    return
  }

  // 4. 角色权限校验
  if (to.meta.roles) {
    // 检查当前用户的角色是否在路由允许的 roles 列表中
    if (!to.meta.roles.includes(currentRole)) {
      ElMessage.error(`Access Denied: Role '${currentRole}' implies insufficient permissions.`)
      // 这里的处理策略是：如果不匹配，尝试回退到 Dashboard；
      // 如果本来就是 Dashboard 进不去(理论上不应该)，则强制登出或留白。
      if (to.name !== 'Dashboard') {
        next({ name: 'Dashboard' })
      } else {
        // 极端情况：连 Dashboard 都不让进，那只能登出了
        sessionStorage.removeItem('user_info')
        next({ name: 'Login' })
      }
      return
    }
  }

  // 5. 放行
  next()
})

export default router