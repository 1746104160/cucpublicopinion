<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-14 13:13:13
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-14 22:04:46
 * @FilePath: /app/src/views/Version/version.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>版本信息</h1>
          </el-header>
          <el-divider />
          <el-main>
            <el-timeline>
              <el-timeline-item v-for="data of datas" :key="data.date" center :timestamp="dayjs(data.date).format('YYYY-MM-DD')" placement="top">
                <el-card>
                  <h4>{{data.message}}</h4>
                  <p><el-icon><User /></el-icon>{{data.author}} committed <el-icon><Timer /></el-icon>{{ dayjs(data.date).format('YYYY-MM-DD HH:mm:ss')}}</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-main>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue'
import { User, Timer } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
export default defineComponent({
  name: 'VersionInfo',
  components: {
    User,
    Timer
  },
  setup () {
    const datas = ref([{
      message: 'add taskmanage',
      author: '1746104160',
      date: '2022-07-14T14:05:32Z'
    }, {
      message: 'add apk qrcode and version info',
      author: '1746104160',
      date: '2022-07-14T7:02:32Z'
    }, {
      message: 'add visualize',
      author: '1746104160',
      date: '2022-07-13T16:47:32Z'
    }, {
      message: 'fix bug',
      author: '1746104160',
      date: '2022-07-12T17:16:10Z'
    }, {
      message: 'fix bugs',
      author: '1746104160',
      date: '2022-07-12T16:32:52Z'
    }, {
      message: 'add log manage',
      author: '1746104160',
      date: '2022-07-12T06:42:15Z'
    }, {
      message: 'add news update',
      author: '1746104160',
      date: '2022-07-11T06:37:12Z'
    }, {
      message: 'add newsmanage',
      author: '1746104160',
      date: '2022-07-09T17:47:16Z'
    }, {
      message: 'update',
      author: '1746104160',
      date: '2022-07-09T15:41:14Z'
    }, {
      message: 'lint',
      author: '1746104160',
      date: '2022-07-08T05:01:52Z'
    },
    {
      message: "Merge branch 'main' of https://github.com/1746104160/cucpublicopinion into main",
      author: '1746104160',
      date: '2022-07-08T04:13:39Z'
    }, {
      message: 'lint',
      author: '1746104160',
      date: '2022-07-08T04:13:30Z'
    }, {
      message: 'lint',
      author: '1746104160',
      date: '2022-07-08T04:13:16Z'
    }, {
      message: 'Delete uwsgi.ini',
      author: '1746104160',
      date: '2022-07-08T04:12:32Z'
    }, {
      message: 'update personcenter',
      author: '1746104160',
      date: '2022-07-08T00:55:41Z'
    }, {
      message: 'update sort',
      author: '1746104160',
      date: '2022-07-08T00:33:43Z'
    }, {
      message: 'update role manage',
      author: '1746104160',
      date: '2022-07-07T18:24:52Z'
    }, {
      message: 'gitignore update',
      author: '1746104160',
      date: '2022-07-07T18:03:07Z'
    }, {
      message: 'clear pycache',
      author: '1746104160',
      date: '2022-07-07T17:40:06Z'
    }, {
      message: 'gitignore update',
      author: '1746104160',
      date: '2022-07-07T17:37:37Z'
    }, {
      message: 'update gitignore for python',
      author: '1746104160',
      date: '2022-07-07T17:36:20Z'
    }, {
      message: 'base frontend and backend',
      author: '1746104160',
      date: '2022-07-07T17:24:10Z'
    }, {
      message: 'Initial commit',
      author: '1746104160',
      date: '2022-07-07T17:14:10Z'
    }])
    return {
      datas,
      dayjs
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
</style>
