/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:35:15
 * @FilePath: /app/src/utils/request.ts
 */

import Axios, { Method, ResponseType, AxiosResponse, AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import Cookies from 'js-cookie'
import { useStorage } from 'vue3-storage'
const storage = useStorage()
interface IAxiosData {
  url: string
  method: Method
  headers?: any
  json: boolean
  contentType?: string
  data?: any
  params?: any
  timeout?: number
  responseType?: ResponseType
}
const axios = Axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL,
  timeout: 2000
})
// 允许携带cookie
axios.defaults.withCredentials = true
// 请求头信息
axios.defaults.headers['X-Requested-With'] = 'XMLHttpRequest'
// 默认使用 application/json 形式
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8'

// 请求拦截器
axios.interceptors.request.use(
  (config:AxiosRequestConfig) => {
    if (storage.getStorageSync('accessToken') && !storage.isExpire('accessToken')) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${storage.getStorageSync('accessToken')}`
      }
    }
    if (Cookies.get('csrf_token') as string) {
      config.headers = {
        ...config.headers,
        'X-CSRFToken': Cookies.get('csrf_token') as string
      }
    }
    return config
  },
  (err) => Promise.reject(err)
)

// 响应拦截器
axios.interceptors.response.use(
  (res:AxiosResponse) => res,
  (err) => {
    if (err.response && err.response.data) {
      const code = err.response.status
      const msg = err.response.data.message
      ElMessage.error(`Code: ${code}, Message: ${msg}`)
    } else {
      ElMessage.error(`${err}`)
    }
    return Promise.reject(err)
  }
)

/** *
 * axios({url,method,content,params,datas})
 *
 * @param {string}  url，(必填)
 * @param {string}  method,默认post
 * @param {boolean} json, content-type类型，(必填)
 * @param {object}  params
 * @param {object}  datas  //token在datas中
 *
 */
export default function request (arr: IAxiosData) {
  return new Promise<any>((resolve, reject) => {
    // arr = requestValidate(arr)
    axios({
      timeout: arr.timeout === undefined ? 10000 : arr.timeout, // 请求超时时间
      url: arr.url,
      method: arr.method || 'POST',
      headers: {

        // 'Authorization': arr.token || '',
        // eslint-disable-next-line no-nested-ternary
        'content-type': arr.contentType
          ? arr.contentType
          : arr.json
            ? 'application/json; charset=UTF-8'
            : 'application/multipart/form-data; charset=UTF-8'
      },
      params: arr.params || '',
      data: arr.data || '',
      responseType: arr.responseType || 'json'
    })
      .then((response: AxiosResponse<any>) => {
        /**
         * response格式
         *
         * {
          data:{},
          status:200,
          statusText:'OK',//从服务器返回的http状态文本
          headers: {},//响应头信息
          config: {} //`config`是在请求的时候的一些配置信息
        }
         */
        const responseStatus = `${response.status}`
        // 状态码2开头的处理逻辑
        if (responseStatus.charAt(0) === '2') {
          if (
            response.data.code !== 0
          ) {
            ElMessage({
              type: 'error',
              message: response.data.message
            })
            reject(response.data)
            return
          }

          resolve(response.data)
        } else {
          ElMessage({
            type: 'error',
            message: response.data.message
          })
          reject(response.data)
        }
      })
      .catch((err) => {
        ElMessage({
          type: 'error',
          message: err.message
        })
        reject(err)
      })
  })
}
