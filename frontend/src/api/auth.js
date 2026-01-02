import request from './request'

// 登录接口
// data: { username, password }
export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}