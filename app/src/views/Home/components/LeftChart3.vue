<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 14:56:45
 * @FilePath: /app/src/views/Home/components/LeftChart3.vue
-->
<template>
  <div class="left-chart-3">
    <div class="lc3-header">
      王五
    </div>
    <div class="lc3-details">
      新闻数据总数<span>245</span>
    </div>
    <dv-capsule-chart class="lc3-chart" :config="config" />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
export default defineComponent({
  name: 'LeftChart2',
  setup () {
    const state = reactive({
      config: {
        data: [
          {
            name: '新华网',
            value: 78
          },
          {
            name: '光明网',
            value: 54
          },
          {
            name: '人民网',
            value: 123
          },
          {
            name: '人民日报',
            value: 167
          },
          {
            name: '其他',
            value: 77
          }
        ],
        colors: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        unit: '件'
      }
    })
    return {
      ...toRefs(state)
    }
  }
})
</script>

<style lang="scss">
.left-chart-3 {
  width: 100%;
  height: 33%;
  display: flex;
  flex-direction: column;

  .lc3-header {
    height: 20px;
    line-height: 20px;
    font-size: 16px;
    text-indent: 20px;
    margin-top: 10px;
  }

  .lc3-details {
    height: 40px;
    font-size: 16px;
    display: flex;
    align-items: center;
    text-indent: 20px;

    span {
      color: #096dd9;
      font-weight: bold;
      font-size: 35px;
      margin-left: 20px;
    }
  }

  .lc3-chart {
    flex: 1;
  }
}
</style>
