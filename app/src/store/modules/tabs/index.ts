/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:33:40
 * @FilePath: /app/src/store/modules/tabs/index.ts
 */

import { Module } from 'vuex'
import tabStateTypes from './types'
import RootStateTypes from '@/store/types'
// create a new Store Modules.
const tabModule: Module<tabStateTypes, RootStateTypes> = {
  namespaced: true,
  state: {
    tabsOption: [
      {
        route: '/home',
        title: '首页',
        name: 'home'
      }
    ],
    currentIndex: '/home',
    breadcrumbList: []
  },
  mutations: {
    ADD_TAB: (state: tabStateTypes, data: { route: string; name: string; title: String }) => {
      state.tabsOption.push(data)
      state.currentIndex = data.route
    },
    DELETE_TAB: (state: tabStateTypes, route: string) => {
      const index = state.tabsOption.findIndex((tab) => tab.route === route)
      state.tabsOption.splice(index, 1)
      if (state.currentIndex === route) {
        state.currentIndex = state.tabsOption[state.tabsOption.length - 1].route
      }
    },
    SET_TAB: (state: tabStateTypes, index: string) => {
      state.currentIndex = index
    },
    CLEAR_TAB: (state: tabStateTypes) => {
      // 初始化tab
      state.tabsOption = [
        {
          route: '/home',
          title: '首页',
          name: 'home'
        }
      ]
    }
  },
  actions: {},
  getters: {
    getCurrentIndex (state: tabStateTypes) {
      return state.currentIndex
    },
    getTabsOption (state: tabStateTypes) {
      return state.tabsOption
    }
  }
}
export default tabModule
