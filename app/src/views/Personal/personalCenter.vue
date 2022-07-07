<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:43:00
 * @FilePath: /app/src/views/Personal/personalCenter.vue
-->

<template>
  <div class="page-container">
    <div class="info">
      <el-divider content-position="left">个人中心</el-divider>
    </div>
    <el-row :gutter="20">
      <el-col :span="8" :offset="1">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <el-button class="button" type="info" @click="router.back()"
                ><i class="el-icon-arrow-left" />返回</el-button
              >
            </div>
          </template>
          <div class="account-avatar">
            <el-avatar class="avatar" :src="avatar"></el-avatar>
          </div>
          <el-descriptions :column="1" size="large" border>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon style="el-icon-user">
                    <user />
                  </el-icon>
                  用户名
                </div>
              </template>
              {{ nickname }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon style="el-icon-user">
                    <user />
                  </el-icon>
                  学工号
                </div>
              </template>
              {{ cuc }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon style="el-icon-user">
                    <user />
                  </el-icon>
                  用户组
                </div>
              </template>
              {{ roles }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon style="el-icon-user">
                    <user />
                  </el-icon>
                  简介
                </div>
              </template>
              {{ description }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon style="el-icon-user">
                    <MessageBox />
                  </el-icon>
                  邮箱
                </div>
              </template>
              {{ email }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onActivated } from 'vue'
import { User, MessageBox } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
export default defineComponent({
  name: 'PersonalCenter',
  components: {
    User,
    MessageBox
  },
  setup () {
    const router = useRouter()
    const formLabelWidth = ref(100)
    const showDesc = ref(true)
    const roles = ref(JSON.parse(sessionStorage.getItem('userinfo') as string).role)
    const nickname = ref(
      JSON.parse(sessionStorage.getItem('userinfo') as string).name ?? '邵佳泓'
    )
    const description = ref(
      JSON.parse(sessionStorage.getItem('userinfo') as string).description ??
        '这个人没有填写简介'
    )
    const cuc = ref(
      JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount ??
        '该账号未与中传SSO账号绑定'
    )
    const email = ref(
      JSON.parse(sessionStorage.getItem('userinfo') as string).email ??
        JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount + '@cuc.edu.cn'
    )
    const avatar = ref(
      JSON.parse(sessionStorage.getItem('userinfo') as string)?.avatar ?? ''
    )
    const docs = ref()
    onActivated(() => {
      window.addEventListener('setItem', () => {
        const userinfo: any = JSON.parse(sessionStorage.getItem('userinfo') as string)
        roles.value = userinfo.role
        nickname.value = userinfo.name
        description.value = userinfo.description ?? '这个人没有填写简介'
        cuc.value = userinfo.cucaccount ?? '该账号未与中传SSO账号绑定'
        email.value = userinfo.email
        avatar.value = userinfo.avatar
      })
    })
    return {
      router,
      formLabelWidth,
      roles,
      showDesc,
      nickname,
      description,
      cuc,
      email,
      avatar,
      docs
    }
  }
})
</script>
<style lang="stylus" scoped>
.page-container{
      .info{
        text-align: left;
    padding-left: 20px;
    margin-bottom: 20px;
    font-size: 12px;
    }
}
.box-card{
  p{
    text-align :right;
  }
  .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
  }
  margin-top:14px;
  .account-avatar{
    text-align: center;
    margin-bottom :24px;
    .avatar{
      width:105px;
      height:105px;
      margin-bottom :20px;
      border-radius:50%;
    }
  }
}
</style>
