<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 00:11:35
 * @FilePath: /app/src/views/Home/components/RightChart.vue
-->
<template>
  <div class="right-chart">
    <div class="rc-header">
      聚类分析
    </div>

    <div class="rc-chart-container">
      <dv-scroll-ranking-board :config="config" style="height:88%;"/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRef, toRefs } from 'vue'
export default defineComponent({
  name: 'RightChart',
  props: {
    clusters: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    }
  },
  setup (props) {
    const data = toRef(props, 'clusters')
    const state = reactive({
      config: {
        data,
        unit: '条'
      }
    })
    return {
      ...toRefs(state)
    }
  }
})
</script>

<style lang="scss">
.right-chart {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;

  .rc-header {
    font-size: 24px;
    font-weight: bold;
    height: 30px;
    line-height: 30px;
  }

  .rc-chart-container {
    flex: 1;
    display: flex;
  }
}
</style>
