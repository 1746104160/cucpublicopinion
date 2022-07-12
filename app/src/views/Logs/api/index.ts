/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-12 13:51:39
 * @FilePath: /app/src/views/Logs/api/index.ts
 */

import request from '@/utils/request'

const logApi = {
  getallLoginfo: 'admin/log/loginfo'
}
class Service {
  /**
   * @description GET 获取日志信息
   */
  static getAllLogInfo (page: number, size: number, ipaddr: string, date: string) {
    return request({
      url: ipaddr !== '' ? `${logApi.getallLoginfo}?page=${page}&size=${size}&ip_addr=${ipaddr}&date=${date}` : `${logApi.getallLoginfo}?page=${page}&size=${size}&date=${date}`,
      method: 'GET',
      json: true
    }).then((res) => {
      if (res.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }
}
export default Service
