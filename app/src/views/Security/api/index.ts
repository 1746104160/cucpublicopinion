/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-12 10:34:48
 * @FilePath: /app/src/views/Security/api/index.ts
 */

import request from '@/utils/request'

const securityApi = {
  getallServiceinfo: 'admin/security/serviceinfo',
  banService: 'admin/security/ban',
  unbanService: 'admin/security/unban'
}
class Service {
  /**
   * @description GET 获取用户信息
   */
  static getAllServiceInfo (page: number, size: number, ipaddr: string) {
    return request({
      url: ipaddr !== '' ? `${securityApi.getallServiceinfo}?page=${page}&size=${size}&ip_addr=${ipaddr}` : `${securityApi.getallServiceinfo}?page=${page}&size=${size}`,
      method: 'GET',
      json: true
    }).then((res) => {
      if (res.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }

  /**
   * @description POST 封禁服务
   */
  static banService (data: any) {
    return request({
      url: securityApi.banService,
      method: 'POST',
      json: true,
      data
    }).then((res) => {
      if (res.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }

  /**
   * @description POST 解封服务
   */
  static unbanService (data: any) {
    return request({
      url: securityApi.unbanService,
      method: 'POST',
      json: true,
      data
    }).then((res) => {
      if (res.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }
}
export default Service
