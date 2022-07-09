/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 00:14:34
 * @FilePath: /app/src/store/modules/user/index.ts
 */

import { Module } from 'vuex'
import { RouteRecordRaw } from 'vue-router'
import router, { constantRoutes, asyncRoutes } from '@/router'
import userStateTypes from './types'
import RootStateTypes from '@/store/types'
import Service from './api'
import setItem from '@/utils/session'
// create a new Store Modules.
const userModule: Module<userStateTypes, RootStateTypes> = {
  namespaced: true,
  state: {
    authedRoutes: constantRoutes // 权限路由
  },
  mutations: {
    /* 设置认证路由。 */
    setAuthedRoutes: (state: userStateTypes, routes) => {
      state.authedRoutes = constantRoutes.concat(routes)
    },
    /* 在会话存储中设置用户信息的突变。 */
    setUserInfo: (state: userStateTypes, userinfo) => {
      setItem('userinfo', JSON.stringify(userinfo))
    }
  },
  actions: {
    /* 用于获取用户信息和用户可以访问的路由的函数。 */
    getUserInfo ({ commit }) {
      // 后端根据JWT，查询授权菜单
      Service.getuserinfo().then((res) => {
        const { Routes, userinfo } = res.data
        commit('setUserInfo', userinfo)
        // 过滤只显示授权菜单
        sessionStorage.setItem('Routes', JSON.stringify(Routes))
        const authedRoutes: RouteRecordRaw[] = []
        for (const path of Routes) {
          for (const item of asyncRoutes) {
            if (item.path === path) {
              authedRoutes.push(item)
            }
          }
        }
        // 动态添加路由
        router.isReady().then(() => {
          authedRoutes.forEach((route: RouteRecordRaw) => {
            const routeName: any = route.name
            if (!router.hasRoute(routeName)) {
              router.addRoute(route)
            }
          })
          router.options.routes = constantRoutes.concat(authedRoutes)
          commit('setAuthedRoutes', authedRoutes)
        })
      })
    },
    /**
     * 它从会话存储中获取路由并将它们添加到路由器。
     * @param  - `commit`：存储的提交方法。
     */
    getRoutes ({ commit }) {
      const Routes = JSON.parse(sessionStorage.getItem('Routes') as string)
      const authedRoutes: RouteRecordRaw[] = []
      for (const path of Routes) {
        for (const item of asyncRoutes) {
          if (item.path === path) {
            authedRoutes.push(item)
          }
        }
      }
      authedRoutes.forEach((route: RouteRecordRaw) => {
        const routeName: any = route.name
        if (!router.hasRoute(routeName)) {
          router.addRoute(route)
        }
      })
      commit('setAuthedRoutes', authedRoutes)
    }
  }
}
export default userModule
