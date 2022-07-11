<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-11 11:25:56
 * @FilePath: /app/src/views/Login/components/registerForm.vue
-->

<template>
  <div class="form-container">
    <el-form ref="registerRef" :model="registerForm" status-icon :hide-required-asterisk="true" :rules="rules" label-width="100px" class="register-form">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="registerForm.username" autocomplete="off" placeholder="请输入昵称"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="registerForm.email" autocomplete="off" placeholder="请输入注册邮箱">
          <template #append>
            <el-button :disabled="sendingCode" @click="handleGetEmailCaptcha">{{ codeText }}</el-button>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item label="邮件验证码" prop="captchaemail">
        <el-input v-model="registerForm.captchaemail" maxlength="10" autocomplete="off" placeholder="请输入验证码"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="registerForm.password" type="password" autocomplete="off" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input v-model="registerForm.checkPass" type="password" autocomplete="off" placeholder="请确认密码"></el-input>
      </el-form-item>
      <el-form-item label="图片验证码" prop="captchapic">
        <el-row :gutter="20">
          <el-col :span="13">
            <div class="grid-content">
              <el-input v-model="registerForm.captchapic" autocomplete="off" placeholder="请输入图片验证码"></el-input>
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
        <div class="operation">
          <el-button type="primary" @click="handleRegister">完成注册</el-button>
          <el-button type="primary" @click="handleLogin">已有账号?<em>去登陆</em></el-button>
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
import Service from '../api/index'
import { validEmail, validEmailCaptcha, validPassword, validPicCaptcha, validUsername } from '@/utils/validate'
import Cookies from 'js-cookie'
interface stateType {
  registerForm: {
    username: string
    email: string
    captchaemail: string
    password: string
    checkPass: string
    captchapic: string
  }
  imgcode: string
}
export default defineComponent({
  name: 'RegisterForm',
  emits: ['toLogin'],
  setup (_props, { emit }) {
    const registerRef = ref()
    const sendingCode = ref(false)
    const codeText = ref('获取验证码')
    const state = reactive<stateType>({
      registerForm: {
        username: '',
        email: '',
        captchaemail: '',
        password: '',
        checkPass: '',
        captchapic: ''
      },
      imgcode: ''
    })
    const validateUsername = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入用户名'))
      } else if (!validUsername(value)) {
        callback(new Error('用户名以英文字母开头,6-16位'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入邮箱'))
      } else if (!validEmail(value)) {
        callback(new Error('请输入正确的邮箱'))
      } else {
        callback()
      }
    }
    const validateEmailcode = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入确认密码'))
      } else if (!validEmailCaptcha(value)) {
        callback(new Error('邮件验证码共6位,区分大小写,请从邮件中复制'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (!validPassword(value)) {
        callback(new Error('密码格式不正确,包含数字和大小写字母,6-12位'))
      } else {
        callback()
      }
    }
    const validateRetypePassword = (rule: any, value: any, callback: any) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (!validPassword(value)) {
        callback(new Error('密码格式不正确,包含数字和大小写字母,6-12位'))
      } else if (value !== state.registerForm.password) {
        callback(new Error('两次输入密码不一致!'))
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
      email: [{ required: true, trigger: 'blur', validator: validateEmail }],
      captchaemail: [{ required: true, trigger: 'blur', validator: validateEmailcode }],
      password: [{ required: true, trigger: 'blur', validator: validatePassword }],
      checkPass: [{ required: true, trigger: 'blur', validator: validateRetypePassword }],
      captchapic: [{ required: true, trigger: 'blur', validator: validatePicCaptcha }]
    })

    // methods

    /**
     * @description 处理注册接口
     */
    const handleRegister = () => {
      registerRef.value.validate(async (valid: any) => {
        if (valid) {
          try {
            const { username, email, password, captchaemail, captchapic } = state.registerForm
            const data = {
              username,
              email,
              emailcode: captchaemail,
              password: encrypt(password),
              captcha: captchapic
            }
            Service.postRegister(data)
              .then((res: any) => {
                ElMessage({
                  type: 'success',
                  message: '注册成功'
                })
                emit('toLogin')
              }).catch((err) => {
                ElMessage({
                  type: 'warning',
                  message: err.message
                })
              })
          } catch (err: any) {
            ElMessage({
              type: 'error',
              message: err.message
            })
          }
        }
      })
    }
    /**
     * @description 获取验证码状态
     */
    const getCodeSucces = () => {
      let countDown = 60
      const interval = setInterval(() => {
        if (countDown > 0) {
          codeText.value = `已发送(${countDown}s)`
          countDown -= 1
        } else {
          clearInterval(interval)
          sendingCode.value = false
          codeText.value = '获取验证码'
        }
      }, 1000)
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
     * @description 获取验证码
     */
    const handleGetEmailCaptcha = async (): Promise<boolean> => {
      sendingCode.value = true
      try {
        const { email } = state.registerForm
        const data = {
          email
        }
        Service.postCaptcha(data).then(res => {
          ElMessage({
            type: 'success',
            message: res.message
          })
          getCodeSucces()
          return true
        }).catch(err => {
          sendingCode.value = false
          ElMessage({
            type: 'warning',
            message: err.message
          })
        })
        return false
      } catch (err :any) {
        sendingCode.value = false
        ElMessage({
          type: 'warning',
          message: err.message
        })
        return false
      }
    }
    /**
     * @description 返回登录
     */
    const handleLogin = () => {
      emit('toLogin')
    }
    onMounted(() => {
      handleGetPicCaptcha()
    })
    return {
      ...toRefs(state),
      registerRef,
      sendingCode,
      codeText,
      rules,
      handleLogin,
      handleRegister,
      handleGetEmailCaptcha,
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

  .register-form {
    width: 100%;
    margin: 0 auto;
  }

  .operation {
    text-align: center;
    position: absolute;
    top: 100%;
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
