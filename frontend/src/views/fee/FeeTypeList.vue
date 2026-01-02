<template>
  <div class="page-container">
    <div class="geek-card">
      <div class="card-header">
        <h3 class="title">> Fee Types Configuration</h3>
        <el-button type="primary" @click="openDialog()">Add Fee Type</el-button>
      </div>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="unit_price" label="Unit Price">
          <template #default="{ row }">¥{{ row.unit_price }}</template>
        </el-table-column>
        <el-table-column prop="unit" label="Unit" />
        <el-table-column label="Operations" width="120">
          <template #default="scope">
            <el-button type="danger" link @click="handleDelete(scope.row.id)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" title="Add Fee Type" width="400px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Name">
          <el-input v-model="form.name" placeholder="e.g. Property Fee" />
        </el-form-item>
        <el-form-item label="Price">
          <el-input-number v-model="form.unit_price" :precision="2" :step="0.1" />
        </el-form-item>
        <el-form-item label="Unit">
          <el-input v-model="form.unit" placeholder="e.g. /m²" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Create</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFeeTypes, createFeeType, deleteFeeType } from '../../api/fee'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const form = ref({ name: '', unit_price: 0, unit: '' })

const loadData = async () => {
  loading.value = true
  tableData.value = await getFeeTypes()
  loading.value = false
}

const openDialog = () => {
  form.value = { name: '', unit_price: 0, unit: '' }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.name || !form.value.unit) {
    ElMessage.error('Please fill all fields')
    return
  }
  await createFeeType(form.value)
  ElMessage.success('Created')
  dialogVisible.value = false
  loadData()
}

const handleDelete = (id) => {
  ElMessageBox.confirm('Delete this fee type?', 'Warning').then(async () => {
    await deleteFeeType(id)
    ElMessage.success('Deleted')
    loadData()
  })
}

onMounted(loadData)
</script>
<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.title { margin: 0; color: var(--geek-text); }
</style>