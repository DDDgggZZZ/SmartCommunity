import request from './request'

export function getRoomList(params) {
  return request({ url: '/api/rooms/', method: 'get', params })
}

export function createRoom(data) {
  return request({ url: '/api/rooms/', method: 'post', data })
}

export function updateRoom(id, data) {
  return request({ url: `/api/rooms/${id}`, method: 'put', data })
}

export function deleteRoom(id) {
  return request({ url: `/api/rooms/${id}`, method: 'delete' })
}