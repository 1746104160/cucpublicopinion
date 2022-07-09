/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 00:16:48
 * @FilePath: /app/src/utils/screen.ts
 */

import { ElMessage } from 'element-plus'

/**
 * 它会尝试使页面全屏显示，如果不能，则会显示警告消息
 */
function toFullScreen () {
  const elem = document.body
  if (elem?.requestFullscreen) {
    elem.requestFullscreen()
  } else {
    ElMessage.warning('浏览器不支持全屏！')
  }
}

/**
 * 如果浏览器支持退出全屏，则退出全屏，否则显示警告信息
 */
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
