import request from './request'

// ================= 费用项类型接口 =================

// 获取所有费用类型
export function getFeeTypes() {
  return request({
    url: '/api/fees/types/',
    method: 'get'
  })
}

// 创建费用类型
// data: { name, unit_price, unit }
export function createFeeType(data) {
  return request({
    url: '/api/fees/types/',
    method: 'post',
    data
  })
}

// 修改费用类型
export function updateFeeType(id, data) {
  return request({
    url: `/api/fees/types/${id}`,
    method: 'put',
    data
  })
}

// 删除费用类型
export function deleteFeeType(id) {
  return request({
    url: `/api/fees/types/${id}`,
    method: 'delete'
  })
}

// ================= 账单接口 =================

// 获取账单列表
// params: { owner_id, status, bill_month }
export function getFeeBills(params) {
  return request({
    url: '/api/fees/bills/',
    method: 'get',
    params
  })
}

// 生成账单 (为所有业主生成某个月份的某类费用)
// data: { fee_type_id, bill_month }
export function generateBills(data) {
  return request({
    url: '/api/fees/bills/generate/',
    method: 'post',
    data
  })
}

// 支付账单
// id: bill_id, data: { pay_time } (可选)
export function payBill(id, data) {
  return request({
    url: `/api/fees/bills/${id}/pay`,
    method: 'put',
    data
  })
}