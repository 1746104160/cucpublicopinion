/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:33:24
 * @FilePath: /app/src/store/modules/sidebar/index.ts
 */

import { Module } from 'vuex'
import Cookies from 'js-cookie'
import sidebarStateTypes from './types'
import RootStateTypes from '@/store/types'
// create a new Store Modules.
const sidebarModule: Module<sidebarStateTypes, RootStateTypes> = {
  namespaced: true,
  state: {
    opened: Cookies.get('sidebarStatus') ? !!Number.parseInt(Cookies.get('sidebarStatus') as string) : true
  },
  mutations: {
    toggle_sidebar: (state: sidebarStateTypes) => {
      state.opened = !state.opened
      Cookies.set('sidebarStatus', state.opened ? '1' : '0')
    },
    close_sidebar: (state: sidebarStateTypes) => {
      Cookies.set('sidebarStatus', '0')
      state.opened = false
    }
  },
  actions: {
    toggleSideBar ({ commit }) {
      commit('toggle_sidebar')
    },
    closeSideBar ({ commit }) {
      commit('close_sidebar')
    }
  },
  getters: {
    getSidebarState (state: sidebarStateTypes) {
      return state.opened
    }
  }
}
export default sidebarModule
