<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:31:53
 * @FilePath: /app/src/layout/components/Sidebar/index.vue
-->

<template>
  <div class='has-logo'>
    <logo :collapse="isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu :router="true" :unique-opened="false" :default-active="activeMenu" class="el-menu-vertical" :collapse="isCollapse" background-color="#545c64" text-color="#fff">
        <sidebar-item v-for="route in routes" :key="route.path" :item="route" :base-path="route.path" />
      </el-menu>
    </el-scrollbar>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { isExternal } from '@/utils/validate'
import sidebarItem from '@/layout/components/Sidebar/sidebarItem.vue'
import logo from './Logo.vue'
import { useStore } from '@/store/index'

export default defineComponent({
  name: 'SidebarIndex',
  components: {
    logo,
    sidebarItem
  },
  setup () {
    const route = useRoute()

    const store = useStore()
    const isCollapse = computed(() => !store.getters['sidebarModule/getSidebarState'])
    const routes = computed(() => store.state.userModule.authedRoutes)
    const activeMenu = computed(() => store.getters['tabModule/getCurrentIndex'])

    onMounted(() => {
      const routePath = route.path
      store.dispatch('userModule/getUserInfo')
      store.commit('tabModule/SET_TAB', routePath)
    })

    // methods
    // eslint-disable-next-line consistent-return
    const resolvePath = (routePath: string) => {
      if (isExternal(routePath)) {
        return routePath
      }
    }
    return {
      activeMenu,
      resolvePath,
      routes,
      isCollapse
    }
  }
})
</script>
<style lang="stylus" scoped>
.el-menu-vertical:not(.el-menu--collapse)
  width 200px
  min-height 400px
  text-align left
</style>
