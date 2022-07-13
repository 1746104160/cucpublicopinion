<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-13 20:03:47
 * @FilePath: /app/src/views/Personal/components/pwdForm.vue
-->

<template>
  <div class="form-container">
    <el-steps :active="active" finish-status="success" align-center>
      <el-step title="验证账号绑定信息"></el-step>
      <el-step title="设置密码"></el-step>
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
        <el-form-item label="验证绑定信息" prop="account">
          <el-input
            v-model="verifyForm.account"
            autocomplete="off"
            placeholder="请输入绑定账号"
          >
            <template #prepend>
              <el-form-item prop="mode">
              <el-select
                v-model="verifyForm.mode"
                style="width: 120px"
                placeholder="请选择"
              >
                <el-option label="邮箱" value="email"></el-option>
                <el-option label="中传SSO" value="cuc"></el-option>
              </el-select>
              </el-form-item>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" :disabled="failure" @click="handleNextStep">{{ nextstepText }}</el-button>
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
      <el-form-item
          v-if="verifyForm.mode === 'email'"
          label="邮件验证码"
          prop="captchaemail"
        >
          <el-input
            v-model="resetForm.captchaemail"
            maxlength="6"
            autocomplete="off"
            placeholder="请输入验证码"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-else-if="verifyForm.mode === 'cuc'"
          label="SSO登录密码"
          prop="cucpassword"
        >
          <el-input
            v-model="resetForm.cucpassword"
            autocomplete="off"
            type="password"
            placeholder="请输入中传SSO账号密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="新的密码" prop="password">
          <el-input
            v-model="resetForm.password"
            type="password"
            autocomplete="off"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input
            v-model="resetForm.checkPass"
            type="password"
            autocomplete="off"
            placeholder="请确认密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="图片验证码" prop="captchapic">
          <el-row :gutter="20">
            <el-col :span="16">
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
                <el-image @click="handleGetPicCaptcha" :src="imgcode" />
              </div>
            </el-col>
          </el-row>
        </el-form-item>
          <el-button type="primary" @click="handleLastStep">上一步</el-button>
          <el-button type="primary" @click="handleResetPwd">确认重置密码</el-button>
      </el-form>
    </template>
    <template v-if="active == 2">
      <el-result icon="success" title="操作成功" />
    </template>
  </div>
</template>
<script lang="ts">
import { defineComponent, reactive, toRefs, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormRules } from 'element-plus'
import { encrypt } from '@/utils/aes'
import Service from '../api/index'
import Cookies from 'js-cookie'
import {
  validCUCUsername,
  validEmail,
  validEmailCaptcha,
  validPassword,
  validPicCaptcha
} from '@/utils/validate'

interface stateType {
  verifyForm: {
    account: string;
    mode: string;
  };
  resetForm: {
    captchaemail: string;
    cucpassword: string;
    password: string;
    checkPass: string;
    captchapic: string;
  };
  imgcode: string;
}

export default defineComponent({
  name: 'ResetpwdForm',
  setup () {
    const resetRef = ref()
    const verifyRef = ref()
    const state = reactive<stateType>({
      verifyForm: {
        account: '',
        mode: ''
      },
      resetForm: {
        captchaemail: '',
        cucpassword: '',
        password: '',
        checkPass: '',
        captchapic: ''
      },
      imgcode: ''
    })
    const active = ref(0)
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
    /**
     * @description 下一步
     */
    const handleNextStep = () => {
      failure.value = true
      verifyRef.value.validate((valid: any) => {
        if (valid) {
          if ((state.verifyForm.mode === 'email' && state.verifyForm.account !== JSON.parse(sessionStorage.getItem('userinfo') as string).email) ||
          (state.verifyForm.mode === 'cuc' && state.verifyForm.account !== JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount)) {
            getNextStepFailure()
            return false
          } else {
            if (state.verifyForm.mode === 'email') {
              handleGetEmailCaptcha()
            }
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
      try {
        const { account } = state.verifyForm
        const data = {
          email: account
        }
        Service.postCaptcha(data)
          .then((res) => {
            ElMessage.success(res.message)
            return true
          })
          .catch((err) => {
            handleGetPicCaptcha()
            ElMessage.error(err.message)
          })
        return false
      } catch (err: any) {
        handleGetPicCaptcha()
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
            const { mode, account } = state.verifyForm
            const { cucpassword, password, captchaemail, captchapic } = state.resetForm
            const data = {
              account,
              mode,
              verify: mode === 'email' ? captchaemail : encrypt(cucpassword),
              password: encrypt(password),
              captcha: captchapic
            }
            Service.postResetPwd(data)
              .then((res) => {
                active.value = 2
                ElMessage.success(res.message)
              })
              .catch((err) => {
                ElMessage.error(err.message)
              })
          } catch (err:any) {
            ElMessage.error(err.message)
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
    const validateAccount = (rule: any, value: any, callback: any) => {
      if (!value || !state.verifyForm.mode) {
        callback(new Error('请选择验证账号'))
      } else if (state.verifyForm.mode === 'email' && !validEmail(value)) {
        callback(new Error('请输入正确的邮箱'))
      } else if (state.verifyForm.mode === 'cuc' && !validCUCUsername(value)) {
        callback(new Error('请输入正确的中传SSO账号'))
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
    const verifyrules = reactive<FormRules>({
      account: [{ required: true, trigger: 'blur', validator: validateAccount }],
      mode: [{ required: true, trigger: 'blur', message: '' }]
    })
    const resetrules = reactive<FormRules>({
      cucpassword: [{ required: true, trigger: 'blur', validator: validateCUCPassword }],
      captchaemail: [{ required: true, trigger: 'blur', validator: validateEmailcode }],
      password: [{ required: true, trigger: 'blur', validator: validatePassword }],
      checkPass: [{ required: true, trigger: 'blur', validator: validateRetypePassword }],
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
      handleResetPwd,
      handleGetPicCaptcha,
      active,
      handleNextStep,
      handleLastStep,
      resetValue,
      failure,
      nextstepText
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
