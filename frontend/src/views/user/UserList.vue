<template>
  <div class="user-list">
    <div class="geek-card">
       <h3 class="terminal-title">SYSTEM USERS</h3>
       <el-table :data="users" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="Username">
           <template #default="{ row }">
             <span style="color: var(--geek-success)">{{ row.username }}</span>
           </template>
        </el-table-column>
        <el-table-column prop="role" label="Role">
           <template #default="{ row }">
             <el-tag effect="dark" :type="row.role === 'admin' ? 'danger' : 'info'">{{ row.role }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column prop="created_at" label="Created At" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserList } from '@/api/user'

const users = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const data = await getUserList()
    users.value = data
  } finally {
    loading.value = false
  }
})
</script>