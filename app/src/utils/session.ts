/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:35:27
 * @FilePath: /app/src/utils/session.ts
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
