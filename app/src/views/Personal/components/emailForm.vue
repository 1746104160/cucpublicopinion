<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 14:19:38
 * @FilePath: /app/src/views/Personal/components/emailForm.vue
-->

<template>
  <div class="form-container">
    <el-result v-if="!cuc" icon="error" title="请先绑定中传SSO账号" />
    <div v-else>
      <el-steps :active="active" finish-status="success" align-center>
        <el-step title="验证中传SSO账号"></el-step>
        <el-step title="绑定邮箱"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>
      <template v-if="active == 0">
        <el-form
          ref="verifyRef"
          :model="verifyForm"
          status-icon
          :hide-required-asterisk="true"
          :rules="verifyrules"
          label-width="100px"
          class="reset-form"
        >
          <el-form-item label="验证中传SSO账号" prop="account">
            <el-input
              v-model="verifyForm.account"
              autocomplete="off"
              placeholder="请输入绑定SSO账号"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :disabled="failure" @click="handleNextStep">{{
              nextstepText
            }}</el-button>
            <el-button @click="resetValue">清空表单</el-button>
          </el-form-item>
        </el-form>
      </template>
      <template v-if="active == 1">
        <el-form
          ref="resetRef"
          :model="resetForm"
          status-icon
          :hide-required-asterisk="true"
          :rules="resetrules"
          label-width="100px"
          class="reset-form"
        >
          <el-form-item label="SSO登录密码" prop="cucpassword">
            <el-input
              v-model="resetForm.cucpassword"
              autocomplete="off"
              type="password"
              placeholder="请输入中传SSO账号密码"
            ></el-input>
          </el-form-item>
          <el-form-item label="新的邮箱" prop="email">
            <el-input
              v-model="resetForm.email"
              autocomplete="off"
              placeholder="请输入密码"
              ><template #append>
                <el-button :disabled="sendingCode" @click="handleGetEmailCaptcha">{{
                  codeText
                }}</el-button>
              </template></el-input
            >
          </el-form-item>
          <el-form-item label="邮件验证码" prop="captchaemail">
            <el-input
              v-model="resetForm.captchaemail"
              type="password"
              autocomplete="off"
              placeholder="请输入邮件验证码"
            ></el-input>
          </el-form-item>
          <el-form-item label="图片验证码" prop="captchapic">
            <el-row :gutter="20">
              <el-col :span="13">
                <div class="grid-content">
                  <el-input
                    v-model="resetForm.captchapic"
                    autocomplete="off"
                    placeholder="请输入图片验证码"
                  ></el-input>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="grid-content">
                  <div @click="handleGetPicCaptcha" v-html="imgcode"></div>
                </div>
              </el-col>
            </el-row>
          </el-form-item>
          <el-button type="primary" @click="handleLastStep">上一步</el-button>
          <el-button type="primary" @click="handleResetEmail">确认重置密码</el-button>
        </el-form>
      </template>
      <template v-if="active == 2">
        <el-result icon="success" title="操作成功" />
      </template>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormRules } from 'element-plus'
import { encrypt } from '@/utils/aes'
import { useStore } from '@/store'
import Service from '../api/index'
import Cookies from 'js-cookie'
import {
  validCUCUsername,
  validEmail,
  validEmailCaptcha,
  validPicCaptcha
} from '@/utils/validate'

interface stateType {
  verifyForm: {
    account: string;
  };
  resetForm: {
    email: string;
    captchaemail: string;
    cucpassword: string;
    captchapic: string;
  };
  imgcode: string;
}

export default defineComponent({
  name: 'ResetemailForm',
  setup () {
    const store = useStore()
    const resetRef = ref()
    const verifyRef = ref()
    const cuc = ref(JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount)
    const state = reactive<stateType>({
      verifyForm: {
        account: ''
      },
      resetForm: {
        email: '',
        captchaemail: '',
        cucpassword: '',
        captchapic: ''
      },
      imgcode: ''
    })
    const active = ref(0)
    const selectedAccType = ref()
    const failure = ref(false)
    const nextstepText = ref('下一步')
    // 校验状态
    const getNextStepFailure = () => {
      let countDown = 60
      const interval = setInterval(() => {
        if (countDown > 0) {
          nextstepText.value = `账号验证错误，请稍后再试(${countDown}s)`
          countDown -= 1
        } else {
          clearInterval(interval)
          failure.value = false
          nextstepText.value = '获取验证码'
        }
      }, 1000)
    }
    const codeText = ref('获取验证码')
    const sendingCode = ref(false)
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
     * @description 下一步
     */
    const handleNextStep = () => {
      failure.value = true
      verifyRef.value.validate((valid: any) => {
        if (valid) {
          if (
            parseInt(state.verifyForm.account) !==
            JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount
          ) {
            getNextStepFailure()
            return false
          } else {
            active.value = 1
            return true
          }
        }
        return false
      })
    }
    /**
     * @description 上一步
     */
    const handleLastStep = () => {
      active.value = 0
      return true
    }
    /**
     * @description 重置表单
     */
    const resetValue = () => {
      verifyRef.value.resetFields()
    }
    /**
     * @description 获取邮件验证码
     */
    const handleGetEmailCaptcha = async (): Promise<boolean> => {
      sendingCode.value = true
      try {
        const { email } = state.resetForm
        if (!validEmail(email)) {
          sendingCode.value = false
          return false
        }
        const data = {
          email
        }
        Service.postCaptcha(data)
          .then((res) => {
            ElMessage({
              type: 'success',
              message: res.message
            })
            getCodeSucces()
            return true
          })
          .catch((err) => {
            sendingCode.value = false
            ElMessage({
              type: 'warning',
              message: err.message
            })
          })
        return false
      } catch (err: any) {
        sendingCode.value = false
        ElMessage({
          type: 'warning',
          message: err.message
        })
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
     * @description 重置邮箱
     *
     */
    const handleResetEmail = async () => {
      resetRef.value.validate(async (valid: any) => {
        if (valid) {
          try {
            const { account } = state.verifyForm
            const { cucpassword, email, captchaemail, captchapic } = state.resetForm
            const data = {
              account,
              verify: encrypt(cucpassword),
              email,
              emailcode: captchaemail,
              captcha: captchapic
            }
            Service.postResetEmail(data)
              .then((res) => {
                store.dispatch('userModule/getUserInfo')
                active.value = 2
                ElMessage({
                  type: 'warning',
                  message: res.message
                })
              })
              .catch((err) => {
                ElMessage({
                  type: 'success',
                  message: err.message
                })
              })
          } catch (err) {
            console.error(err)
          }
        }
        return false
      })
    }
    const validateCUCPassword = (rule: any, value: string, callback: any) => {
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
    const validateAccount = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请选择验证账号'))
      } else if (!validCUCUsername(value)) {
        callback(new Error('请输入正确的中传SSO账号'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请选择验证账号'))
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
    const verifyrules = reactive<FormRules>({
      account: [{ required: true, trigger: 'blur', validator: validateAccount }]
    })
    const resetrules = reactive<FormRules>({
      cucpassword: [{ required: true, trigger: 'blur', validator: validateCUCPassword }],
      captchaemail: [{ required: true, trigger: 'blur', validator: validateEmailcode }],
      email: [{ required: true, trigger: 'blur', validator: validateEmail }],
      captchapic: [{ required: true, trigger: 'blur', validator: validatePicCaptcha }]
    })
    onMounted(() => {
      handleGetPicCaptcha()
    })
    return {
      ...toRefs(state),
      verifyrules,
      resetrules,
      resetRef,
      verifyRef,
      sendingCode,
      codeText,
      handleResetEmail,
      handleGetEmailCaptcha,
      handleGetPicCaptcha,
      active,
      selectedAccType,
      handleNextStep,
      handleLastStep,
      resetValue,
      failure,
      nextstepText,
      cuc
    }
  }
})
</script>
<style lang="scss" scoped>
.form-container {
  width: 100%;

  .reset-form {
    width: 100%;
    margin: 0 auto;
  }
}
</style>
