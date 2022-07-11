<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>导入新闻</h1>
          </el-header>
          <el-divider />
          <el-main>
            <el-form ref="formRef" :model="form" :rules="rules" label-position="right" label-width="100px">
              <el-form-item label="标题" prop="title">
                <el-input v-model="form.title" placeholder="请输入新闻标题"></el-input>
              </el-form-item>
              <el-form-item label="作者" prop="author">
                <el-input v-model="form.author" placeholder="请输入新闻作者"></el-input>
              </el-form-item>
              <el-form-item label="内容" prop="content">
                <el-input :rows="5" type="textarea" v-model="form.content" placeholder="请输入新闻内容"></el-input>
              </el-form-item>
              <el-form-item label="发布时间" prop="publish_time">
                <el-date-picker v-model="form.publish_time" type="date" placeholder="请选择新闻发布时间" />
              </el-form-item>
              <el-form-item label="爬取时间" prop="spider_time">
                <el-date-picker v-model="form.spider_time" type="date" placeholder="请选择新闻爬起时间" />
              </el-form-item>
              <el-form-item label="来源" prop="article_url">
                <el-input v-model="form.article_url" autocomplete="off" placeholder="请输入新闻来源地址">
                  <template #prepend>
                    <el-form-item prop="articleSource">
                      <el-select v-model="form.articleSource" style="width: 150px" placeholder="请选择新闻来源" filterable
    allow-create default-first-option>
                        <el-option label="央视网" value="央视网"></el-option>
                        <el-option label="新华网" value="新华网"></el-option>
                        <el-option label="人民网" value="人民网"></el-option>
                        <el-option label="光明日报" value="光明日报"></el-option>
                        <el-option label="经济日报" value="经济日报"></el-option>
                        <el-option label="新浪" value="新浪"></el-option>
                        <el-option label="搜狐" value="搜狐"></el-option>
                      </el-select>
                    </el-form-item>
                  </template>
                </el-input>
              </el-form-item>
              <el-row :gutter="20">
                <el-col :span="4" :offset="10">
                  <el-button size="small" type="primary" @click="submitForm">更新编辑</el-button>
                </el-col>
              </el-row>
            </el-form>
          </el-main>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script lang="ts">
import { ElMessage, FormRules } from 'element-plus'
import { defineComponent, toRefs, reactive, ref, onMounted } from 'vue'
import { validURL } from '@/utils/validate'
import Service from './api'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from '@/store'
export default defineComponent({
  name: 'NewsUpdate',
  setup () {
    const route = useRoute()
    const router = useRouter()
    const store = useStore()
    const state = reactive({
      form: {
        newsid: 0,
        title: '',
        content: '',
        publish_time: '',
        spider_time: '',
        author: '',
        articleSource: '',
        article_url: ''
      }
    })
    const validateURL = (rule: any, value: any, callback: any) => {
      if (!value) {
        callback(new Error('请输入新闻来源地址'))
      } else if (!validURL(value)) {
        callback(new Error('不是正确的url'))
      } else {
        callback()
      }
    }
    const formRef = ref()
    const rules = reactive<FormRules>({
      title: [{ required: true, trigger: 'blur', message: '请输入文章标题' }],
      content: [{ required: true, trigger: 'blur', message: '请输入文章内容' }],
      publish_time: [{ required: true, trigger: 'blur', message: '请选择文章发布时间' }],
      spider_time: [{ required: true, trigger: 'blur', message: '请选择文章爬取时间' }],
      author: [{ required: true, trigger: 'blur', message: '请输入文章作者' }],
      articleSource: [{ required: true, trigger: 'blur', message: '请选择文章来源' }],
      article_url: [{ required: true, trigger: 'blur', validator: validateURL }]
    })
    const submitForm = () => {
      formRef.value.validate((valid: any): boolean => {
        if (valid) {
          Service.updateNewsInfo(state.form).then((res: any) => {
            state.form = {
              newsid: 0,
              title: '',
              content: '',
              publish_time: '',
              spider_time: '',
              author: '',
              articleSource: '',
              article_url: ''
            }
            ElMessage.success(res.message)
            store.commit('tabModule/DELETE_TAB', '/news/newsupdate')
            router.push({ path: store.getters['tabModule/getCurrentIndex'] })
            return true
          }).catch((err: any) => {
            ElMessage.error(err.message)
            return false
          })
        }
        return false
      })
    }
    onMounted(() => {
      state.form.newsid = parseInt(route.params.newsid as string)
      state.form.title = route.params.title as string
      state.form.author = route.params.author as string
      state.form.publish_time = route.params.publish_time as string
      state.form.spider_time = route.params.spider_time as string
      state.form.articleSource = route.params.articleSource as string
      state.form.article_url = route.params.article_url as string
      Service.getNewsContent(state.form.newsid).then((res:any) => {
        state.form.content = res.data.content
      }).catch(() => {
        store.commit('tabModule/DELETE_TAB', '/news/newsupdate')
        router.push({ path: store.getters['tabModule/getCurrentIndex'] })
      })
    })
    return {
      ...toRefs(state),
      formRef,
      rules,
      submitForm
    }
  }
})
</script>
<style lang="scss" scoped>
.page-container {
  .box-card {
    p {
      text-align: right;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
    }

    margin-top: 14px;
  }
}

.tag-dynamic {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  flex-wrap: wrap;
  width: 100%;
  margin: 10px 0px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.el-tag+.el-tag {
  margin-left: 10px;
}
</style>
