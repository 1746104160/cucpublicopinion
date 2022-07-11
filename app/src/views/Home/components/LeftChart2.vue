<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 14:56:09
 * @FilePath: /app/src/views/Home/components/LeftChart2.vue
-->
<template>
  <div class="left-chart-2">
    <div class="lc2-header">
      李四
    </div>
    <div class="lc2-details">
      新闻数据总数<span>245</span>
    </div>
    <dv-charts class="lc2-chart" :option="option" />
    <dv-decoration-2 style="height:10px;" />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from 'vue'
export default defineComponent({
  name: 'LeftChart2',
  setup () {
    const state = reactive({
      option: {
        series: [
          {
            type: 'pie',
            data: [
              { name: '新华网', value: 93 },
              { name: '光明网', value: 32 },
              { name: '人民网', value: 65 },
              { name: '人民日报', value: 44 },
              { name: '其他', value: 52 }
            ],
            radius: ['45%', '65%'],
            insideLabel: {
              show: false
            },
            outsideLabel: {
              labelLineEndLength: 10,
              formatter: '{percent}%\n{name}',
              style: {
                fontSize: 14,
                fill: '#fff'
              }
            }
          }
        ],
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b']
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
  height: 30%;
  display: flex;
  flex-direction: column;

  .lc2-header {
    height: 20px;
    line-height: 20px;
    font-size: 16px;
    text-indent: 20px;
    margin-top: 10px;
  }

  .lc2-details {
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

  .lc2-chart {
    height: calc(100% - 80px);
  }
}
</style>
