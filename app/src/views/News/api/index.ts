/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 00:48:35
 * @FilePath: /app/src/views/News/api/index.ts
 */

import request from '@/utils/request'

const newsApi = {
  getallnewsinfo: 'admin/news/newsinfo',
  updatenewsinfo: 'admin/news/update',
  createnews: 'admin/news/create',
  deletenews: 'admin/news/delete',
  bannews: 'admin/news/ban',
  getallRoutesinfo: 'admin/news/routes'
}
class Service {
  /**
   * @description GET 获取新闻信息
   */
  static getAllNewsInfo (page:number, size:number, order:string) {
    return request({
      url: `${newsApi.getallnewsinfo}?page=${page}&size=${size}&order=${order}`,
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
   * @description POST 修改新闻信息
   */
  static updateNewsInfo (data:any) {
    return request({
      url: newsApi.updatenewsinfo,
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
   * @description POST 导入新闻
   */
  static createNews (data:any) {
    return request({
      url: newsApi.createnews,
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
   * @description POST 删除新闻
   */
  static deleteNews (data:any) {
    return request({
      url: newsApi.deletenews,
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
