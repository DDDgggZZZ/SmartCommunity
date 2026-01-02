<template>
  <div class="page-container">
    <div class="geek-card">
      <div class="card-header">
        <h3 class="title">> System Notices</h3>
        <el-button v-if="role === 'admin'" type="primary" @click="openDialog()">Publish New</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="Title" width="200" />
        <el-table-column prop="content" label="Content" show-overflow-tooltip />
        <el-table-column prop="publish_time" label="Publish Time" width="180" />
        
        <el-table-column label="Operations" width="180" v-if="role === 'admin'">
          <template #default="scope">
            <el-button type="primary" link @click="openDialog(scope.row)">Edit</el-button>
            <el-button type="danger" link @click="handleDelete(scope.row.id)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? 'Edit Notice' : 'New Notice'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="Title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="Content">
          <el-input v-model="form.content" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="Time">
          <el-date-picker 
            v-model="form.publish_time" 
            type="datetime" 
            value-format="YYYY-MM-DD HH:mm:ss" 
            placeholder="Select date and time"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getNoticeList, createNotice, updateNotice, deleteNotice } from '../../api/notice'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const form = ref({})
const role = ref('staff')

const loadData = async () => {
  loading.value = true
  try {
    tableData.value = await getNoticeList()
  } finally {
    loading.value = false
  }
}

const openDialog = (row = {}) => {
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.title || !form.value.content) {
    ElMessage.error('Title and content are required')
    return
  }
  
  try {
    if (form.value.id) {
      // ★ 关键：只提取需要修改的字段，避免发送 created_at 等干扰字段
      const updateData = {
        title: form.value.title,
        content: form.value.content,
        publish_time: form.value.publish_time
      }
      await updateNotice(form.value.id, updateData)
      ElMessage.success('Updated')
    } else {
      await createNotice(form.value)
      ElMessage.success('Published')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('Are you sure to delete?', 'Warning', { type: 'warning' })
    .then(async () => {
      await deleteNotice(id)
      ElMessage.success('Deleted')
      loadData()
    })
    .catch(() => {})
}

onMounted(() => {
  const userStr = sessionStorage.getItem('user_info')
  if (userStr) {
    role.value = JSON.parse(userStr).role || 'staff'
  }
  loadData()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.title { margin: 0; color: var(--geek-text); }
</style>