<template>
  <div class="geek-container">
    <div class="toolbar geek-card">
      <el-button type="primary" :icon="Plus" @click="handleAdd">New Unit</el-button>
      <el-input v-model="searchId" placeholder="Filter by Building ID..." style="width: 200px; margin-left: 10px" />
      <el-button type="primary" link @click="fetchData">Search</el-button>
    </div>

    <div class="table-container geek-card">
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="building_id" label="Building ID" width="120" />
        <el-table-column prop="unit_no" label="Unit No">
             <template #default="{ row }">
            <span style="color: var(--geek-primary)">{{ row.unit_no }}</span>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'EDIT UNIT' : 'NEW UNIT'" width="30%">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Building ID">
          <el-input-number v-model="form.building_id" :min="1" />
        </el-form-item>
        <el-form-item label="Unit No">
          <el-input v-model="form.unit_no" placeholder="e.g. 1单元" />
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
import { ref, onMounted, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { getUnitList, createUnit, updateUnit, deleteUnit } from '@/api/unit'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const searchId = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ id: null, building_id: 1, unit_no: '' })

const fetchData = async () => {
  loading.value = true
  try {
    const params = searchId.value ? { building_id: searchId.value } : {}
    tableData.value = await getUnitList(params) || []
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = { building_id: 1, unit_no: '' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`Delete Unit [${row.unit_no}]?`, 'Warning', { type: 'warning' })
    .then(async () => {
      await deleteUnit(row.id)
      ElMessage.success('Deleted')
      fetchData()
    })
}

const submitForm = async () => {
  if (isEdit.value) await updateUnit(form.value.id, form.value)
  else await createUnit(form.value)
  dialogVisible.value = false
  fetchData()
}

onMounted(fetchData)
</script>