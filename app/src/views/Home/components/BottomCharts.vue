<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-11 07:59:40
 * @FilePath: /app/src/views/Home/components/BottomCharts.vue
-->

<template>
  <div class="bottom-charts">
    <div class="bc-chart-item">
      <div class="bcci-header">
        赵钱
      </div>
      <dv-active-ring-chart :config="config1" />
      <Label-Tag :config="labelConfig" />
    </div>
    <dv-decoration-2 class="decoration-1" :reverse="true" style="width:5px;" />

    <div class="bc-chart-item">
      <div class="bcci-header">
        孙李
      </div>
      <dv-active-ring-chart :config="config2" />
      <Label-Tag :config="labelConfig" />
    </div>

    <dv-decoration-2 class="decoration-2" :reverse="true" style="width:5px;" />

    <div class="bc-chart-item">
      <div class="bcci-header">
        周吴
      </div>
      <dv-active-ring-chart :config="config3" />
      <Label-Tag :config="labelConfig" />
    </div>

    <dv-decoration-2 class="decoration-3" :reverse="true" style="width:5px;" />

    <div class="bc-chart-item">
      <div class="bcci-header">
        郑王
      </div>
      <dv-active-ring-chart :config="config4" />
      <Label-Tag :config="labelConfig" />
    </div>
  </div>
</template>

<script lang="ts">
import { reactive, defineComponent, toRefs } from 'vue'
import LabelTag from './LabelTag.vue'
export default defineComponent({
  name: 'BottomCharts',
  components: {
    LabelTag
  },
  setup () {
    const state = reactive({
      config1: {
        data: [
          {
            name: '人民日报',
            value: 356
          },
          {
            name: '新华网',
            value: 215
          },
          {
            name: '光明网',
            value: 90
          },
          {
            name: '其他',
            value: 317
          }
        ],
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      config2: {
        data: [
          {
            name: '人民日报',
            value: 615
          },
          {
            name: '新华网',
            value: 322
          },
          {
            name: '光明网',
            value: 198
          },
          {
            name: '其他',
            value: 80
          }
        ],
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      config3: {
        data: [
          {
            name: '人民日报',
            value: 452
          },
          {
            name: '新华网',
            value: 512
          },
          {
            name: '光明网',
            value: 333
          },
          {
            name: '其他',
            value: 255
          }
        ],
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      config4: {
        data: [
          {
            name: '人民日报',
            value: 156
          },
          {
            name: '新华网',
            value: 415
          },
          {
            name: '光明网',
            value: 90
          },
          {
            name: '其他',
            value: 210
          }
        ],
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      labelConfig: {
        data: ['人民日报', '新华网', '光明网', '其他']
      }
    })
    return {
      ...toRefs(state)
    }
  }
})
</script>

<style lang="scss">
.bottom-charts {
  width: 100%;
  height: 100%;
  display: flex;
  position: relative;

  .bc-chart-item {
    width: 25%;
    height: 100%;
    padding-top: 20px;
    box-sizing: border-box;
  }

  .bcci-header {
    height: 50px;
    text-align: center;
    line-height: 50px;
    font-size: 20px;
  }

  .dv-active-ring-chart {
    height: calc(100% - 80px);
  }

  .label-tag {
    height: 30px;
  }

  .active-ring-name {
    font-size: 18px !important;
  }

  .decoration-1, .decoration-2, .decoration-3 {
    display: absolute;
    left: 0%;
  }
}
</style>
