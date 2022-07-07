/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:32:57
 * @FilePath: /app/src/store/index.ts
 */

import { InjectionKey } from '@vue/runtime-core'
import { createStore, Store, useStore as baseUseStore } from 'vuex'

import sidebarModule from './modules/sidebar/index'
import userModule from './modules/user/index'
import tabModule from './modules/tabs/index'
import RootStateTypes, { AllStateTypes } from './types'

const defaultState = {
  count: 0
}
// 新建store 实例
export const store = createStore({
  state () {
    return defaultState
  },
  mutations: {
    increment (state: typeof defaultState) {
      // eslint-disable-next-line no-plusplus
      state.count++
    }
  },
  actions: {
    increment (context) {
      context.commit('increment')
    }
  },
  getters: {
    count (state: typeof defaultState) {
      return state.count
    }
  },
  modules: {
    sidebarModule,
    userModule,
    tabModule
  }
})

export const key: InjectionKey<Store<RootStateTypes>> = Symbol('vue3-store')

export function useStore<T = AllStateTypes> () {
  return baseUseStore<T>(key)
}
