import request from './request'

// 获取报修列表
// params: { owner_id, status }
export function getRepairList(params) {
  return request({
    url: '/api/repairs/',
    method: 'get',
    params
  })
}

// 提交报修
// data: { owner_id, content }
export function submitRepair(data) {
  return request({
    url: '/api/repairs/',
    method: 'post',
    data
  })
}

// 更新报修状态 (派单/完成)
// id: repair_id, data: { status, feedback }
export function updateRepairStatus(id, data) {
  return request({
    url: `/api/repairs/${id}/status`,
    method: 'put',
    data
  })
}