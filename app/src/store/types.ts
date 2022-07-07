/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:34:28
 * @FilePath: /app/src/store/types.ts
 */
import sidebarStateTypes from './modules/sidebar/types'
import userStateTypes from './modules/user/types'
import tabStateTypes from './modules/tabs/types'

export default interface RootStateTypes {
  count: Number
}

export interface AllStateTypes extends RootStateTypes {
  sidebarModule: sidebarStateTypes
  userModule: userStateTypes
  tabModule: tabStateTypes
}
