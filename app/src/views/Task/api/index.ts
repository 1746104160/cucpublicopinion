/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 21:49:01
 * @FilePath: /app/src/views/Task/api/index.ts
 */

import axios from 'axios'
import { useStorage } from 'vue3-storage'
const storage = useStorage()
const gpuApi = {
  creatework: 'gpu/longtask',
  checkstate: 'gpu/status'
}
class Service {
  /**
   * @description GET 创建任务
   */
  static creatework (clas:number) {
    return axios({
      url: import.meta.env.VITE_APP_API_URL + `${gpuApi.creatework}?clas=${clas}`,
      method: 'GET',
      headers: {
        Authorization: `Bearer ${storage.getStorageSync('accessToken')}`
      }
    }).then((res) => {
      return Promise.resolve(res.headers.location)
    })
  }

  /**
   * @description GET 查询进度
   */
  static checkstate (ids:string) {
    return axios({
      url: import.meta.env.VITE_APP_API_URL + `${gpuApi.checkstate}/${ids}`,
      method: 'GET',
      headers: {
        Authorization: `Bearer ${storage.getStorageSync('accessToken')}`
      }
    }).then((res) => {
      return Promise.resolve(res.data)
    })
  }
}
export default Service
