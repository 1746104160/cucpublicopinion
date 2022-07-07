/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:33:46
 * @FilePath: /app/src/store/modules/tabs/types.ts
 */

export default interface tabStateTypes {
  tabsOption: [{ route: String; name: String; title: String }]
  currentIndex: String
  breadcrumbList: any[]
}
