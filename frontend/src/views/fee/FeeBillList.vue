<template>
  <div class="page-container">
    <div class="geek-card">
      <div class="card-header">
        <h3 class="title">> {{ role === 'admin' ? 'Bill Management' : 'My Bills' }}</h3>
        <el-button v-if="role === 'admin'" type="success" @click="showGenDialog = true">Generate Bills</el-button>
      </div>

      <div v-if="role === 'admin'" class="filter-bar" style="margin-bottom: 20px; display: flex; gap: 10px;">
        <el-input v-model="query.owner_id" placeholder="Owner ID" style="width: 150px;" clearable />
        <el-select v-model="query.status" placeholder="Status" clearable style="width: 150px;">
          <el-option label="Unpaid" value="未缴" />
          <el-option label="Paid" value="已缴" />
        </el-select>
        <el-input v-model="query.bill_month" placeholder="Month (YYYY-MM)" style="width: 180px;" clearable />
        <el-button type="primary" @click="loadData">Search</el-button>
      </div>

      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column v-if="role === 'admin'" prop="owner_id" label="Owner ID" width="100" />
        <el-table-column prop="fee_type_id" label="Fee Type ID" width="100" />
        <el-table-column prop="bill_month" label="Month" width="120" />
        <el-table-column prop="amount" label="Amount">
          <template #default="{ row }">¥{{ row.amount }}</template>
        </el-table-column>
        <el-table-column prop="status" label="Status">
          <template #default="{ row }">
            <el-tag :type="row.status === '已缴' ? 'success' : 'danger'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pay_time" label="Pay Time" width="180" />
        <el-table-column label="Action">
          <template #default="{ row }">
            <el-button 
              v-if="row.status === '未缴'" 
              type="primary" 
              size="small" 
              @click="handlePay(row)"
            >Pay Now</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="showGenDialog" title="Generate Monthly Bills" width="400px">
      <el-form :model="genForm" label-width="100px">
        <el-form-item label="Fee Type">
          <el-select v-model="genForm.fee_type_id" placeholder="Select Type">
            <el-option v-for="item in feeTypes" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Month">
          <el-date-picker 
            v-model="genForm.bill_month" 
            type="month" 
            value-format="YYYY-MM" 
            placeholder="Pick a month" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showGenDialog = false">Cancel</el-button>
        <el-button type="success" @click="handleGenerate">Generate</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFeeBills, generateBills, payBill, getFeeTypes } from '../../api/fee'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const feeTypes = ref([])
const showGenDialog = ref(false)
const role = ref('staff')

const query = ref({ owner_id: '', status: '', bill_month: '' })
const genForm = ref({ fee_type_id: null, bill_month: '' })

const loadData = async () => {
  loading.value = true
  const params = {}
  if(query.value.owner_id) params.owner_id = query.value.owner_id
  if(query.value.status) params.status = query.value.status
  if(query.value.bill_month) params.bill_month = query.value.bill_month
  
  try {
    tableData.value = await getFeeBills(params)
  } finally {
    loading.value = false
  }
}

const loadTypes = async () => {
  feeTypes.value = await getFeeTypes()
}

const handleGenerate = async () => {
  if (!genForm.value.fee_type_id || !genForm.value.bill_month) {
    ElMessage.error('Please select fee type and month')
    return
  }
  const loadingMsg = ElMessage.loading({ message: 'Generating...', duration: 0 })
  try {
    await generateBills(genForm.value)
    loadingMsg.close()
    ElMessage.success('Bills Generated Successfully')
    showGenDialog.value = false
    loadData()
  } catch (e) {
    loadingMsg.close()
  }
}

const handlePay = (row) => {
  ElMessageBox.confirm(`Confirm payment of ¥${row.amount} for Bill #${row.id}?`, 'Payment', {
    confirmButtonText: 'Pay',
    type: 'info'
  }).then(async () => {
    await payBill(row.id, {})
    ElMessage.success('Payment Successful')
    loadData()
  }).catch(() => {})
}

onMounted(() => {
  const userStr = sessionStorage.getItem('user_info')
  if (userStr) {
    role.value = JSON.parse(userStr).role || 'staff'
  }
  
  loadData()
  if (role.value === 'admin') {
    loadTypes()
  }
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.title { margin: 0; color: var(--geek-text); }
</style>