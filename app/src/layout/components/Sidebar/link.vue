<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:32:00
 * @FilePath: /app/src/layout/components/Sidebar/link.vue
-->

<template>
  <component :is="linkProps(to)">
    <slot />
  </component>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import { isExternal } from '@/utils/validate.js'

export default defineComponent({
  name: 'SidebarLink',
  props: {
    to: {
      type: String,
      required: true
    }
  },
  setup () {
    // methods
    const linkProps = (url: string) => {
      if (isExternal(url)) {
        return {
          is: 'a',
          href: url,
          target: '_blank',
          rel: 'noopener'
        }
      }
      return {
        is: 'router-link',
        to: url
      }
    }
    return {
      linkProps
    }
  }
})
</script>
