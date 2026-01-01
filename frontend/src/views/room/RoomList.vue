<template>
  <div class="geek-container">
    <div class="toolbar geek-card">
      <el-button type="primary" :icon="Plus" @click="handleAdd">New Room</el-button>
       <el-input v-model="searchUnitId" placeholder="Filter by Unit ID..." style="width: 200px; margin-left: 10px" />
       <el-button type="primary" link @click="fetchData">Search</el-button>
    </div>

    <div class="table-container geek-card">
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="unit_id" label="Unit ID" width="100" />
        <el-table-column prop="room_no" label="Room No" />
        <el-table-column prop="area" label="Area (㎡)" />
        <el-table-column prop="layout" label="Layout" />
        <el-table-column prop="status" label="Status">
          <template #default="{ row }">
            <el-tag :type="row.status === '已售' ? 'danger' : 'success'" effect="dark">{{ row.status }}</el-tag>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'EDIT ROOM' : 'NEW ROOM'" width="35%">
      <el-form :model="form" label-width="80px">
        <el-form-item label="Unit ID">
          <el-input-number v-model="form.unit_id" :min="1" />
        </el-form-item>
        <el-form-item label="Room No">
          <el-input v-model="form.room_no" placeholder="e.g. 301" />
        </el-form-item>
        <el-form-item label="Area">
          <el-input-number v-model="form.area" :precision="2" :step="0.1" />
        </el-form-item>
        <el-form-item label="Layout">
          <el-input v-model="form.layout" placeholder="e.g. 3室1厅" />
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="form.status">
            <el-option label="已售" value="已售" />
            <el-option label="未售" value="未售" />
          </el-select>
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
import { getRoomList, createRoom, updateRoom, deleteRoom } from '@/api/room'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const searchUnitId = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({})

const fetchData = async () => {
  loading.value = true
  try {
     const params = searchUnitId.value ? { unit_id: searchUnitId.value } : {}
    tableData.value = await getRoomList(params) || []
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = { unit_id: 1, room_no: '', area: 0, layout: '', status: '未售' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`Delete Room [${row.room_no}]?`, 'Warning', { type: 'warning' })
    .then(async () => {
      await deleteRoom(row.id)
      ElMessage.success('Deleted')
      fetchData()
    })
}

const submitForm = async () => {
  if (isEdit.value) await updateRoom(form.value.id, form.value)
  else await createRoom(form.value)
  dialogVisible.value = false
  fetchData()
}

onMounted(fetchData)
</script>