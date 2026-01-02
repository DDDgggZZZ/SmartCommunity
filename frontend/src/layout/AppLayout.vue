<template>
  <div class="layout-container">
    <aside class="sidebar">
      <div class="logo">
        <span class="terminal-title">SMART_COMMUNITY</span>
      </div>
      <el-menu
        router
        :default-active="$route.path"
        background-color="transparent"
        text-color="var(--geek-text-secondary)"
        active-text-color="var(--geek-primary)"
        style="border-right: none;"
      >
        <el-menu-item index="/">
          <el-icon><Odometer /></el-icon>
          <span>Dashboard</span>
        </el-menu-item>
        
        <el-sub-menu index="/base" v-if="role === 'admin'">
          <template #title>
            <el-icon><OfficeBuilding /></el-icon>
            <span>Base Data</span>
          </template>
          <el-menu-item index="/buildings">Buildings</el-menu-item>
          <el-menu-item index="/units">Units</el-menu-item>
          <el-menu-item index="/rooms">Rooms</el-menu-item>
          <el-menu-item index="/parkings">Parkings</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/owners" v-if="role === 'admin'">
          <el-icon><Avatar /></el-icon>
          <span>Owner Mgmt</span>
        </el-menu-item>

        <el-sub-menu index="/fees">
          <template #title>
            <el-icon><Money /></el-icon>
            <span>{{ role === 'admin' ? 'Fee Center' : 'My Fees' }}</span>
          </template>
          
          <el-menu-item index="/fees/types" v-if="role === 'admin'">Types Config</el-menu-item>
          
          <el-menu-item index="/fees/bills">
            {{ role === 'admin' ? 'All Bills' : 'My Bills' }}
          </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/notices">
          <el-icon><Bell /></el-icon>
          <span>Notices</span>
        </el-menu-item>

        <el-menu-item index="/repairs">
          <el-icon><Tools /></el-icon>
          <span>Repairs</span>
        </el-menu-item>

        <el-menu-item index="/users" v-if="role === 'admin'">
          <el-icon><User /></el-icon>
          <span>Sys Users</span>
        </el-menu-item>

        <el-menu-item @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
          <span>Logout</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <main class="main-content">
      <header class="header">
        <div class="breadcrumb">
          <span v-if="role === 'admin'" class="terminal-font">
            root@server: ~/{{ $route.name ? $route.name.toString().toLowerCase().replace(/\s+/g, '_') : 'home' }}
          </span>
          <span v-else>
            My Home / {{ $route.name }}
          </span>
        </div>
        <div class="user-status">
           ● {{ username }} [{{ role.toUpperCase() }}]
        </div>
      </header>
      <div class="content-body">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { 
  Odometer, OfficeBuilding, User, Avatar,
  Money, Bell, Tools, SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const role = ref('')
const username = ref('')

onMounted(() => {
  // 从 sessionStorage 恢复会话
  const userStr = sessionStorage.getItem('user_info')
  if (userStr) {
    const user = JSON.parse(userStr)
    role.value = user.role || 'staff' // 默认为 staff
    username.value = user.username
    
    // 强制确认主题 (Admin -> Dark, Staff -> Light)
    if (role.value === 'admin') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  } else {
    // 无会话信息，强制跳回登录
    router.push('/login')
  }
})

const handleLogout = () => {
  ElMessageBox.confirm(
    'End current session?', 
    'Logout', 
    { confirmButtonText: 'Yes', cancelButtonText: 'No', type: 'warning' }
  ).then(() => {
    // 清除会话
    sessionStorage.removeItem('user_info')
    // 恢复默认亮色主题
    document.documentElement.classList.remove('dark')
    // 跳转
    router.push('/login')
    ElMessage.success('Session ended')
  }).catch(() => {})
}
</script>

<style scoped>
/* 保持样式不变 */
.layout-container { display: flex; height: 100vh; width: 100vw; overflow: hidden; }
.sidebar { width: 240px; background-color: var(--geek-panel); border-right: 1px solid var(--geek-border); display: flex; flex-direction: column; transition: background-color 0.3s; }
.logo { height: 60px; display: flex; align-items: center; padding-left: 20px; font-weight: bold; color: var(--geek-text); border-bottom: 1px solid var(--geek-border); font-size: 14px; }
.terminal-title { font-family: 'Courier New', Courier, monospace; letter-spacing: 1px; }
.main-content { flex: 1; display: flex; flex-direction: column; background-color: var(--geek-bg); transition: background-color 0.3s; }
.header { height: 60px; border-bottom: 1px solid var(--geek-border); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; background-color: var(--geek-panel); backdrop-filter: blur(10px); }
.breadcrumb { color: var(--geek-primary); font-size: 14px; }
.terminal-font { font-family: 'Courier New', Courier, monospace; }
.user-status { color: var(--geek-success); font-size: 12px; }
.content-body { flex: 1; padding: 20px; overflow-y: auto; overflow-x: hidden; }
.fade-transform-enter-from { opacity: 0; transform: translateY(20px); }
.fade-transform-leave-to { opacity: 0; transform: translateY(-20px); }
.fade-transform-enter-active, .fade-transform-leave-active { transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); }
:deep(.el-menu) { border-right: none; }
:deep(.el-menu-item), :deep(.el-sub-menu__title) { color: var(--geek-text-secondary); }
:deep(.el-menu-item.is-active) { color: var(--geek-primary); background-color: rgba(64, 158, 255, 0.1); }
</style>