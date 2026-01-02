import request from './request'

// 获取所有公告
export function getNoticeList() {
  return request({
    url: '/api/notices/',
    method: 'get'
  })
}

// 发布新公告
// data: { title, content, publish_time }
export function createNotice(data) {
  return request({
    url: '/api/notices/',
    method: 'post',
    data
  })
}

// 修改公告
// id: notice_id, data: { title, content, publish_time }
export function updateNotice(id, data) {
  return request({
    url: `/api/notices/${id}`,
    method: 'put',
    data
  })
}

// 删除公告
export function deleteNotice(id) {
  return request({
    url: `/api/notices/${id}`,
    method: 'delete'
  })
}