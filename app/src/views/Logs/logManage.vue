<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-08 01:18:12
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-12 14:35:36
 * @FilePath: /app/src/views/Logs/logManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>日志管理</h1>
            <div>
              <el-button type="success" size="small" class="ml-3" @click="fetchdata">
                <el-icon>
                  <refresh />
                </el-icon>
                刷新
              </el-button>
            </div>
            <div class="search-container">
            </div>
          </el-header>
          <el-date-picker v-model="date" type="date" placeholder="请选择新闻发布时间" :disabled-date="disabledDate"
            :shortcuts="shortcuts" @change="fetchdata" />
          <el-divider />
          <el-main>
            <el-table ref="tableRef" :data="tableData" style="width: 100%" height="60vh" stripe :border="true"
              :table-layout="'auto'" @selection-change="handleSelectionChange" @filter-change="handleFilterChange">
              <el-table-column label="请求IP地址" :filters="ips">
                <template #default="scope">
                  <el-tooltip :content="scope.row.remote_addr">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.remote_addr }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="访问时间" width="200">
                <template #default="scope">
                  <el-tooltip :content="dayjs(scope.row.visit_time).format('YYYY/MM/DD HH:mm:ss')">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <Timer />
                      </ElIcon>
                      {{ dayjs(scope.row.visit_time).format('HH:mm:ss') }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="请求方式">
                <template #default="scope">
                  <el-tooltip
                    :content="scope.row.request_method + ' ' + scope.row.request_path + ' ' + scope.row.request_protocal">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.request_method }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="请求路径">
                <template #default="scope">
                  <el-tooltip
                    :content="scope.row.request_method + ' ' + scope.row.request_path + ' ' + scope.row.request_protocal">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.request_path }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="返回状态码">
                <template #default="scope">
                  <el-tooltip :content="scope.row.status.toString()">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.status }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="请求来源">
                <template #default="scope">
                  <el-tooltip :content="scope.row.http_referer">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.http_referer }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="用户代理">
                <template #default="scope">
                  <el-tooltip :content="scope.row.http_user_agent">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.http_user_agent }}</el-tag>
                    </span>
                  </el-tooltip>
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
<script lang="ts">
import {
  ElTable
} from 'element-plus'
import { defineComponent, onActivated, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Refresh, Timer } from '@element-plus/icons-vue'
interface dataType {
  text: string
  value: string
}
export default defineComponent({
  name: 'RolesManage',
  components: {
    Refresh,
    Timer
  },
  setup () {
    const tableRef = ref<InstanceType<typeof ElTable>>()
    const multipleSelection = ref([])
    const tableData = ref([] as any[])
    const createVisible = ref(false)
    const editVisible = ref(false)
    const total = ref(0)
    const ipaddr = ref('')
    const date = ref('2022-07-12')
    const ips = ref([] as dataType[])
    const currentrole = ref()
    const state = reactive({
      param: {
        size: 10,
        page: 1
      }
    })
    const fetchdata = () => {
      Service.getAllLogInfo(state.param.page, state.param.size, ipaddr.value, dayjs(date.value).format('YYYY-MM-DD')).then((res) => {
        tableData.value = res.data.logs
        total.value = res.data.total
        ips.value = []
        res.data.ips.forEach((element: string) => {
          ips.value.push({
            text: element,
            value: element
          })
        })
      })
    }
    const onCurrentChange = (val: number) => {
      state.param.page = val
      fetchdata()
    }
    const onSizeChange = (val: number) => {
      state.param.size = val
      fetchdata()
    }
    const handleSelectionChange = (val: any) => {
      multipleSelection.value = val
    }
    const handleFilterChange = (filters: any) => {
      ipaddr.value = filters['el-table_1_column_1'][0] ?? ''
      fetchdata()
    }
    const shortcuts = [
      {
        text: '今天',
        value: new Date()
      },
      {
        text: '昨天',
        value: () => {
          const date = new Date()
          date.setTime(date.getTime() - 3600 * 1000 * 24)
          return date
        }
      },
      {
        text: '最早',
        value: () => {
          const date = new Date()
          date.setTime(date.getTime() - 3600 * 1000 * 24 * 6)
          return date
        }
      }
    ]

    const disabledDate = (time: Date) => {
      return time.getTime() > Date.now() || time.getTime() < Date.now() - 3600 * 1000 * 24 * 7
    }
    onActivated(() => {
      fetchdata()
    })
    return {
      ...toRefs(state),
      tableData,
      tableRef,
      dayjs,
      total,
      createVisible,
      editVisible,
      currentrole,
      ips,
      date,
      shortcuts,
      disabledDate,
      onCurrentChange,
      onSizeChange,
      fetchdata,
      handleSelectionChange,
      handleFilterChange
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
