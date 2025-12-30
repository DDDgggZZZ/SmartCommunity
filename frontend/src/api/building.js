import request from './request'

export function getBuildingList() {
  return request({ url: '/api/buildings/', method: 'get' })
}

export function createBuilding(data) {
  return request({ url: '/api/buildings/', method: 'post', data })
}

export function updateBuilding(id, data) {
  return request({ url: `/api/buildings/${id}`, method: 'put', data })
}

export function deleteBuilding(id) {
  return request({ url: `/api/buildings/${id}`, method: 'delete' })
}