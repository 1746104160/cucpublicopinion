/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:32:49
 * @FilePath: /app/src/router/index.ts
 */

import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { store } from '../store'
import layout from '../layout/index.vue'
import { ElMessage } from 'element-plus'
import { useStorage } from 'vue3-storage'
const storage = useStorage()
// 静态路由
export const constantRoutes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: layout,
    redirect: '/home',
    meta: {
      title: '首页',
      icon: 'ic ic-homepage-fill'
    },
    children: [
      {
        path: '/home',
        name: 'home',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home/home.vue'),
        meta: {
          title: '首页',
          icon: 'ic ic-homepage-fill'
        }
      }
    ]
  },
  {
    path: '/login',
    name: '登录',
    component: () => import(/* webpackChunkName: "login" */ '@/views/Login/index.vue'),
    meta: {
      title: '登录',
      hidden: true,
      hiddenTab: true
    }
  },
  {
    path: '/noFound',
    name: 'NoFound',
    component: () => import(/* webpackChunkName: "noFound" */ '@/views/noFound.vue'),
    meta: {
      title: '404',
      hidden: true,
      hiddenTab: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import(/* webpackChunkName: "noFound" */ '@/views/noFound.vue'),
    meta: {
      title: '未找到',
      hidden: true,
      hiddenTab: true
    }
  }
]

// 异步路由
export const asyncRoutes: Array<RouteRecordRaw> = [
  {
    path: '/personal',
    component: layout,
    redirect: '/personal/personalCenter',
    meta: {
      title: '个人空间',
      icon: 'ic ic-people-fill'
    },
    children: [
      {
        path: '/personal/personalCenter',
        name: 'personalCenter',
        component: () => import(/* webpackChunkName: "personalCenter" */ '@/views/Personal/personalCenter.vue'),
        meta: {
          title: '个人中心',
          icon: 'ic ic-people-fill'
        }
      },
      {
        path: '/personal/personalSetting',
        name: 'personalSetting',
        component: () => import(/* webpackChunkName: "personalSetting" */ '@/views/Personal/personalSetting.vue'),
        meta: {
          title: '个人设置',
          icon: 'ic ic-setup-fill'
        }
      }
    ]
  },
  {
    path: '/dashboard',
    component: layout,
    redirect: '/dashboard/usersedit',
    meta: {
      title: '系统管理',
      icon: 'ic ic-group-fill'
    },
    children: [
      {
        path: '/dashboard/usersmanage',
        name: 'usersManage',
        component: () => import(/* webpackChunkName: "usersManage" */ '@/views/Dashboard/usersManage.vue'),
        meta: {
          title: '用户管理',
          icon: 'ic ic-group-fill'
        }
      },
      {
        path: '/dashboard/roleManage',
        name: 'rolesManage',
        component: () => import(/* webpackChunkName: "rolesManage" */ '@/views/Dashboard/rolesManage.vue'),
        meta: {
          title: '角色管理',
          icon: 'ic ic-group-fill'
        }
      }
    ]
  }
]
const router = createRouter({
  history: createWebHashHistory(), // hash模式：createWebHashHistory，history模式：createWebHistory
  scrollBehavior: () => ({
    top: 0
  }),
  routes: constantRoutes
})
router.beforeEach((to, from, next) => {
  const tabsOption = store.getters['tabModule/getTabsOption']
  const flag = tabsOption.findIndex((tab: { route: string }) => tab.route === to.path) > -1
  if (!flag && !to.meta.hiddenTab) {
    store.commit('tabModule/ADD_TAB', { route: to.path, title: to.meta.title, name: to.name })
  }
  store.commit('tabModule/SET_TAB', to.path)
  if (storage.getStorageSync('accessToken') && !storage.isExpire('accessToken')) {
    next()
  } else if (to.path === '/login') {
    next()
  } else {
    ElMessage.warning('unauthed into login')
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }
})

export default router
