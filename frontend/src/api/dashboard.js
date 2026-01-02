import request from './request'

// 获取仪表盘统计信息
export function getDashboardStats() {
  return request({
    url: '/api/dashboard/stats',
    method: 'get'
  })
}