import request from './request'

export function getParkingList(params) {
  return request({ url: '/api/parkings/spaces/', method: 'get', params })
}

export function createParking(data) {
  return request({ url: '/api/parkings/spaces/', method: 'post', data })
}

export function updateParking(id, data) {
  return request({ url: `/api/parkings/spaces/${id}`, method: 'put', data })
}

export function deleteParking(id) {
  return request({ url: `/api/parkings/spaces/${id}`, method: 'delete' })
}