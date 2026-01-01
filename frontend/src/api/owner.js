import request from './request'

export function getOwnerList(params) {
  return request({ url: '/api/owners/', method: 'get', params })
}

export function createOwner(data) {
  return request({ url: '/api/owners/', method: 'post', data })
}

export function updateOwner(id, data) {
  return request({ url: `/api/owners/${id}`, method: 'put', data })
}

export function deleteOwner(id) {
  return request({ url: `/api/owners/${id}`, method: 'delete' })
}