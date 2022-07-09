/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 14:20:40
 * @FilePath: /app/src/views/Login/api/index.ts
 */

import axios from 'axios'
import request from '@/utils/request'
const loginApi = {
  userLogin: 'auth/user/login',
  userSSORegister: 'auth/user/register/cucaccount',
  imageCaptcha: 'auth/user/captcha',
  userRegister: 'auth/user/register/systemaccount',
  sendCaptcha: 'auth/user/email',
  resetPassword: 'auth/user/resetpw'
}
class Service {
  /**
   * @description POST 用户登录接口
  */
  static postLogin (data: any) {
    return request({
      url: loginApi.userLogin,
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
   * @description POST SSO单点登录账号注册接口
  */
  static postSSORegister (data: any) {
    return request({
      url: loginApi.userSSORegister,
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
   * @descript POST  系统用户注册接口
  */
  static postRegister (data: any) {
    return request({
      url: loginApi.userRegister,
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
   * @description   POST 发送邮件验证码
  */
  static postCaptcha (data: any) {
    return request({
      url: loginApi.sendCaptcha,
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
      url: import.meta.env.VITE_APP_API_URL + loginApi.imageCaptcha + '/' + data,
      method: 'GET'
    }).then((res) => {
      if (res.data.code === 0) {
        return Promise.resolve(res)
      }
      return Promise.reject(res)
    })
  }

  /**
   * @description POST 修改密码
  */
  static postResetPwd (data: any) {
    return request({
      url: loginApi.resetPassword,
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
