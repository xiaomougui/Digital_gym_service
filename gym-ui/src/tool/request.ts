import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'

interface ResponseData<T = any> {
    code: number
    data: T
    message: string
    [key: string]: any
}

const request: AxiosInstance = axios.create({
    baseURL: '/api', // 全局统一添加 '/api' 前缀
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    timeout: 10000,  // 建议添加超时时间
    withCredentials: true // 跨域携带cookie
})

// 设置实际后端API基础地址
request.defaults.baseURL = "http://localhost:8080"

// 请求拦截器
request.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    // 可在请求发送前统一处理
    // 例如添加token到请求头
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers = config.headers || {}
    //   config.headers.Authorization = `Bearer ${token}`
    // }

    // 设置默认Content-Type
    if (!config.headers['Content-Type']) {
        config.headers['Content-Type'] = 'application/json'
    }

    return config
}, (error: AxiosError) => {
    return Promise.reject(error)
})

// 响应拦截器
request.interceptors.response.use(
    (response: AxiosResponse) => {
        // 处理二进制数据响应
        if (response.config.responseType === 'blob') {
            return response.data
        }

        let res = response.data

        // 处理字符串类型的响应数据
        if (typeof res === 'string') {
            try {
                res = res ? JSON.parse(res) : res
            } catch (e) {
                console.error('Response parsing error:', e)
            }
        }

        // 这里可以添加业务状态码检查
        // if (res.code !== 200) {
        //   return Promise.reject(new Error(res.message || 'Error'))
        // }

        return res
    },
    (error: AxiosError) => {
        console.error('Request error:', error)

        // 统一错误处理
        // if (error.response) {
        //   switch (error.response.status) {
        //     case 401:
        //       // 处理未授权
        //       break
        //     case 404:
        //       // 处理资源不存在
        //       break
        //     // 其他状态码处理...
        //   }
        // }

        return Promise.reject(error)
    }
)

export default request