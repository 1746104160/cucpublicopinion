<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-13 23:50:52
 * @FilePath: /app/src/views/Home/components/LeftChart1.vue
-->
<template>
  <div class="left-chart-1">
    <div class="lc1-header">
      情感分析
    </div>
    <dv-capsule-chart class="lc1-chart" :config="config" />
    <dv-decoration-2 style="height:10px;" />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRef, toRefs } from 'vue'
export default defineComponent({
  name: 'LeftChart1',
  props: {
    sentiments: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    }
  },
  setup (props) {
    const data = toRef(props, 'sentiments')
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
.left-chart-1 {
  width: 100%;
  height: 50%;
  display: flex;
  flex-grow: 0;
  flex-direction: column;

  .lc1-header {
    text-align: center;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 30px;
    margin-bottom: 20px;
  }

  .lc1-details {
    height: 50px;
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

  .lc1-chart {
    flex: 1;
  }
}
</style>
