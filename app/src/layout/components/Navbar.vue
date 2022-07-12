<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:49
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-12 22:15:16
 * @FilePath: /app/src/layout/components/Navbar.vue
-->

<template>
  <div class="navbar">
    <el-header height="50px">
      <hamburger id="Hamburger" :is-active="opened" class="hamburger-container" @toggleClick="toggleSideBar" />
      <breadcrumb class="breadcrumb-container" />
      <div class="right-menu">
        <search></search>
        <div id="fullScreen" class="right-menu-box">
          <el-button class="full-screen">
            <el-tooltip content="进入全屏" effect="dark" placement="left">
              <el-icon v-show="fullScreen == false" @click="toShowFullScreen()"><full-screen /></el-icon>
            </el-tooltip>
            <el-tooltip content="退出全屏" effect="dark" placement="left">
              <el-icon v-show="fullScreen == true" @click="toExitFullScreen()"><bottom-left /></el-icon>
            </el-tooltip>
          </el-button>
        </div>
        <el-dropdown class="avatar-container" trigger="hover">
          <div class="avatar-wrapper">
            <el-avatar :src="avatar"></el-avatar>
            <div class="nickname">{{ nickname }}</div>
          </div>
          <template #dropdown>
            <el-dropdown-menu class="user-dropdown">
              <router-link to="/">
                <el-dropdown-item>首页</el-dropdown-item>
              </router-link>
              <router-link to="/personal/personalCenter">
                <el-dropdown-item>个人中心</el-dropdown-item>
              </router-link>
              <router-link to="/personal/personalSetting">
                <el-dropdown-item>个人设置</el-dropdown-item>
              </router-link>
              <el-dropdown-item divided>
                <span style="display: block" @click="logout">退出登录</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
  </div>
</template>
<script lang="ts">
import { defineComponent, computed, ref, onMounted } from 'vue'
import { FullScreen, BottomLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import Hamburger from '@/components/Hamburger/Hamburger.vue'
import Breadcrumb from '@/components/Breadcrumb/index.vue'
import Search from '@/components/Search/index.vue'
import { toFullScreen, exitFullScreen } from '@/utils/screen'
import { useStore } from '@/store/index'
import { useStorage } from 'vue3-storage'
import Service from './api'
import { ElMessage } from 'element-plus'
export default defineComponent({
  name: 'NavbarItem',
  components: {
    Hamburger,
    Breadcrumb,
    Search,
    FullScreen,
    BottomLeft
  },
  props: {
    primary: {
      default: '#fff',
      type: String
    }
  },
  setup () {
    const router = useRouter()
    const store = useStore()
    const storage = useStorage()
    const opened = computed(() => store.getters['sidebarModule/getSidebarState'])
    const fullScreen = ref(false)
    const nickname = ref(JSON.parse(sessionStorage.getItem('userinfo') as string)?.name ?? '邵佳泓')
    const avatar = ref(JSON.parse(sessionStorage.getItem('userinfo') as string)?.avatar ?? '')
    // methods
    const toggleSideBar = () => {
      store.dispatch('sidebarModule/toggleSideBar')
    }

    const toShowFullScreen = () => {
      toFullScreen()
      fullScreen.value = true
    }

    const toExitFullScreen = () => {
      exitFullScreen()
      fullScreen.value = false
    }
    const logout = () => {
      // clear()
      Service.Logout().then((res:any) => {
        storage.removeStorageSync('accessToken')
        sessionStorage.removeItem('Routes')
        sessionStorage.removeItem('userinfo')
        router.go(0)
      }).catch((err:any) => {
        ElMessage.error(err.message)
      })
    }
    onMounted(() => {
      window.addEventListener('setItem', () => {
        const userinfo: any = JSON.parse(sessionStorage.getItem('userinfo') as string)
        nickname.value = userinfo.name
        avatar.value = userinfo.avatar
      })
    })
    return {
      toShowFullScreen,
      toExitFullScreen,
      toFullScreen,
      exitFullScreen,
      fullScreen,
      nickname,
      avatar,
      toggleSideBar,
      opened,
      logout
    }
  }
})
</script>
<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.28);
  z-index: 1;

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background 0.3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .nickname {
    float: right;
    padding: 0px 25px 0px 25px;
    line-height: 40px;
    outline: none;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;
    display: flex;
    &:focus {
      outline: none;
    }
    .right-menu-box {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    .full-screen {
      background-color: transparent;
      border: none;
      padding: 5px 20px;

      i {
        background-color: transparent;
        border: none;
        color: #2c3e50;
        font-size: 28px;
      }
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;
        cursor: pointer;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
