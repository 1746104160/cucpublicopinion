<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-07 15:23:17
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 21:30:01
-->
<template>
  <div>
    <el-form ref="formRef" :model="form" :rules="rules" label-position="right" label-width="100px">
      <el-form-item label="角色名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入角色名称"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="description">
        <el-input v-model="form.description" placeholder="请输入备注"></el-input>
      </el-form-item>
      <el-row :gutter="20">
        <el-col :span="4" :offset="10">
          <el-button size="small" type="primary" @click="submitForm">新增角色</el-button>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>
<script lang="ts">
import { ElMessage, FormRules } from 'element-plus'
import { defineComponent, reactive, toRefs, ref } from 'vue'
import Service from '../api'

export default defineComponent({
  name: 'RolesNew',
  emits: ['success'],
  setup (_props, { emit }) {
    const validateRolename = (rule: any, value: string, callback: any) => {
      if (!value) {
        callback(new Error('请输入角色名称'))
      } else if (value.length < 2) {
        callback(new Error('角色名称长度不能小于2'))
      } else {
        callback()
      }
    }
    const rules = reactive<FormRules>({
      name: [{ required: true, trigger: 'blur', validator: validateRolename }],
      description: [{ required: true, trigger: 'blur', message: '请输入角色描述' }]
    })
    const formRef = ref()
    const state = reactive({
      form: {
        name: '',
        description: ''
      }
    })
    /**
     * @description 提交新建角色处理函数
     */
    const submitForm = () => {
      formRef.value.validate((valid: any): boolean => {
        if (valid) {
          Service.createRole(state.form).then((res: any) => {
            state.form.name = state.form.description = ''
            emit('success')
            ElMessage.success(res.message)
            return true
          }).catch((err: any) => {
            ElMessage.error(err.message)
            return false
          })
        }
        return false
      })
    }
    return {
      submitForm,
      rules,
      formRef,
      ...toRefs(state)
    }
  }
})
</script>
