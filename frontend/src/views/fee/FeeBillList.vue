<template>
  <div class="page-container">
    <div class="geek-card">
      <div class="card-header">
        <h3 class="title">> {{ role === 'admin' ? 'Bill Management' : 'My Bills' }}</h3>
        <div v-if="role === 'admin'">
          <el-button type="primary" @click="openAddDialog">Add Bill</el-button>
          <el-button type="success" @click="showGenDialog = true">Generate Bills</el-button>
        </div>
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

    <el-dialog v-model="showGenDialog" title="Generate Monthly Bills (Batch)" width="400px">
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

    <el-dialog v-model="showAddDialog" title="Add New Bill (Single)" width="500px">
      <el-form :model="addForm" label-width="100px">
        <el-form-item label="Owner ID">
          <el-input v-model="addForm.owner_id" placeholder="Enter Owner ID (e.g., 1)" />
        </el-form-item>
        <el-form-item label="Fee Type">
          <el-select v-model="addForm.fee_type_id" placeholder="Select Fee Type" style="width: 100%">
            <el-option v-for="item in feeTypes" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Month">
          <el-date-picker 
            v-model="addForm.bill_month" 
            type="month" 
            value-format="YYYY-MM" 
            placeholder="Pick a month" 
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="Amount">
          <el-input-number v-model="addForm.amount" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="Status">
           <el-radio-group v-model="addForm.status">
             <el-radio label="未缴">Unpaid</el-radio>
             <el-radio label="已缴">Paid</el-radio>
           </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">Cancel</el-button>
        <el-button type="primary" @click="handleAdd">Submit</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFeeBills, generateBills, createBill, payBill, getFeeTypes } from '../../api/fee'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const feeTypes = ref([])
const showGenDialog = ref(false)
const showAddDialog = ref(false)
const role = ref('staff')

const query = ref({ owner_id: '', status: '', bill_month: '' })
const genForm = ref({ fee_type_id: null, bill_month: '' })
// 初始表单数据
const addForm = ref({
  owner_id: '',
  fee_type_id: null,
  bill_month: '',
  amount: 0,
  status: '未缴'
})

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

// 打开新增弹窗
const openAddDialog = () => {
  addForm.value = {
    owner_id: '',
    fee_type_id: null,
    bill_month: '',
    amount: 0,
    status: '未缴'
  }
  showAddDialog.value = true
  // 确保类型数据已加载
  if(feeTypes.value.length === 0) {
    loadTypes()
  }
}

// 提交新增
const handleAdd = async () => {
  if (!addForm.value.owner_id || !addForm.value.fee_type_id || !addForm.value.bill_month) {
    ElMessage.error('Please fill in Owner, Fee Type, and Month')
    return
  }
  try {
    await createBill(addForm.value)
    ElMessage.success('Bill Added Successfully')
    showAddDialog.value = false
    loadData()
  } catch (e) {
    console.error(e)
  }
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
  // 预加载费用类型
  loadTypes()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.title { margin: 0; color: var(--geek-text); }
</style>