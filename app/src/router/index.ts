/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 20:36:21
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
    redirect: '/dashboard/usersmanage',
    meta: {
      title: '系统管理',
      icon: 'ic ic-setup-fill'
    },
    children: [
      {
        path: '/dashboard/usersmanage',
        name: 'usersManage',
        component: () => import(/* webpackChunkName: "usersManage" */ '@/views/Dashboard/usersManage.vue'),
        meta: {
          title: '用户管理',
          icon: 'ic ic-people-fill'
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
  },
  {
    path: '/news',
    component: layout,
    redirect: '/news/newsmanage',
    meta: {
      title: '新闻管理',
      icon: 'ic ic-document-fill'
    },
    children: [
      {
        path: '/news/newsmanage',
        name: 'newsManage',
        component: () => import(/* webpackChunkName: "newsManage" */ '@/views/News/newsManage.vue'),
        meta: {
          title: '新闻管理',
          icon: 'ic ic-document-fill'
        }
      },
      {
        path: '/news/newscreate',
        name: 'newsCreate',
        component: () => import(/* webpackChunkName: "newsCreate" */ '@/views/News/newsCreate.vue'),
        meta: {
          title: '新闻导入',
          icon: 'ic ic-document-fill'
        }
      },
      {
        path: '/news/newsupdate',
        name: 'newsUpdate',
        component: () => import(/* webpackChunkName: "newsUpdate" */ '@/views/News/newsUpdate.vue'),
        meta: {
          hidden: true,
          title: '新闻修改'
        }
      }
    ]
  },
  {
    path: '/security',
    component: layout,
    redirect: '/security/servicemanage',
    meta: {
      title: '安全管理',
      icon: 'ic ic-manage-fill'
    },
    children: [
      {
        path: '/security/servicemanage',
        name: 'serviceManage',
        component: () => import(/* webpackChunkName: "serviceManage" */ '@/views/Security/serviceManage.vue'),
        meta: {
          title: '安全管理',
          icon: 'ic ic-manage-fill'
        }
      }
    ]
  },
  {
    path: '/log',
    component: layout,
    redirect: '/log/logmanage',
    meta: {
      title: '日志管理',
      icon: 'ic ic-task-fill'
    },
    children: [
      {
        path: '/log/logmanage',
        name: 'logManage',
        component: () => import(/* webpackChunkName: "logManage" */ '@/views/Logs/logManage.vue'),
        meta: {
          title: '日志管理',
          icon: 'ic ic-task-fill'
        }
      }
    ]
  },
  {
    path: '/version',
    component: layout,
    redirect: '/version/versioninfo',
    meta: {
      title: '版本信息',
      icon: 'ic ic-clock-fill'
    },
    children: [
      {
        path: '/version/versioninfo',
        name: 'versionInfo',
        component: () => import(/* webpackChunkName: "versionInfo" */ '@/views/Version/version.vue'),
        meta: {
          title: '版本信息',
          icon: 'ic ic-clock-fill'
        }
      }
    ]
  },
  {
    path: '/task',
    component: layout,
    redirect: '/task/taskmanage',
    meta: {
      title: '调度管理',
      icon: 'ic ic-activity-fill'
    },
    children: [
      {
        path: '/task/taskmanage',
        name: 'taskManage',
        component: () => import(/* webpackChunkName: "taskManage" */ '@/views/Task/task.vue'),
        meta: {
          title: '调度管理',
          icon: 'ic ic-activity-fill'
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
