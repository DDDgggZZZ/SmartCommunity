<template>
  <div class="dashboard">
    <div class="welcome-banner geek-card">
      <h1 class="terminal-title">SYSTEM READY...</h1>
      <p class="terminal-cursor">Welcome back, Admin. All systems operational.</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card geek-card" v-for="item in stats" :key="item.label">
        <div class="stat-value">{{ item.value }}</div>
        <div class="stat-label">{{ item.label }}</div>
        <div class="stat-deco"></div>
      </div>
    </div>
    
    <div class="geek-card log-panel">
      <h3>> System Logs</h3>
      <div class="logs">
        <div v-for="(log, i) in logs" :key="i" class="log-item">
          <span class="log-time">[{{ log.time }}]</span>
          <span class="log-msg">{{ log.msg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const stats = ref([
  { label: 'CPU LOAD', value: '12%' },
  { label: 'MEMORY', value: '4.2GB' },
  { label: 'NETWORK', value: '1.2Gbps' },
  { label: 'NODES', value: 'Online' }
])

const logs = ref([
  { time: '10:00:01', msg: 'System initialized successfully.' },
  { time: '10:00:05', msg: 'Connected to database @127.0.0.1.' },
  { time: '10:01:23', msg: 'User admin logged in.' },
  { time: '10:05:12', msg: 'Data synchronization complete.' },
])
</script>

<style scoped>
.welcome-banner {
  margin-bottom: 20px;
  border-left: 4px solid var(--geek-success);
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
  position: relative;
  overflow: hidden;
}
.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--geek-primary);
}
.stat-label {
  color: #8b949e;
  font-size: 0.8rem;
  margin-top: 5px;
}
.log-panel h3 {
  margin-top: 0;
  color: var(--geek-text);
  border-bottom: 1px solid var(--geek-border);
  padding-bottom: 10px;
}
.log-item {
  font-size: 0.9rem;
  margin-bottom: 5px;
}
.log-time {
  color: #8b949e;
  margin-right: 10px;
}
.log-msg {
  color: var(--geek-success);
}
</style>