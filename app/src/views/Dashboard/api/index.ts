/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 01:03:41
 * @FilePath: /app/src/views/Dashboard/api/index.ts
 */

import request from '@/utils/request'

const roleApi = {
  getallUserinfo: 'admin/user/userinfo',
  updateUserinfo: 'admin/user/update',
  deleteUser: 'admin/user/delete',
  banUser: 'admin/user/ban',
  getallRoleinfo: 'admin/role/roleinfo',
  updateRoleinfo: 'admin/role/update',
  createRole: 'admin/role/create',
  deleteRole: 'admin/role/delete',
  banRole: 'admin/role/ban'
}

class Service {
  /**
   * @description GET 获取用户信息
   */
  static getAllUserInfo (page:number, size:number, order:string) {
    return request({
      url: roleApi.getallUserinfo + '/' + page + '/' + size + '/' + order,
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
   * @description POST 修改用户信息
   */
  static updateUserInfo (data:any) {
    return request({
      url: roleApi.updateUserinfo,
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
   * @description POST 删除用户
   */
  static deleteUser (data:any) {
    return request({
      url: roleApi.deleteUser,
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
   * @description POST 封禁用户
   */
  static banUser (data:any) {
    return request({
      url: roleApi.banUser,
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
   * @description GET 获取角色信息
   */
  static getAllRoleInfo (page:number, size:number, order:string) {
    return request({
      url: roleApi.getallRoleinfo + '/' + page + '/' + size + '/' + order,
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
   * @description POST 修改角色信息
   */
  static updateRoleInfo (data:any) {
    return request({
      url: roleApi.updateRoleinfo,
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
   * @description POST 创建用户
   */
  static createRole (data:any) {
    return request({
      url: roleApi.createRole,
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
   * @description POST 删除角色
   */
  static deleteRole (data:any) {
    return request({
      url: roleApi.deleteRole,
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
   * @description POST 封禁角色
   */
  static banRole (data:any) {
    return request({
      url: roleApi.banRole,
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
