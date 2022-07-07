<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:43:11
 * @FilePath: /app/src/views/Personal/personalSetting.vue
-->

<template>
  <div class="PersonalSetting">
    <el-row>
      <el-col :offset="1" :span="22">
        <div class="grid-content bg-purple-dark">
          <el-card class="box-card">
            <template #header>
              <div class="card-header">
                <el-button class="button" type="info" @click="router.back()"
                  ><i class="el-icon-arrow-left" />返回</el-button
                >

                <span>个人设置</span>
                <div></div>
              </div>
            </template>
            <el-tabs tab-position="left">
              <el-tab-pane label="基本设置">
                <div class="set-title">
                  <span>基本设置</span>
                </div>
                <div class="set-info">
                  <div class="form-info">
                    <el-form
                      ref="settingFormRef"
                      :model="settingForm"
                      :rules="rules"
                      label-width="100px"
                      class="demo-ruleForm"
                    >
                      <el-form-item label="个人简介" prop="desc">
                        <el-input
                          v-model="settingForm.description"
                          type="textarea"
                          placeholder="个人简介"
                          maxlength="120"
                        ></el-input>
                      </el-form-item>

                      <el-form-item>
                        <el-button
                          type="primary"
                          :loading="updateLoading"
                          @click="submitForm()"
                          >更新基本信息</el-button
                        >
                        <el-button @click="resetForm()">重置</el-button>
                      </el-form-item>
                    </el-form>
                  </div>
                  <div class="avatar">
                    <div class="preview">
                      <span>头像</span>
                      <el-image class="avatar" :src="imageUrl" fit="fill" />
                    </div>
                    <el-upload
                      accept=".jpg, .png, .jpeg, .bmp, .JPG, .PNG, .JPEG, .BMP"
                      action=""
                      class="avatar-uploader"
                      :on-change="handleAvatarChange"
                      :before-remove="beforeRemove"
                      :auto-upload="false"
                      :file-list="picList"
                      :limit="1"
                      :on-exceed="handleAvatarExceed"
                    >
                      <template #trigger>
                        <el-button type="primary">选择头像</el-button>
                      </template>
                      <el-button
                        v-show="picList"
                        class="ml-3"
                        type="success"
                        @click="submitAvatarUpload"
                      >
                        上传
                      </el-button>
                      <template #tip>
                        <div class="el-upload__tip">只支持jpg png jpeg bmp文件的上传</div>
                      </template>
                    </el-upload>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="安全设置">
                <div class="set-title">
                  <span>安全设置</span>
                </div>
                <div class="secure-item">
                  <div class="secure-info">
                    <span class="secure-key">账户密码</span>
                    <span class="secure-value">使用SSO注册的账户推荐修改密码</span>
                  </div>
                  <div class="opera-btn">
                    <el-button class="ml-3" type="primary" @click="dialogVisible=showpwdReset=true">
                      修改
                    </el-button>
                  </div>
                </div>
                <div class="secure-item">
                  <div class="secure-info">
                    <span class="secure-key">绑定邮箱</span>
                    <span class="secure-value">已绑定邮箱: {{ email }}</span>
                  </div>
                  <div class="opera-btn">
                    <el-button class="ml-3" type="primary" @click="dialogVisible=showemailReset=true">
                      修改
                    </el-button>
                  </div>
                </div>
                <div class="secure-item">
                  <div class="secure-info">
                    <span class="secure-key">绑定中传SSO账号</span>
                    <span v-if="cuc!='该账号未与中传SSO账号绑定'" class="secure-value">已绑定学工号: {{ cuc }}</span>
                    <span v-else class="secure-value">{{ cuc }}</span>
                  </div>
                  <div class="opera-btn">
                    <el-button v-if="cuc!='该账号未与中传SSO账号绑定'" class="ml-3" type="primary" @click="dialogVisible=showssoReset=true">
                      修改
                    </el-button>
                    <el-button v-else class="ml-3" type="success" @click="dialogVisible=showssoReset=true">
                      绑定
                    </el-button>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </div></el-col
      >
    </el-row>
    <el-dialog
    v-model="dialogVisible"
    title="修改"
    width="40%"
    :before-close="handleClose"
  >
    <ResetpwdForm v-if="showpwdReset" />
    <ResetemailForm v-if="showemailReset" />
    <ResetssoForm v-if="showssoReset" />
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = showpwdReset = false;router.go(0)">关闭</el-button>
      </span>
    </template>
  </el-dialog>
  </div>
</template>
<script lang="ts">
import { ElMessage, ElMessageBox, UploadProps, UploadRawFile } from 'element-plus'
import type { FormRules } from 'element-plus'
import { defineComponent, reactive, ref, toRefs, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/store'
import Service from './api/index'
import ResetpwdForm from './components/pwdForm.vue'
import ResetemailForm from './components/emailForm.vue'
import ResetssoForm from './components/ssoForm.vue'
export default defineComponent({
  name: 'PersonalSetting',
  components: {
    ResetpwdForm,
    ResetemailForm,
    ResetssoForm
  },
  setup () {
    const router = useRouter()
    const store = useStore()
    const settingFormRef = ref()
    const noticeSwitch = reactive({
      userSwitch: false,
      sysSwitch: true
    })
    const settingForm = reactive({
      description: ''
    })
    const picList = ref()
    const imageUrl = ref(JSON.parse(sessionStorage.getItem('userinfo') as string)?.avatar ?? '')
    const updateLoading = ref(false)
    const email = ref(JSON.parse(sessionStorage.getItem('userinfo') as string).email ?? JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount + '@cuc.edu.cn')
    const cuc = ref(JSON.parse(sessionStorage.getItem('userinfo') as string).cucaccount ?? '该账号未与中传SSO账号绑定')
    onMounted(() => {
      window.addEventListener('setItem', () => {
        const userinfo: any = JSON.parse(sessionStorage.getItem('userinfo') as string)
        cuc.value = userinfo.cucaccount ?? '该账号未与中传SSO账号绑定'
        email.value = userinfo.email
        imageUrl.value = userinfo.avatar
      })
    })
    const rules = reactive<FormRules>({
      description: { required: true, message: '请输入个人简介', trigger: 'blur' }
    })
    const dialogVisible = ref(false)
    const showpwdReset = ref(false)
    const showemailReset = ref(false)
    const showssoReset = ref(false)
    // methods
    const submitForm = () => {
      settingFormRef.value.validate(async (valid: any) => {
        if (valid) {
          updateLoading.value = true
          const data = {
            ...settingForm
          }
          Service.postUpdateUserInfo(data).then(res => {
            updateLoading.value = false
            store.dispatch('userModule/getUserInfo')
            router.go(0)
            ElMessage({
              type: 'success',
              message: res.message
            })
            return true
          }).catch(err => {
            ElMessage({
              type: 'error',
              message: err
            })
            return false
          })
        }
      })
    }
    const submitAvatarUpload = () => {
      if (picList.value) {
        const PicData = new FormData()
        PicData.append('avatar', picList.value[0])
        Service.postUserAvatar(PicData)
          .then(() => {
            picList.value = []
            store.dispatch('userModule/getUserInfo')
            router.go(0)
            return true
          })
          .catch((err: any) => {
            ElMessage({
              type: 'error',
              message: err
            })
            return false
          })
      }
    }
    const resetForm = () => {
      settingFormRef.value.resetFields()
    }
    const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
      return ElMessageBox.confirm(`是否删除${uploadFile.name}?`).then(
        () => true,
        () => false
      )
    }
    const handleAvatarChange: UploadProps['onChange'] = (file, filelist) => {
      const ext = file.name.substring(file.name.lastIndexOf('.') + 1)
      const whiteList = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'bmp', 'BMP']
      if (whiteList.indexOf(ext) === -1) {
        ElMessage.closeAll()
        ElMessage.error('只支持上传 jpg,png,bmp 格式的图片!')
        filelist.pop()
      }
      picList.value = [file.raw as UploadRawFile]
    }
    const handleAvatarExceed: UploadProps['onExceed'] = (files) => {
      picList.value = [files[0] as UploadRawFile]
    }
    const handleClose = (done: () => void) => {
      ElMessageBox.confirm('是否取消修改？')
        .then(() => {
          router.go(0)
          showpwdReset.value = false
          done()
        })
        .catch(() => {
          // catch error
        })
    }
    return {
      handleAvatarExceed,
      router,
      settingFormRef,
      settingForm,
      submitForm,
      resetForm,
      handleAvatarChange,
      rules,
      imageUrl,
      ...toRefs(noticeSwitch),
      updateLoading,
      email,
      cuc,
      picList,
      submitAvatarUpload,
      beforeRemove,
      dialogVisible,
      handleClose,
      showpwdReset,
      showemailReset,
      showssoReset
    }
  }
})
</script>

<style lang="stylus" scoped>
.PersonalSetting{
    margin-top:20px;
    .demo-ruleForm{
        text-align :left;
    }
    .set-title{
      text-align :left;
    }
    .secure-item{
      width:100%;
      padding:20px;
      border-bottom:1px solid #f0f0f0;
      display :flex;
      flex-direction:row;
      justify-content :space-between;
      align-items :center;
      .secure-info{
         display :flex;
      flex-direction:column;
      justify-content :flex-start;
      align-items :flex-start;
        .secure-key{
          margin-bottom: 4px;
          color: rgba(0,0,0,.85);
          font-size: 14px;
          line-height: 1.6;
        }
        .secure-value{
          color: rgba(0,0,0,.45);
          font-size: 14px;
          line-height: 1.6;
        }
      }
      .opera-btn{
        color:#1890ff;
        cursor:pointer;

      }
    }
    .set-info{
      display :flex;
      flex-direction :row;
      justify-content :space-around;
      align-items :flex-start;
      .form-info{

      }
      .avatar{
        display :flex;
        flex-direction:row;
        justify-content:flex-start;
        align-items :flex-end;
        .preview{
           display :flex;
        flex-direction:column;
        justify-content:flex-start;
        align-items :flex-start;
        margin-right:20px;
         .avatar{
            width:174px;
          height:174px;
          border-radius:50%;
         }
        }

          .avatar-uploader .el-upload:hover {
            border-color: #409EFF;
          }
          .avatar-uploader-icon {
            font-size: 28px;
            color: #8c939d;
            width: 178px;
            height: 178px;
            line-height: 178px;
            text-align: center;
          }
          .avatar {
            width: 178px;
            height: 178px;
            display: block;
          }
      }
    }
    .info{
        text-align: left;
    padding-left: 20px;
    margin-bottom: 20px;
    font-size: 12px;
    }
     .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
  }

  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .box-card {
    width:100%;
  }
}
</style>
