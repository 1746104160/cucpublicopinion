<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-07 15:23:17
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 23:26:20
 * @FilePath: /app/src/views/Dashboard/components/usersEdit.vue
-->

<template>
  <div class="wrapper">
    <el-card class="transfer">
      <el-transfer v-model="value" v-loading="false" :data="data" :titles="['全部角色', '已添加角色']" />
    </el-card>
    <br />
    <el-row :gutter="20">
      <el-col :span="4" :offset="10">
        <el-button size="small" type="primary" @click="submitForm">调整用户</el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script lang="ts">
import { ElMessage } from 'element-plus'
import { defineComponent, onMounted, reactive, ref, toRef, toRefs, watchEffect } from 'vue'
import Service from '../api'
export default defineComponent({
  name: 'UsersEdit',
  props: {
    currentUser: {
      type: Object,
      default: () => ({
        userid: 0,
        role: ['standard']
      })
    }
  },
  emits: ['success'],
  setup (props, { emit }) {
    const user = toRef(props, 'currentUser')
    const state = reactive({
      data: [] as any[]
    })
    const value = ref([] as any[])
    /**
     * @description 提交更新roles
     */
    const fetchdata = async () => {
      const { data } = await Service.getAllSimpleRoles()
      data.forEach((role:any) => {
        state.data.push({
          key: role.name,
          label: role.name
        })
      })
    }
    const submitForm = () => {
      if (value.value.length === 0) {
        value.value.push('standard')
      }
      Service.updateUserInfo({ userid: user.value.userid, role: value.value }).then((res: any) => {
        value.value = [] as any[]
        emit('success')
        ElMessage.success(res.message)
        return true
      }).catch((err: any) => {
        ElMessage.error(err.message)
        return false
      })
    }
    onMounted(() => {
      fetchdata()
    })
    watchEffect(() => {
      user.value.role.forEach((role: { name: string }) => {
        value.value.push(role.name)
      })
    })
    return {
      ...toRefs(state),
      submitForm,
      value
    }
  }
})
</script>
