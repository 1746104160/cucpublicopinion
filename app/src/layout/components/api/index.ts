/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-12 22:02:38
 * @FilePath: /app/src/layout/components/api/index.ts
 */

import request from '@/utils/request'
const logoutApi = {
  userLogout: 'auth/user/logout'
}
class Service {
  /**
   * @description GET 用户注销接口
  */
  static Logout () {
    return request({
      url: logoutApi.userLogout,
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
