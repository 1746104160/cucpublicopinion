<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 14:46:18
 * @FilePath: /app/src/views/Home/components/LabelTag.vue
-->
<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 11:37:06
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 11:51:58
 * @FilePath: /app/src/views/Home/components/LabelTag.vue
-->
<template>
  <div class="label-tag">
    <template v-if="mergedConfig">
      <div v-for="(label, i) in mergedConfig.data" :key="label" class="label-item">
        {{ label }}
        <div :style="`background-color: ${mergedConfig.colors[i % mergedConfig.colors.length]};`" />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { deepClone, deepMerge } from '@/utils/deep'
import { reactive, watch, onMounted, defineComponent, toRefs } from 'vue'
export default defineComponent({
  name: 'LabelTag',
  props: {
    config: {
      type: Object,
      default: () => ({})
    }
  },
  setup (props) {
    const state = reactive({
      defaultConfig: {
        /**
         * @description Label data
         * @type {Array<String>}
         * @default data = []
         * @example data = ['label1', 'label2']
         */
        data: [],
        /**
         * @description Label color (Hex|Rgb|Rgba|color keywords)
         * @type {Array<String>}
         * @default colors = ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b']
         * @example colors = ['#666', 'rgb(0, 0, 0)', 'rgba(0, 0, 0, 1)', 'red']
         */
        colors: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b']
      },

      mergedConfig: {
        data: [],
        colors: ['#00baff', '#3de7c9', '#fff', '#ffc530', '#469f4b']
      }
    })

    watch(() => props.config, () => {
      mergeConfig()
    })

    function mergeConfig () {
      state.mergedConfig = deepMerge(deepClone(state.defaultConfig, true), props.config || {})
    }

    onMounted(() => {
      mergeConfig()
    })
    return {
      ...toRefs(state)
    }
  }
})
</script>

<style lang="scss">
.label-tag {
  display: flex;
  justify-content: center;
  align-items: center;

  .label-item {
    margin: 5px;
    font-size: 15px;
    display: flex;
    align-items: center;

    div {
      width: 12px;
      height: 12px;
      margin-left: 5px;
    }
  }
}
</style>
