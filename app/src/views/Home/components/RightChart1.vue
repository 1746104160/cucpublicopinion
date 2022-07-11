<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-11 07:48:57
 * @FilePath: /app/src/views/Home/components/RightChart1.vue
-->
<template>
  <div class="right-chart-1">
    <div class="rc1-header">
      赵六
    </div>

    <div class="rc1-chart-container">
      <div class="left">
        <div class="number">
          262
        </div>
        <div>新闻数据总数</div>
      </div>

      <dv-capsule-chart class="right" :config="config" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
export default defineComponent({
  name: 'RightChart1',
  setup () {
    const state = reactive({
      config: {
        data: [
          {
            name: '新华网',
            value: 25
          },
          {
            name: '光明网',
            value: 66
          },
          {
            name: '人民网',
            value: 123
          },
          {
            name: '人民日报',
            value: 72
          },
          {
            name: '其他',
            value: 99
          }
        ],
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
.right-chart-1 {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;

  .rc1-header {
    font-size: 24px;
    font-weight: bold;
    height: 30px;
    line-height: 30px;
  }

  .rc1-chart-container {
    flex: 1;
    display: flex;
  }

  .left {
    width: 30%;
    font-size: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .number {
      font-size: 34px;
      color: #096dd9;
      font-weight: bold;
      margin-bottom: 30px;
    }
  }

  .right {
    flex: 1;
    padding-bottom: 20px;
    padding-right: 20px;
    box-sizing: border-box;
  }
}
</style>
