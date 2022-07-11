<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:49
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 14:23:22
 * @FilePath: /app/src/App.vue
-->
<template>
   <el-config-provider>
    <div id="app">
      <router-view></router-view>
    </div>
   </el-config-provider>
</template>
<script lang="ts">

</script>
<style>
html,
body,
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  margin: 0;
  padding: 0;
}
.element-plus-logo {
  width: 50%;
}
</style>
