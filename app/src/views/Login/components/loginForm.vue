<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:39:22
 * @FilePath: /app/src/views/Login/components/loginForm.vue
-->

<template>
  <div class="form-container">
    <el-form ref="loginFormRef" :model="loginForm" status-icon :hide-required-asterisk="true" :rules="rules" label-width="100px" class="login-form">
      <el-form-item label="用户名" prop="account">
        <el-input v-model="loginForm.account" autocomplete="off" placeholder="请输入邮箱/昵称"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="loginForm.password" type="password" autocomplete="off" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="captchapic">
        <el-row :gutter="20">
          <el-col :span="13">
            <div class="grid-content">
              <el-input v-model="loginForm.captchapic" autocomplete="off" placeholder="请输入图片验证码"></el-input>
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
          <el-button type="primary" style="width: 100%" @click="handleLogin">登录</el-button>
        </div>
        <div class="operation">
          <el-button type="primary" @click="handleSSORegister">中传账号注册</el-button>
          <el-button type="primary" @click="handleRegister">系统注册</el-button>
          <el-button type="primary" @click="handleForget">忘记密码</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>
<script lang="ts">
import Cookies from 'js-cookie'
import { defineComponent, ref, toRefs, reactive, onMounted } from 'vue'
import { useStore } from '@/store/index'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormRules } from 'element-plus'
import { encrypt } from '@/utils/aes' // aes 密码加密
import Service from '@/views/Login/api/index'
import { validPicCaptcha } from '@/utils/validate'
import { useStorage } from 'vue3-storage'
interface stateType {
  loginForm: {
    account: string
    password: string
    captchapic: string
  }
  imgcode: string
}
export default defineComponent({
  name: 'LoginForm',
  emits: ['toReset', 'toRegister', 'toSSORegister'],
  setup (_props, { emit }) {
    const store = useStore()
    const storage = useStorage()
    const route = useRoute()
    const router = useRouter()
    const loginFormRef = ref()
    const state = reactive<stateType>({
      loginForm: {
        account: '',
        password: '',
        captchapic: ''
      },
      imgcode: ''
    })
    const validateaccount = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else if (value.length < 4) {
        callback(new Error('用户名格式不正确'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码格式不正确'))
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
      account: [{ required: true, trigger: 'blur', validator: validateaccount }],
      password: [{ required: true, trigger: 'blur', validator: validatePassword }],
      captchapic: [{ required: true, trigger: 'blur', validator: validatePicCaptcha }]
    })

    // methods

    /**
     * @description  用户登录接口
     *
     */
    const handleLogin = () => {
      loginFormRef.value.validate(async (valid: any) => {
        if (valid) {
          try {
            const { account, password, captchapic } = state.loginForm
            const data = {
              account,
              password: encrypt(password),
              captcha: captchapic
            }
            Service.postLogin(data).then(res => {
              if (res.data.accessToken) {
                storage.setStorageSync('accessToken', res.data.accessToken, 24 * 60 * 60 * 1000)
                store.dispatch('userModule/getUserInfo')
                Cookies.remove('requestid')
                if (route.query.redirect) {
                  const path = route.query.redirect
                  router.push({ path: path as string })
                } else {
                  router.push('/home')
                }
              }
            }).catch(err => {
              ElMessage({
                type: 'warning',
                message: err.message
              })
            })
          } catch (err: any) {
            ElMessage({
              type: 'warning',
              message: err.message
            })
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
     * @description 忘记密码
     */
    const handleForget = () => {
      emit('toReset')
    }
    /**
     * @description 立即注册
     */
    const handleRegister = () => {
      emit('toRegister')
    }
    /**
     * @description 使用中传SSO登录
     */
    const handleSSORegister = () => {
      emit('toSSORegister')
    }
    onMounted(() => {
      handleGetPicCaptcha()
    })
    return {
      ...toRefs(state),
      loginFormRef,
      rules,
      handleLogin,
      handleRegister,
      handleForget,
      handleGetPicCaptcha,
      handleSSORegister
    }
  }
})
</script>
<style lang="stylus" scoped>
.form-container{
  width:100%;
  :deep(.el-input-group__append) {
    padding:0px 7px;
  }

  :deep(.el-input-group__prepend) {
    padding:0px 7px;
  }

  .login-form{
    width:100%;
    margin: 0 auto;
  }

  .operation{
    text-align:center;
    position:absolute;
    top:100%;
    left: 0;
    margin: auto;
    right: 0;
  }
  .btn-container{
    width:100%;
    display :flex;
    flex-direction:row;
    justify-content :flex-start;
    align-items :center;
  }
}
</style>
