<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 01:42:00
 * @FilePath: /app/src/views/News/newsManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>新闻管理</h1>
            <el-button type="success" size="small" class="ml-3" @click="fetchdata">
              <el-icon>
                <refresh />
              </el-icon>
              刷新
            </el-button>
          </el-header>
          <el-divider />
          <el-main>
            <el-table :data="tableData" :default-sort="sort" style="width: 100%" height="60vh" stripe :border="true"
              @sort-change="onSortChange" :table-layout="'auto'">
              <el-table-column fixed prop="newsid" label="序号" :sortable="'custom'" />
              <el-table-column label="标题">
                <template #default="scope">
                  <el-tooltip :content="scope.row.title">
                    <el-tag>{{ scope.row.title }}</el-tag>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="作者">
                <template #default="scope">
                  <el-tooltip :content="scope.row.author">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <User />
                      </ElIcon>
                      {{ scope.row.author }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="发布时间">
                <template #default="scope">
                  <el-tooltip :content="dayjs(scope.row.publish_time).format('YYYY/MM/DD HH:mm:ss')">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <Timer />
                      </ElIcon>
                      {{ dayjs(scope.row.publish_time).format('YYYY/MM/DD') }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="爬取时间">
                <template #default="scope">
                  <el-tooltip :content="dayjs(scope.row.spider_time).format('YYYY/MM/DD HH:mm:ss')">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <Timer />
                      </ElIcon>
                      {{ dayjs(scope.row.spider_time).format('YYYY/MM/DD') }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="来源">
                <template #default="scope">
                  <el-tooltip :content="`<a href='${scope.row.article_url}'>${scope.row.article_url}</a>`" raw-content>
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.articleSource}}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除新闻</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination">
              <el-pagination :current-page="param.page" :page-size="param.size" layout="sizes,prev,pager,next,total"
                :page-sizes="[5, 10, 20]" :total="total" background @current-change="onCurrentChange"
                @size-change="onSizeChange">
              </el-pagination>
            </div>
          </el-main>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script lang="tsx">
import {
  ElMessage,
  ElMessageBox
} from 'element-plus'
import { User, Timer } from '@element-plus/icons-vue'
import { defineComponent, onMounted, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Sort } from 'element-plus/es/components/table/src/table/defaults'
export default defineComponent({
  name: 'UsersManage',
  components: {
    Timer,
    User
  },
  setup () {
    const tableData = ref([] as any[])
    const sort = ref<Sort>({
      prop: 'userid',
      order: 'ascending'
    })
    const total = ref(0)
    const editVisible = ref(false)
    const state = reactive({
      param: {
        size: 10,
        page: 1
      }
    })
    const currentuser = ref({})
    const fetchdata = () => {
      Service.getAllNewsInfo(state.param.page, state.param.size, sort.value.order === 'descending' ? 'descending' : 'ascending').then((res) => {
        tableData.value = res.data.news
        total.value = res.data.total
      })
    }
    const handleDelete = (index: number, row: any) => {
      return ElMessageBox.confirm('是否删除新闻' + row.title + '?')
        .then(() => {
          Service.deleteNews({ userid: row.userid }).then(
            (res) => {
              ElMessage.success(res.message)
              fetchdata()
            }
          )
        })
        .catch(() => false)
    }
    const onCurrentChange = (val: number) => {
      state.param.page = val
      fetchdata()
    }
    const onSizeChange = (val: number) => {
      state.param.size = val
      fetchdata()
    }
    const onSortChange = (order: Sort) => {
      sort.value = order
      fetchdata()
    }
    onMounted(() => {
      fetchdata()
    })
    return {
      ...toRefs(state),
      sort,
      tableData,
      dayjs,
      total,
      editVisible,
      currentuser,
      handleDelete,
      onCurrentChange,
      onSizeChange,
      onSortChange,
      fetchdata
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
