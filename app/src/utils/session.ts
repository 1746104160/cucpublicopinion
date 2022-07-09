/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 00:17:50
 * @FilePath: /app/src/utils/session.ts
 */

/**
 * 它创建一个新的 StorageEvent，初始化它，然后调度它
 * @param {string} key - 设置值的键。
 * @param {string} newVal - 您要存储的新值
 * @returns 函数调用 storage.setItem 的结果。
 */
export default function setItem (key: string, newVal: string) {
  if (key === 'userinfo') {
    const newStorageEvent = document.createEvent('StorageEvent')
    const storage = {
      setItem: function (k: string, val: string) {
        sessionStorage.setItem(k, val)
        newStorageEvent.initStorageEvent('setItem', false, false, k, null, val)
        window.dispatchEvent(newStorageEvent)
      }
    }
    return storage.setItem(key, newVal)
  }
}
