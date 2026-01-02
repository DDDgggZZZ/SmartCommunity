import request from './request'

// ================= 费用项类型接口 =================

export function getFeeTypes() {
  return request({
    url: '/api/fees/types/',
    method: 'get'
  })
}

export function createFeeType(data) {
  return request({
    url: '/api/fees/types/',
    method: 'post',
    data
  })
}

export function updateFeeType(id, data) {
  return request({
    url: `/api/fees/types/${id}`,
    method: 'put',
    data
  })
}

export function deleteFeeType(id) {
  return request({
    url: `/api/fees/types/${id}`,
    method: 'delete'
  })
}

// ================= 账单接口 =================

export function getFeeBills(params) {
  return request({
    url: '/api/fees/bills/',
    method: 'get',
    params
  })
}

// [新增] 创建单条账单
export function createBill(data) {
  return request({
    url: '/api/fees/bills/',
    method: 'post',
    data
  })
}

export function generateBills(data) {
  return request({
    url: '/api/fees/bills/generate/',
    method: 'post',
    data
  })
}

export function payBill(id, data) {
  return request({
    url: `/api/fees/bills/${id}/pay`,
    method: 'put',
    data
  })
}