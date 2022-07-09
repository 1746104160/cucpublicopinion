/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 14:21:19
 * @FilePath: /app/src/utils/screen.ts
 */

import { ElMessage } from 'element-plus'

function toFullScreen () {
  const elem = document.body
  if (elem?.requestFullscreen) {
    elem.requestFullscreen()
  } else {
    ElMessage.warning('浏览器不支持全屏！')
  }
}

function exitFullScreen () {
  const elem = window.parent.document
  if (elem?.exitFullscreen) {
    elem.exitFullscreen()
  } else {
    ElMessage.warning('浏览器不支持全屏！')
  }
}

export {
  toFullScreen,
  exitFullScreen
}
