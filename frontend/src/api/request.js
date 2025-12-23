import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:5000', // 后端地址
  timeout: 5000 // 请求超时时间
})

// request 拦截器 (可以在这里统一加 Token)
service.interceptors.request.use(
  config => {
    // 例如: config.headers['Authorization'] = getToken()
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// response 拦截器 (统一处理错误)
service.interceptors.response.use(
  response => {
    const res = response.data
    // 如果后端返回 code 不是 200，说明出错了
    if (res.code !== 200) {
      ElMessage.error(res.msg || '系统错误')
      return Promise.reject(new Error(res.msg || 'Error'))
    } else {
      return res.data // ★直接把后端 data 字段剥离出来，页面里少写一层 .data
    }
  },
  error => {
    console.log('err' + error)
    ElMessage.error(error.message)
    return Promise.reject(error)
  }
)

export default service