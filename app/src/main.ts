/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:49
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 11:32:26
 * @FilePath: /app/src/main.ts
 */
import { createApp } from 'vue'
import locale from 'element-plus/lib/locale/lang/zh-cn'
import ElementPlus from 'element-plus'
import App from './App.vue'
import { key, store } from './store/index'
import Vue3Storage from 'vue3-storage'
import router from './router/index'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/index.css'
import '@/styles/index.scss'
import DataVVue3 from '@kjgl77/datav-vue3'
if (sessionStorage.getItem('Routes')) {
  store.dispatch('userModule/getRoutes')
}
// 链式注册插件
const app = createApp(App).use(store, key).use(Vue3Storage).use(router).use(ElementPlus, { locale }).use(DataVVue3)
// 现在所有的导航都是异步的，等路由ready以后再进行挂载组件；
router.isReady().then(() => app.mount('#app'))

// 在导航期间每次发生未捕获的错误时都会调用该处理程序
// eslint-disable-next-line no-console
router.onError((err) => {
  console.error(err)
})
