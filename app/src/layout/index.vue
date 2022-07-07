<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:49
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:31:12
 * @FilePath: /app/src/layout/index.vue
-->
<template>
  <div :class="classObj" class="app-wrapper">
    <Sidebar class="sidebar-container" />
    <div class="main-container">
      <!--Navbar-->
      <div>
        <navbar />
      </div>
      <!--AppMain-->
      <AppMain />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useStore } from '@/store/index'

import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar/index.vue'
import AppMain from './components/AppMain.vue'

export default defineComponent({
  name: 'LayoutItem',
  components: {
    Navbar,
    Sidebar,
    AppMain
  },
  setup () {
    const store = useStore()

    const opened = computed(() => store.getters['sidebarModule/getSidebarState'])

    const classObj = computed(() => ({
      hideSidebar: !opened.value,
      openSidebar: opened.value
    }))

    return {
      classObj
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/styles/mixin.scss';
@import '@/styles/variables.scss';
.app-wrapper {
  @include clearfix;
  position: relative;
  height: 100%;
  width: 100%;
  overflow: scroll;
}
</style>
