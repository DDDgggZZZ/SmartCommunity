<template>
  <div class="geek-container">
    <div class="toolbar geek-card">
      <el-button type="primary" :icon="Plus" @click="handleAdd">New Space</el-button>
      <el-select v-model="filterStatus" placeholder="Filter Status" clearable style="width: 150px; margin-left: 10px" @change="fetchData">
        <el-option label="闲置" value="闲置" />
        <el-option label="已租" value="已租" />
        <el-option label="已售" value="已售" />
      </el-select>
    </div>

    <div class="table-container geek-card">
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="space_no" label="Space No">
           <template #default="{ row }">
             <span style="font-weight: bold">{{ row.space_no }}</span>
           </template>
        </el-table-column>
        <el-table-column prop="status" label="Status">
          <template #default="{ row }">
            <el-tag effect="dark" :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="180">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">[EDIT]</el-button>
            <el-button link type="danger" @click="handleDelete(row)">[DEL]</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'EDIT SPACE' : 'NEW SPACE'" width="30%">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Space No">
          <el-input v-model="form.space_no" />
        </el-form-item>
        <el-form-item label="Status">
          <el-radio-group v-model="form.status">
            <el-radio-button value="闲置">闲置</el-radio-button>
            <el-radio-button value="已租">已租</el-radio-button>
            <el-radio-button value="已售">已售</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitForm">Execute</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { getParkingList, createParking, updateParking, deleteParking } from '@/api/parking'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const filterStatus = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({})

const getStatusType = (status) => {
  if (status === '闲置') return 'success'
  if (status === '已租') return 'warning'
  return 'info'
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = filterStatus.value ? { status: filterStatus.value } : {}
    tableData.value = await getParkingList(params) || []
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = { space_no: '', status: '闲置' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`Delete Space [${row.space_no}]?`, 'Warning', { type: 'warning' }).then(async () => {
    await deleteParking(row.id)
    ElMessage.success('Deleted')
    fetchData()
  })
}

const submitForm = async () => {
  if (isEdit.value) await updateParking(form.value.id, form.value)
  else await createParking(form.value)
  dialogVisible.value = false
  fetchData()
}

onMounted(fetchData)
</script>