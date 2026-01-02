<template>
  <div class="login-container">
    <div class="login-card geek-card">
      <div class="login-header">
        <h2 class="app-title">Smart Community</h2>
        <p class="sub-text">请登录您的账号</p>
      </div>
      <el-form :model="form" @keyup.enter="handleLogin" label-position="top" size="large">
        <el-form-item label="账号">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名" 
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item label="密码">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-button 
          type="primary" 
          class="login-btn" 
          :loading="loading" 
          @click="handleLogin"
        >
          立即登录
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/auth'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const form = ref({ username: '', password: '' })

onMounted(() => {
  document.documentElement.classList.remove('dark')
})

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  
  loading.value = true
  try {
    const res = await login(form.value)
    ElMessage.success(`欢迎回来, ${res.username}`)
    
    sessionStorage.setItem('user_info', JSON.stringify(res))

    if (res.role === 'admin') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }

    router.push('/')
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5; 
  background-image: radial-gradient(#e0e0e0 1px, transparent 1px);
  background-size: 20px 20px;
}
.login-card {
  width: 400px;
  padding: 40px;
  background-color: #ffffff;
  border: 1px solid #e4e7ed;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border-radius: 8px;
}
.app-title {
  text-align: center;
  color: #303133;
  font-weight: 700;
  margin-bottom: 5px;
  font-family: sans-serif;
}
.sub-text {
  text-align: center;
  color: #909399;
  font-size: 0.9rem;
  margin-bottom: 30px;
}
.login-btn {
  width: 100%;
  margin-top: 20px;
  font-weight: bold;
}
</style>