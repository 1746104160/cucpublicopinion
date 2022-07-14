<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 20:13:52
 * @FilePath: /app/src/views/Login/components/ssoregisterForm.vue
-->

<template>
  <div class="form-container">
    <el-form ref="ssoregisterFormRef" :model="ssoregisterForm" status-icon :hide-required-asterisk="true" :rules="rules" label-width="100px" class="login-form">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="ssoregisterForm.username" autocomplete="off" placeholder="请输入邮箱/昵称"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="ssoregisterForm.password" type="password" autocomplete="off" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="captchapic">
        <el-row :gutter="20">
          <el-col :span="16">
            <div class="grid-content">
              <el-input v-model="ssoregisterForm.captchapic" autocomplete="off" placeholder="请输入图片验证码"></el-input>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="grid-content">
              <el-image @click="handleGetPicCaptcha" :src="imgcode" />
            </div>
          </el-col>
        </el-row>
      </el-form-item>

      <el-form-item>
        <div class="btn-container">
          <el-button type="primary" style="width: 100%" @click="handleRegister">注册</el-button>
          <el-button type="primary" @click="handletoLogin">已有账号?<em>去登陆</em></el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, toRefs, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormRules } from 'element-plus'
import { encrypt } from '@/utils/aes' // aes 密码加密
import Service from '@/views/Login/api/index'
import { validPicCaptcha, validCUCUsername } from '@/utils/validate'
import Cookies from 'js-cookie'
interface stateType {
  ssoregisterForm: {
    username: string
    password: string
    captchapic: string
  }
  imgcode: string
}
export default defineComponent({
  name: 'SSOssoregisterForm',
  emits: ['toLogin'],
  setup (_props, { emit }) {
    const ssoregisterFormRef = ref()
    const state = reactive<stateType>({
      ssoregisterForm: {
        username: '',
        password: '',
        captchapic: ''
      },
      imgcode: ''
    })
    const validateUsername = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else if (!validCUCUsername(value)) {
        callback(new Error('请输入正确的中传SSO用户名'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule: any, value: string, callback: any) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码至少6位'))
      } else {
        callback()
      }
    }
    const validatePicCaptcha = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入图片验证码'))
      } else if (!validPicCaptcha(value)) {
        callback(new Error('图片验证码共4位,不区分大小写'))
      } else {
        callback()
      }
    }

    const rules = reactive<FormRules>({
      username: [{ required: true, trigger: 'blur', validator: validateUsername }],
      password: [{ required: true, trigger: 'blur', validator: validatePassword }],
      captchapic: [{ required: true, trigger: 'blur', validator: validatePicCaptcha }]
    })

    // methods

    /**
     * @description  SSO注册
     *
     */
    const handleRegister = () => {
      ssoregisterFormRef.value.validate(async (valid: any) => {
        if (valid) {
          try {
            const { username, password, captchapic } = state.ssoregisterForm
            const data = {
              username,
              password: encrypt(password),
              captcha: captchapic
            }
            Service.postSSORegister(data).then(res => {
              ElMessage.success(res.message)
              emit('toLogin')
            }).catch(err => {
              handleGetPicCaptcha()
              ElMessage.error(err.message)
            })
          } catch (err: any) {
            handleGetPicCaptcha()
            ElMessage.error(err.message)
          }
        }
        return false
      })
    }
    /**
     * @description 获取图片验证码
     */
    const handleGetPicCaptcha = async (): Promise<boolean> => {
      try {
        const res = await Service.getCaptcha(Math.random())
        state.imgcode = res.data.data.captcha
        Cookies.set('requestid', res.headers['request-id'], { expires: 1 })
        return true
      } catch (err: any) {
        ElMessage(err)
        return false
      }
    }
    /**
     * @description 返回登录
     */
    const handletoLogin = () => {
      emit('toLogin')
    }
    onMounted(() => {
      handleGetPicCaptcha()
    })
    return {
      ...toRefs(state),
      ssoregisterFormRef,
      rules,
      handleRegister,
      handletoLogin,
      handleGetPicCaptcha
    }
  }
})
</script>
<style lang="scss" scoped>
.form-container {
  width: 100%;

  :deep(.el-input-group__append) {
    padding: 0px 7px;
  }

  :deep(.el-input-group__prepend) {
    padding: 0px 7px;
  }

  .login-form {
    width: 100%;
    margin: 0 auto;
  }

  .operation {
    text-align: center;
    position: absolute;
    top: 150%;
    left: 0;
    margin: auto;
    right: 0;
  }

  .btn-container {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
  }
}
</style>
