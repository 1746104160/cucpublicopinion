<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:39:02
 * @FilePath: /app/src/views/Home/home.vue
-->

<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>欢迎来到业务管理系统</h1>
          </el-header>
          <el-divider />
          <el-main>
          </el-main>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'HomePage',
  setup () {
    return {
    }
  }
})
</script>
<style scoped lang="scss">
.page-container {
  .box-card {
    p {
      text-align: right;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
    }
    margin-top: 14px;
    .block {
      padding: 30px 0;
      text-align: center;
      border-right: solid 1px var(--el-border-color);
      display: inline-block;
      width: 20%;
      box-sizing: border-box;
      vertical-align: top;
    }
    .block:last-child {
      border-right: none;
    }
  }
}
</style>
