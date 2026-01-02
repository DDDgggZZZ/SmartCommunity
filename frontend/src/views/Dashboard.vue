<template>
  <div class="dashboard">
    <div class="welcome-banner geek-card">
      <h1 class="terminal-title">SYSTEM STATUS</h1>
      <p class="terminal-cursor">User: {{ username }} / Role: {{ role }}</p>
    </div>

    <div v-if="role === 'admin'" class="stats-grid">
      <div class="stat-card geek-card" v-for="(value, key) in stats" :key="key">
        <div class="stat-value">{{ value }}</div>
        <div class="stat-label">{{ formatKey(key) }}</div>
        <div class="stat-deco"></div>
      </div>
    </div>

    <div v-else class="user-panel geek-card">
      <h3>> Welcome to Smart Community</h3>
      <p style="color: var(--geek-text-secondary); margin-top: 10px;">
        You can check your bills, submit repair requests, and view community notices here.
      </p>
      <div style="margin-top: 30px; display: flex; gap: 20px; justify-content: center;">
        <el-button type="primary" @click="$router.push('/fees/bills')">My Bills</el-button>
        <el-button type="success" @click="$router.push('/repairs')">Repair Request</el-button>
      </div>
    </div>
    
    <div class="geek-card log-panel" style="margin-top: 20px;">
      <h3>> System Logs</h3>
      <div class="logs">
        <div class="log-item"><span class="log-time">[System]</span> Connection established.</div>
        <div class="log-item"><span class="log-time">[Auth]</span> Identity verified as {{ role }}.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboardStats } from '../api/dashboard'
import { useRouter } from 'vue-router'

const router = useRouter()
const stats = ref({})
const username = ref('User')
const role = ref('staff')

const formatKey = (key) => key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')

const loadData = async () => {
  // 只有管理员才去请求统计接口，节省资源且避免403错误
  if (role.value === 'admin') {
    try {
      const data = await getDashboardStats()
      stats.value = data
    } catch (e) {
      console.error("Failed to load stats", e)
    }
  }
}

onMounted(() => {
  const userStr = sessionStorage.getItem('user_info')
  if (userStr) {
    const user = JSON.parse(userStr)
    username.value = user.username
    role.value = user.role || 'staff'
  }
  loadData()
})
</script>

<style scoped>
.welcome-banner { margin-bottom: 20px; border-left: 4px solid var(--geek-success); padding: 20px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
.stat-card { text-align: center; padding: 30px; position: relative; overflow: hidden; }
.stat-value { font-size: 2.5rem; font-weight: bold; color: var(--geek-primary); }
.stat-label { color: #8b949e; margin-top: 10px; text-transform: uppercase; letter-spacing: 1px; }
.user-panel { padding: 40px; text-align: center; }
.log-panel { padding: 20px; }
.log-item { font-family: 'Courier New', monospace; color: #8b949e; margin-bottom: 5px; }
.log-time { color: var(--geek-success); margin-right: 10px; }
</style>