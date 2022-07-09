/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 14:19:58
 * @FilePath: /app/src/views/Personal/api/index.ts
 */

import axios from 'axios'
import request from '@/utils/request'

const personalApi = {
  updateInfo: 'personal/user/update',
  uploadAvatar: 'personal/user/upload',
  imageCaptcha: 'auth/user/captcha',
  sendCaptcha: 'auth/user/email',
  resetPassword: 'personal/user/resetpw',
  resetEmail: 'personal/user/resetemail',
  resetSSO: 'personal/user/resetsso'
}

class Service {
  /**
   * @description POST 设置基本信息
   */
  static postUpdateUserInfo (data: any) {
    return request({
      url: personalApi.updateInfo,
      method: 'post',
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
   * @description POST 设置基本信息
   */
  static postUserAvatar (data: any) {
    return request({
      url: personalApi.uploadAvatar,
      method: 'post',
      json: false,
      data
    }).then((res) => {
      if (res.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }

  static postCaptcha (data: any) {
    return request({
      url: personalApi.sendCaptcha,
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
   * @description   GET 获取图片验证码
  */
  static getCaptcha (data: number) {
    return axios({
      url: import.meta.env.VITE_APP_API_URL + personalApi.imageCaptcha + '/' + data,
      method: 'GET'
    }).then((res) => {
      if (res.data.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }

  /**
   * @description POST 修改密码 /personal/user/resetpwd
  */
  static postResetPwd (data: any) {
    return request({
      url: personalApi.resetPassword,
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
   * @description POST 修改邮箱 /personal/user/resetemail
  */
  static postResetEmail (data: any) {
    return request({
      url: personalApi.resetEmail,
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
   * @description POST 绑定/改绑中传SSO账号 /personal/user/resetsso
  */
  static postResetSSO (data: any) {
    return request({
      url: personalApi.resetSSO,
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
