<template>
  <div class="page-container">
    <div class="geek-card">
      <div class="card-header">
        <h3 class="title">> Repair Tickets</h3>
        <el-button v-if="role === 'staff'" type="warning" @click="showSubmitDialog = true">Submit Ticket</el-button>
        <el-tag v-else type="info">Admin Mode: Process Only</el-tag>
      </div>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="owner_id" label="Owner ID" width="100" />
        <el-table-column prop="content" label="Issue Description" show-overflow-tooltip />
        <el-table-column prop="status" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="Created At" width="170" />
        <el-table-column prop="feedback" label="Feedback" show-overflow-tooltip />
        <el-table-column label="Process" width="150" v-if="role === 'admin'">
          <template #default="{ row }">
            <el-button 
              v-if="row.status === '待处理'" 
              type="primary" 
              size="small" 
              @click="openProcess(row, '处理中')"
            >Start</el-button>
            <el-button 
              v-if="row.status === '处理中'" 
              type="success" 
              size="small" 
              @click="openProcess(row, '完成')"
            >Finish</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="showSubmitDialog" title="Submit Repair Ticket" width="500px">
      <el-form :model="submitForm" label-width="100px">
        <el-form-item label="Owner ID">
          <el-input v-model="submitForm.owner_id" placeholder="Enter Owner ID" />
        </el-form-item>
        <el-form-item label="Content">
          <el-input v-model="submitForm.content" type="textarea" :rows="3" placeholder="Describe the issue..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSubmitDialog = false">Cancel</el-button>
        <el-button type="warning" @click="handleSubmit">Submit</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showProcessDialog" :title="`Update Status`" width="500px">
      <el-form :model="processForm">
        <el-form-item label="Feedback" v-if="processForm.status === '完成'">
          <el-input v-model="processForm.feedback" type="textarea" placeholder="Repair result / feedback..." />
        </el-form-item>
        <p v-else>Confirm to start processing this ticket?</p>
      </el-form>
      <template #footer>
        <el-button @click="showProcessDialog = false">Cancel</el-button>
        <el-button type="primary" @click="handleUpdateStatus">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRepairList, submitRepair, updateRepairStatus } from '../../api/repair'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const role = ref('staff')

// 提交相关
const showSubmitDialog = ref(false)
const submitForm = ref({ owner_id: '', content: '' })

// 处理相关
const showProcessDialog = ref(false)
const processForm = ref({ id: null, status: '', feedback: '' })

const loadData = async () => {
  loading.value = true
  try {
    tableData.value = await getRepairList({})
  } finally {
    loading.value = false
  }
}

const getStatusType = (status) => {
  if (status === '待处理') return 'info'
  if (status === '处理中') return 'warning'
  if (status === '完成') return 'success'
  return ''
}

const handleSubmit = async () => {
  if (!submitForm.value.owner_id || !submitForm.value.content) {
    ElMessage.error('Required fields missing')
    return
  }
  await submitRepair(submitForm.value)
  ElMessage.success('Ticket Submitted')
  showSubmitDialog.value = false
  submitForm.value = { owner_id: '', content: '' }
  loadData()
}

const openProcess = (row, nextStatus) => {
  processForm.value = { id: row.id, status: nextStatus, feedback: '' }
  showProcessDialog.value = true
}

const handleUpdateStatus = async () => {
  if (processForm.value.status === '完成' && !processForm.value.feedback) {
    ElMessage.error('Feedback is required when finishing a repair')
    return
  }
  await updateRepairStatus(processForm.value.id, {
    status: processForm.value.status,
    feedback: processForm.value.feedback
  })
  ElMessage.success('Status Updated')
  showProcessDialog.value = false
  loadData()
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