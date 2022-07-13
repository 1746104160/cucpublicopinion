<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-13 11:20:31
 * @FilePath: /app/src/views/Login/components/resetForm.vue
-->

<template>
  <div class="form-container">
    <el-form ref="resetRef" :model="resetForm" status-icon :hide-required-asterisk="true" :rules="rules" label-width="100px" class="reset-form">
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="resetForm.email" autocomplete="off" placeholder="请输入注册邮箱">
          <template #append>
            <el-button :disabled="sendingCode" @click="handleGetEmailCaptcha">{{ codeText }}</el-button>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="captchaemail">
        <el-input v-model="resetForm.captchaemail" maxlength="6" autocomplete="off" placeholder="请输入验证码"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="resetForm.password" type="password" autocomplete="off" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input v-model="resetForm.checkPass" type="password" autocomplete="off"  placeholder="请确认密码"></el-input>
      </el-form-item>
      <el-form-item label="图片验证码" prop="captchapic">
        <el-row :gutter="20">
          <el-col :span="16">
              <div class="grid-content">
                <el-input v-model="resetForm.captchapic" autocomplete="off" placeholder="请输入图片验证码"></el-input>
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
          <el-button type="primary" @click="handleResetPwd">确认重置</el-button>
          <el-button type="primary" @click="handleToLogin">返回登陆</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormRules } from 'element-plus'
import { encrypt } from '@/utils/aes' // aes 密码加密
import Service from '../api/index'
import { validEmail, validEmailCaptcha, validPassword, validPicCaptcha } from '@/utils/validate'
import Cookies from 'js-cookie'
interface stateType {
  resetForm: {
    email: string
    captchaemail: string
    password: string
    checkPass: string
    captchapic: string
  },
  imgcode: string,
}

export default defineComponent({
  name: 'ResetForm',
  emits: ['toLogin'],
  setup (_props, { emit }) {
    const resetRef = ref()
    const state = reactive<stateType>({
      resetForm: {
        email: '',
        captchaemail: '',
        password: '',
        checkPass: '',
        captchapic: ''
      },
      imgcode: ''
    })
    const sendingCode = ref(false)
    const codeText = ref('获取验证码')
    const handleToLogin = () => {
      emit('toLogin')
    }
    // 已发送状态
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
     * @description 获取邮件验证码
     */
    const handleGetEmailCaptcha = async (): Promise<boolean> => {
      sendingCode.value = true
      try {
        const { email } = state.resetForm
        const data = {
          email
        }
        Service.postCaptcha(data).then(res => {
          ElMessage.success(res.message)
          getCodeSucces()
          return true
        }).catch(err => {
          sendingCode.value = false
          ElMessage.error(err.message)
        })
        return false
      } catch (err :any) {
        sendingCode.value = false
        ElMessage.error(err.message)
        return false
      }
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
     * @description 重置密码
     *
     */
    const handleResetPwd = async () => {
      resetRef.value.validate(async (valid: any) => {
        if (valid) {
          try {
            const { email, password, captchaemail, captchapic } = state.resetForm
            const data = {
              email,
              password: encrypt(password),
              captcha: captchapic,
              emailcode: captchaemail
            }
            Service.postResetPwd(data).then(res => {
              ElMessage.success(res.message)
              emit('toLogin')
            }).catch(err => {
              handleGetPicCaptcha()
              ElMessage.error(err.message)
            })
          } catch (err:any) {
            handleGetPicCaptcha()
            ElMessage.error(err.message)
          }
        }
        return false
      })
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
    const validatePicCaptcha = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入图片验证码'))
      } else if (!validPicCaptcha(value)) {
        callback(new Error('图片验证码共4位,不区分大小写'))
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
    const validateRetypePassword = (rule: any, value: any, callback: any) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (!validPassword(value)) {
        callback(new Error('密码格式不正确,包含数字和大小写字母,6-12位'))
      } else if (value !== state.resetForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const rules = reactive<FormRules>({
      password: [{ required: true, trigger: 'blur', validator: validatePassword }],
      email: [{ required: true, trigger: 'blur', validator: validateEmail }],
      captchaemail: [{ required: true, trigger: 'blur', validator: validateEmailcode }],
      checkPass: [{ required: true, trigger: 'blur', validator: validateRetypePassword }],
      captchapic: [{ required: true, trigger: 'blur', validator: validatePicCaptcha }]
    })
    onMounted(() => {
      handleGetPicCaptcha()
    })
    return {
      ...toRefs(state),
      rules,
      sendingCode,
      codeText,
      resetRef,
      handleGetEmailCaptcha,
      handleToLogin,
      handleResetPwd,
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

  .reset-form {
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
}
</style>
