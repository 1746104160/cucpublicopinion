<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-08 01:18:12
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-13 10:32:36
 * @FilePath: /app/src/views/Security/serviceManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>接口管理</h1>
            <div>
              <el-button type="success" size="small" class="ml-3" @click="fetchdata">
                <el-icon>
                  <refresh />
                </el-icon>
                刷新
              </el-button>
            </div>
          </el-header>
          <el-divider />
          <el-main>
            <el-table ref="tableRef" :data="tableData" style="width: 100%" height="60vh" stripe :border="true"
              :table-layout="'auto'" @selection-change="handleSelectionChange" @filter-change="handleFilterChange" >
              <el-table-column type="selection" />
              <el-table-column label="IP地址" :filters="ips">
                <template #default="scope">
                  <el-tooltip :content="scope.row.ip_addr">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.ip_addr }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="服务名">
                <template #default="scope">
                  <el-tooltip :content="scope.row.servicename">
                    <el-tag>{{ scope.row.servicename }}</el-tag>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="当日访问次数">
                <template #default="scope">
                  <el-tooltip :content="scope.row.current_visit.toString()">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.current_visit }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="当日最高访问次数">
                <template #default="scope">
                  <el-tooltip :content="scope.row.max_visit.toString()">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.max_visit }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button v-if="scope.row.current_visit < scope.row.max_visit" size="small" type="danger"
                    @click="handleBan(scope.$index, scope.row)">封禁接口</el-button>
                  <el-button v-else size="small" type="success" @click="handleunBan(scope.$index, scope.row)">解封接口
                  </el-button>
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
  ElMessage,
  ElMessageBox,
  ElTable
} from 'element-plus'
import { defineComponent, onActivated, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Refresh } from '@element-plus/icons-vue'
interface dataType {
  text: string
  value: string
}
export default defineComponent({
  name: 'RolesManage',
  components: {
    Refresh
  },
  setup () {
    const tableRef = ref<InstanceType<typeof ElTable>>()
    const multipleSelection = ref([])
    const tableData = ref([] as any[])
    const createVisible = ref(false)
    const editVisible = ref(false)
    const total = ref(0)
    const ipaddr = ref('')
    const ips = ref([] as dataType[])
    const currentrole = ref()
    const state = reactive({
      param: {
        size: 10,
        page: 1
      }
    })
    const fetchdata = () => {
      Service.getAllServiceInfo(state.param.page, state.param.size, ipaddr.value).then((res) => {
        tableData.value = res.data.security
        total.value = res.data.total
        ips.value = []
        res.data.ips.forEach((element:string) => {
          ips.value.push({
            text: element,
            value: element
          })
        })
      })
    }
    const handleBan = (index: number, row: any) => {
      if (multipleSelection.value.length === 0) {
        return ElMessageBox.confirm('是否封禁接口' + row.servicename + '?')
          .then(() => {
            Service.banService({ data: [row] }).then(
              (res) => {
                ElMessage.success(res.message)
                fetchdata()
              }
            )
          })
          .catch(() => false)
      } else {
        const names:string[] = []
        multipleSelection.value.forEach((element:any) => {
          names.push(element.servicename)
        })
        return ElMessageBox.confirm('是否封禁' + names.join(',') + '这些接口?')
          .then(() => {
            Service.banService({ data: multipleSelection.value }).then(
              (res) => {
                ElMessage.success(res.message)
                fetchdata()
              }
            )
          })
          .catch(() => false)
      }
    }
    const handleunBan = (index: number, row: any) => {
      if (multipleSelection.value.length === 0) {
        return ElMessageBox.confirm('是否解封接口' + row.servicename + '?')
          .then(() => {
            Service.unbanService({ data: [row] }).then(
              (res) => {
                ElMessage.success(res.message)
                fetchdata()
              }
            )
          })
          .catch(() => false)
      } else {
        const names:string[] = []
        multipleSelection.value.forEach((element:any) => {
          names.push(element.servicename)
        })
        return ElMessageBox.confirm('是否解封' + names.join(',') + '这些接口?')
          .then(() => {
            Service.unbanService({ data: multipleSelection.value }).then(
              (res) => {
                ElMessage.success(res.message)
                fetchdata()
              }
            )
          })
          .catch(() => false)
      }
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
      ipaddr.value = filters['el-table_1_column_2'][0] ?? ''
      fetchdata()
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
      handleBan,
      handleunBan,
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
</style>
