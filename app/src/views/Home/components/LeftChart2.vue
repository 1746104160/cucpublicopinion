<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-13 23:50:03
 * @FilePath: /app/src/views/Home/components/LeftChart2.vue
-->
<template>
  <div class="left-chart-2">
    <div class="lc2-header">
      新闻类型
    </div>
    <dv-active-ring-chart :config="config" />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRef, toRefs } from 'vue'
export default defineComponent({
  name: 'LeftChart2',
  props: {
    categories: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    }
  },
  setup (props) {
    const data = toRef(props, 'categories')
    const state = reactive({
      config: {
        data,
        radius: '65%',
        activeRadius: '70%'
      }
    })
    return {
      ...toRefs(state)
    }
  }
})
</script>

<style lang="scss">
.left-chart-2 {
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;

  .lc2-header {
    text-align: center;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 30px;
    margin-bottom: 20px;
  }

  .dv-active-ring-chart {
    height: calc(100% - 80px);
  }
}
</style>
