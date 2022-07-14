/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 11:34:00
 * @FilePath: /app/src/views/Home/api/index.ts
 */

import request from '@/utils/request'
const visualizeApi = {
  getCategory: 'visualize/news/category',
  getCluster: 'visualize/news/cluster',
  getHotword: 'visualize/news/hotword',
  getPostnum: 'visualize/news/postnum',
  getSentiment: 'visualize/news/sentiment'
}
class Service {
  /**
   * @description GET 获取新闻分类
  */
  static getCategory () {
    return request({
      url: visualizeApi.getCategory,
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
   * @description GET 获取新闻聚类
  */
  static getCluster () {
    return request({
      url: visualizeApi.getCluster,
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
   * @description GET 获取新闻分类
  */
  static getHotword () {
    return request({
      url: visualizeApi.getHotword,
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
   * @description GET 获取新闻统计信息
  */
  static getPostnum () {
    return request({
      url: visualizeApi.getPostnum,
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
   * @description GET 获取新闻情感信息
  */
  static getSentiment () {
    return request({
      url: visualizeApi.getSentiment,
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
   * @description GET 获取新闻情感信息
  */
  static getSentimentforarticleSource (articleSource:string[]) {
    return request({
      url: visualizeApi.getSentiment + '?articleSource=' + articleSource,
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
