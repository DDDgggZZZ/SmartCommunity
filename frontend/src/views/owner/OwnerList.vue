<template>
  <div class="geek-container">
    <div class="toolbar geek-card">
      <el-button type="primary" :icon="Plus" @click="handleAdd">New Owner</el-button>
      <div style="flex: 1"></div>
      <el-button :icon="Refresh" circle @click="fetchData" />
    </div>

    <div class="table-container geek-card">
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="Name" width="120">
          <template #default="{ row }">
            <span style="color: var(--geek-primary); font-weight: bold">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="Phone" width="150" />
        <el-table-column prop="id_card" label="ID Card" />
        <el-table-column prop="move_in_date" label="Move In">
          <template #default="{ row }">
            <el-tag v-if="row.move_in_date" type="info" effect="plain">{{ row.move_in_date }}</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="180" align="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">[EDIT]</el-button>
            <el-button link type="danger" @click="handleDelete(row)">[DEL]</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog 
      v-model="dialogVisible" 
      :title="isEdit ? 'EDIT OWNER' : 'NEW OWNER'" 
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form :model="form" label-width="100px" style="padding-right: 20px">
        <el-form-item label="Name">
          <el-input v-model="form.name" placeholder="Owner Name" />
        </el-form-item>
        <el-form-item label="Phone">
          <el-input v-model="form.phone" placeholder="Phone Number" />
        </el-form-item>
        <el-form-item label="ID Card">
          <el-input v-model="form.id_card" placeholder="ID Card No." />
        </el-form-item>
        <el-form-item label="Move In Date">
          <el-date-picker 
            v-model="form.move_in_date" 
            type="date" 
            value-format="YYYY-MM-DD" 
            placeholder="Select Date" 
            style="width: 100%" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">Execute</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { getOwnerList, createOwner, updateOwner, deleteOwner } from '@/api/owner'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const submitting = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getOwnerList()
    tableData.value = Array.isArray(res) ? res : (res.data || [])
  } catch (error) {
    console.error("Fetch error:", error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = { name: '', phone: '', id_card: '', move_in_date: '' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  // 浅拷贝对象
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `Are you sure to delete owner [${row.name}]?`, 
    'System Warning', 
    { 
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning' 
    }
  ).then(async () => {
    try {
      await deleteOwner(row.id)
      ElMessage.success('Operation Successful')
      fetchData()
    } catch (error) {
      console.error(error)
    }
  })
}

const submitForm = async () => {
  // 1. 简单校验
  if (!form.value.name || !form.value.phone || !form.value.id_card) {
    ElMessage.warning('Name, Phone, and ID Card are required.')
    return
  }

  // 2. ★★★ 核心修复：提交前强制清洗日期格式 ★★★
  // 防止后端传来的 GMT 格式字符串（如 'Wed, 04 Jan 2023...'）未被修改就直接传回去导致报错
  const payload = { ...form.value }
  if (payload.move_in_date && payload.move_in_date.includes('GMT')) {
    try {
      // 如果发现是 GMT 格式，强行转回 YYYY-MM-DD
      const dateObj = new Date(payload.move_in_date)
      const year = dateObj.getFullYear()
      const month = String(dateObj.getMonth() + 1).padStart(2, '0')
      const day = String(dateObj.getDate()).padStart(2, '0')
      payload.move_in_date = `${year}-${month}-${day}`
    } catch (e) {
      console.warn("Date parsing failed, sending original string")
    }
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      // 注意：这里传的是清洗后的 payload，而不是 form.value
      await updateOwner(payload.id, payload)
      ElMessage.success('Updated Successfully')
    } else {
      await createOwner(payload)
      ElMessage.success('Created Successfully')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error("Submit error:", error)
    ElMessage.error('Operation Failed: ' + (error.response?.data?.msg || 'Unknown error'))
  } finally {
    submitting.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
/* 保持和其他页面一致的极客风格 */
.geek-container {
  padding: 0;
}
.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  padding: 15px;
}
.table-container {
  padding: 20px;
  min-height: 400px;
}
</style>