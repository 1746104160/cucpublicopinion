<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 14:54:23
 * @FilePath: /app/src/views/Home/components/LeftChart1.vue
-->
<template>
  <div class="left-chart-1">
    <div class="lc1-header">
      张三
    </div>
    <div class="lc1-details">
      新闻数据总数<span>430</span>
    </div>
    <dv-capsule-chart class="lc1-chart" :config="config" />
    <dv-decoration-2 style="height:10px;" />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
export default defineComponent({
  name: 'LeftChart1',
  setup () {
    const state = reactive({
      config: {
        data: [
          {
            name: '新华网',
            value: 167
          },
          {
            name: '光明网',
            value: 67
          },
          {
            name: '人民网',
            value: 123
          },
          {
            name: '人民日报',
            value: 55
          },
          {
            name: '其他',
            value: 98
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
.left-chart-1 {
  width: 100%;
  height: 37%;
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
