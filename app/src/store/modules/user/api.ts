/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:33:57
 * @FilePath: /app/src/store/modules/user/api.ts
 */

import request from '@/utils/request'

const userApi = {
  queryUserInfo: 'auth/user/userinfo'
}

class Service {
  /**
   * @description GET 查询用户信息
   */
  static getuserinfo () {
    return request({
      url: userApi.queryUserInfo,
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
