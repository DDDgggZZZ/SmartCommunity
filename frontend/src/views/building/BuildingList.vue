<template>
  <div class="building-manager">
    <div class="toolbar geek-card">
      <el-button type="primary" @click="handleAdd" :icon="Plus">New Building</el-button>
      <el-input v-model="search" placeholder="Search building no..." style="width: 200px; margin-left: 10px" />
    </div>

    <div class="table-container geek-card">
      <el-table :data="filteredData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="building_no" label="NO." width="120">
          <template #default="{ row }">
            <span style="color: var(--geek-primary); font-weight: bold;">{{ row.building_no }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="total_floors" label="Floors" width="120" />
        <el-table-column prop="description" label="Description" />
        <el-table-column label="Operations" width="180">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleEdit(row)">[EDIT]</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">[DEL]</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'EDIT NODE' : 'NEW NODE'" width="30%" class="geek-dialog">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Building No">
          <el-input v-model="form.building_no" placeholder="e.g. 1栋" />
        </el-form-item>
        <el-form-item label="Total Floors">
          <el-input-number v-model="form.total_floors" :min="1" />
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitForm">Execute</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { getBuildingList, createBuilding, updateBuilding, deleteBuilding } from '@/api/building'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const search = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ id: null, building_no: '', total_floors: 1, description: '' })

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const res = await getBuildingList()
    tableData.value = res || []
  } finally {
    loading.value = false
  }
}

// 搜索过滤
const filteredData = computed(() => {
  return tableData.value.filter(item => 
    !search.value || item.building_no.includes(search.value)
  )
})

const handleAdd = () => {
  isEdit.value = false
  form.value = { building_no: '', total_floors: 1, description: '' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row } // 浅拷贝
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `Are you sure to delete Building [${row.building_no}]? This action cannot be undone.`,
    'Warning',
    { confirmButtonText: 'Confirm', cancelButtonText: 'Cancel', type: 'warning' }
  ).then(async () => {
    await deleteBuilding(row.id)
    ElMessage.success('Deleted successfully')
    fetchData()
  })
}

const submitForm = async () => {
  try {
    if (isEdit.value) {
      await updateBuilding(form.value.id, form.value)
      ElMessage.success('Updated successfully')
    } else {
      await createBuilding(form.value)
      ElMessage.success('Created successfully')
    }
    dialogVisible.value = false
    fetchData()
  } catch (e) {
    // Error handled by request interceptor
  }
}

onMounted(fetchData)
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}
.table-container {
  min-height: 400px;
}
</style>