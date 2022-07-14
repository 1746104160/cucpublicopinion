<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-08 01:18:12
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 22:02:49
 * @FilePath: /app/src/views/Task/task.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>调度管理</h1>
          </el-header>
          <el-divider />
          <el-main>
            <div class="search-container">
              <el-select v-model="clas" placeholder="请选择任务类型">
                <el-option label="测试任务" :value="1"></el-option>
                <el-option label="情感分析" :value="2"></el-option>
                <el-option label="计算热词" :value="3"></el-option>
                <el-option label="聚类分析" :value="4"></el-option>
                <el-option label="新闻分类" :value="5"></el-option>
                <el-option label="数量统计" :value="6"></el-option>
              </el-select>
            </div>
            <el-button type="success" size="large" class="ml-3" @click="creatework">
              <el-icon>
                <plus />
              </el-icon>
              创建任务
            </el-button>
          </el-main>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog v-model="visible">
      <el-progress :text-inside="true" :stroke-width="60" :percentage="percent" status="success">
        <span style="font-size:40px">{{ message }}</span>
      </el-progress>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import { defineComponent, onBeforeMount, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import Service from './api'
import { ElMessage } from 'element-plus'
export default defineComponent({
  name: 'TaskManage',
  components: {
    Plus
  },
  setup () {
    const visible = ref(false)
    const clas = ref()
    const percent = ref(0)
    const message = ref('')
    let timer: NodeJS.Timer | null = null
    const creatework = () => {
      Service.creatework(clas.value).then((res: string) => {
        const ids = res.split('/')[2]
        percent.value = 0
        message.value = ''
        visible.value = true
        createSetInterval(ids)
      })
    }
    const checkState = (ids: string) => {
      Service.checkstate(ids).then((res: any) => {
        if (res.state === 'FAILURE') {
          ElMessage.error('任务执行失败')
          percent.value = 0
          message.value = ''
          visible.value = false
          stopSetInterval()
        } else if (res.result) {
          percent.value = 100
          message.value = ''
          visible.value = false
          stopSetInterval()
        } else {
          percent.value = parseInt(res.current) / parseInt(res.total) * 100
          message.value = res.status
        }
      })
    }
    const createSetInterval = (ids: string) => {
      stopSetInterval()
      timer = setInterval(() => {
        checkState(ids)
      }, 2000)
    }
    const stopSetInterval = () => {
      if (timer) {
        clearInterval(timer)
        timer = null
      }
    }
    onBeforeMount(() => {
      stopSetInterval()
    })
    return {
      clas,
      visible,
      percent,
      message,
      creatework
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

.search-container {
  :deep(.el-input__inner) {
    border-radius: 0;
    border: 0;
    padding-left: 0;
    padding-right: 0;
    box-shadow: none !important;
    border-bottom: 1px solid #d9d9d9;
    vertical-align: middle;
  }
}
</style>
