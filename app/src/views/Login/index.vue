<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 15:00:12
 * @FilePath: /app/src/views/Login/index.vue
-->

<template>
  <div class="container">
    <div class="login-container">
      <div class="login-left">
        <div class="top">
          <div class="title">
            <span>欢迎使用</span>
          </div>
          <div class="desc">
            <span>业务管理系统</span>
          </div>
        </div>
        <div class="bottom">
          <img :src="working" />
          <img :src="qrcode" />
        </div>
      </div>
      <div class="login-right">
        <h1>{{ title }}</h1>
        <LoginForm v-if="showLogin" @toReset="handleToReset" @toRegister="handleToRegister" @toSSORegister="handleToSSORegister"></LoginForm>
        <RegisterForm v-else-if="showRegister" @toLogin="handleToLogin"></RegisterForm>
        <ResetForm v-else-if="showReset" @toLogin="handleToLogin"></ResetForm>
        <SSORegisterForm v-else-if="showSSORegister" @toLogin="handleToLogin"></SSORegisterForm>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import working from '@/assets/woking.gif'
import LoginForm from './components/loginForm.vue'
import ResetForm from './components/resetForm.vue'
import RegisterForm from './components/registerForm.vue'
import SSORegisterForm from './components/ssoregisterForm.vue'
import Service from './api'
export default defineComponent({
  name: 'LoginPage',
  components: {
    LoginForm,
    ResetForm,
    RegisterForm,
    SSORegisterForm
  },
  setup () {
    const title = ref('登录')
    const showLogin = ref(true)
    const showRegister = ref(false)
    const showReset = ref(false)
    const showSSORegister = ref(false)
    const handleToReset = () => {
      showLogin.value = false
      showRegister.value = false
      showReset.value = true
      showSSORegister.value = false
      title.value = '重置密码'
    }
    const handleToLogin = () => {
      showLogin.value = true
      showRegister.value = false
      showReset.value = false
      showSSORegister.value = false
      title.value = '登录'
    }
    const handleToRegister = () => {
      showLogin.value = false
      showRegister.value = true
      showReset.value = false
      showSSORegister.value = false
      title.value = '注册'
    }
    const handleToSSORegister = () => {
      showSSORegister.value = true
      showRegister.value = false
      showReset.value = false
      showLogin.value = false
      title.value = '中传SSO账号注册'
    }
    const qrcode = ref('')
    onMounted(() => {
      Service.getQRcode().then((res:any) => {
        qrcode.value = res.data.qrcode
        console.log(res.data.qrcode)
      })
    })
    return {
      title,
      showReset,
      showRegister,
      showLogin,
      showSSORegister,
      working,
      qrcode,
      handleToRegister,
      handleToReset,
      handleToLogin,
      handleToSSORegister
    }
  }
})
</script>

<style lang="scss" scoped>
.container {
  position: relative;
  background-image: linear-gradient(90deg, #ebebeb, #f5f7f6);
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

  .login-container {
    width: 874px;
    min-width: 874px;
    height: 78%;
    min-height: 600px;
    flex-direction: row;
    display: flex;
    justify-content: space-evenly;
    border-radius: 10px;
    overflow: hidden;
    background-color: white;
    box-shadow: 0 0 20px 5px rgba(34, 84, 142, 0.26);

    .login-left {
      width: 50%;
      padding: 47px 54px;

      img {
        width: 100%;
        height: auto;
        margin: 0px 20px;
      }

      .top {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        margin: 40px 0px;

        .title {
          font-size: 32px;
          margin-bottom: 16px;
        }

        .desc {
          font-size: 28px;
          text-align: left;
          color: rgb(166, 175, 188);
        }
      }
    }

    .login-right {
      width: 70%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 30px;

      h1 {
        margin-left: 50px;
        font-size: 32px;
        margin-bottom: 16px;
      }
    }
  }
}
</style>
