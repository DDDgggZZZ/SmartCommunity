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
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>SysUsers</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <main class="main-content">
      <header class="header">
        <div class="breadcrumb">root@server: ~/{{ $route.name }}</div>
        <div class="user-status">● Online</div>
      </header>
      <div class="content-body">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { Odometer, OfficeBuilding, User } from '@element-plus/icons-vue'
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
  font-size: 14px;
}

.user-status {
  color: var(--geek-success);
  font-size: 12px;
}

.content-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>