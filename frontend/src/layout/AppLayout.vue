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
        text-color="#8b949e"
        active-text-color="#58a6ff"
        style="border-right: none;"
      >
        <el-menu-item index="/">
          <el-icon><Odometer /></el-icon>
          <span>Dashboard</span>
        </el-menu-item>
        
        <el-menu-item index="/buildings">
          <el-icon><OfficeBuilding /></el-icon>
          <span>Buildings</span>
        </el-menu-item>

        <el-menu-item index="/units">
          <el-icon><Connection /></el-icon>
          <span>Units</span>
        </el-menu-item>

        <el-menu-item index="/rooms">
          <el-icon><House /></el-icon>
          <span>Rooms</span>
        </el-menu-item>

        <el-menu-item index="/parkings">
          <el-icon><Van /></el-icon>
          <span>Parkings</span>
        </el-menu-item>

        <el-menu-item index="/owners">
          <el-icon><Avatar /></el-icon>
          <span>Owners</span>
        </el-menu-item>

        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>SysUsers</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <main class="main-content">
      <header class="header">
        <div class="breadcrumb">root@server: ~/{{ $route.name ? $route.name.toLowerCase().replace(/\s+/g, '_') : 'home' }}</div>
        <div class="user-status">● Online</div>
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
import { 
  Odometer, 
  OfficeBuilding, 
  User, 
  Connection, 
  House, 
  Van, 
  Avatar 
} from '@element-plus/icons-vue'
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  background-color: var(--geek-panel);
  border-right: 1px solid var(--geek-border);
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding-left: 20px;
  font-weight: bold;
  color: var(--geek-text);
  border-bottom: 1px solid var(--geek-border);
  font-size: 14px;
}

.terminal-title {
  font-family: 'Courier New', Courier, monospace;
  letter-spacing: 1px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--geek-bg);
}

.header {
  height: 60px;
  border-bottom: 1px solid var(--geek-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background-color: rgba(13, 17, 23, 0.8);
  backdrop-filter: blur(10px);
}

.breadcrumb {
  color: var(--geek-primary);
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
}

.user-status {
  color: var(--geek-success);
  font-size: 12px;
  text-shadow: 0 0 5px rgba(46, 160, 67, 0.5);
}

.content-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden; /* 防止动画过程中出现横向滚动条 */
}

/* ============================================
   Geek Style Page Transitions (Fade + Slide Up)
   ============================================ */

/* 进场初始状态：透明且下移 20px */
.fade-transform-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

/* 离场结束状态：透明且上移 20px */
.fade-transform-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 动画激活状态：使用贝塞尔曲线让运动更顺滑 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
</style>