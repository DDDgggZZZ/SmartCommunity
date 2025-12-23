<template>
  <div class="user-container">
    <h2>业主信息列表</h2>
    
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="姓名" width="120" />
      <el-table-column prop="phone" label="电话" width="150" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="create_time" label="注册时间" width="180" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserList } from './api/user' // 引入接口

const tableData = ref([]) // 响应式数据

// 页面加载完成后自动执行
onMounted(async () => {
  try {
    // 调用后端接口
    const data = await getUserList()
    console.log("后端返回的数据:", data)
    tableData.value = data // 将数据赋值给表格
  } catch (error) {
    console.error("获取失败", error)
  }
})
</script>

<style scoped>
.user-container {
  padding: 20px;
}
</style>