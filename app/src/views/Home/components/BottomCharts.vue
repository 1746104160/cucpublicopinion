<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 00:43:30
 * @FilePath: /app/src/views/Home/components/BottomCharts.vue
-->

<template>
  <div class="bottom-charts">
    <div class="bc-chart-item">
      <div class="bcci-header">
        {{ title1 }}
      </div>
      <dv-active-ring-chart :config="config1" />
    </div>
    <dv-decoration-2 class="decoration-1" :reverse="true" style="width:5px;" />

    <div class="bc-chart-item">
      <div class="bcci-header">
        {{ title2 }}
      </div>
      <dv-active-ring-chart :config="config2" />
    </div>

    <dv-decoration-2 class="decoration-2" :reverse="true" style="width:5px;" />

    <div class="bc-chart-item">
      <div class="bcci-header">
        {{ title3 }}
      </div>
      <dv-active-ring-chart :config="config3" />
    </div>

    <dv-decoration-2 class="decoration-3" :reverse="true" style="width:5px;" />

    <div class="bc-chart-item">
      <div class="bcci-header">
        {{ title4 }}
      </div>
      <dv-active-ring-chart :config="config4" />
    </div>
  </div>
</template>

<script lang="ts">
import { reactive, defineComponent, toRef, toRefs } from 'vue'
export default defineComponent({
  name: 'BottomCharts',
  props: {
    config1: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    },
    config2: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    },
    config3: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    },
    config4: {
      default: () => { return [{ name: '', value: 0 }] as any[] }
    },
    title1: {
      type: String,
      default: ''
    },
    title2: {
      type: String,
      default: ''
    },
    title3: {
      type: String,
      default: ''
    },
    title4: {
      type: String,
      default: ''
    }
  },
  setup (props) {
    const state = reactive({
      config1: {
        data: toRef(props, 'config1'),
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      config2: {
        data: toRef(props, 'config2'),
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      config3: {
        data: toRef(props, 'config3'),
        color: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b'],
        radius: '65%',
        activeRadius: '70%'
      },

      config4: {
        data: toRef(props, 'config4'),
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
