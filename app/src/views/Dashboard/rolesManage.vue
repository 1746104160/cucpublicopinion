<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-08 01:18:12
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 02:20:09
 * @FilePath: /app/src/views/Dashboard/rolesManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>角色管理</h1>
          </el-header>
          <el-divider />
          <el-main>
            <el-table :data="tableData" :default-sort="sort" style="width: 100%" height="60vh" stripe :border="true"
              @sort-change="onSortChange">
              <el-table-column fixed prop="roleid" label="序号" :sortable="'custom'" width="100" />
              <el-table-column label="角色名" width="100">
                <template #default="scope">
                  <el-tooltip :content="scope.row.name">
                    <el-tag>{{ scope.row.name }}</el-tag>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="账号状态" width="100">
                <template #default="scope">
                  <el-tooltip :content="scope.row.valid ? '正常' : '封禁中'">
                    <span class="flex items-center">
                      <el-tag v-if="scope.row.valid" type="success">正常</el-tag>
                      <el-tag v-else type="info"><i class="ic ic-lock"></i> 封禁中 </el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="角色简介" width="150">
                <template #default="scope">
                  <el-tooltip :content="scope.row.description ?? '该用户暂时没有填写简介'">
                    <span class="flex items-center">
                      {{ scope.row.description ?? '该用户暂时没有填写简介' }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="路由" width="100">
                <template #default="scope">
                  <div v-for="route in scope.row.routes" :key="route">
                    <el-tooltip :content="route">
                      <el-tag closable :disable-transitions="false" @close="handleClose(route,scope.row)">{{ route }}</el-tag>
                    </el-tooltip>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="350">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除用户</el-button>
                  <el-button v-if="scope.row.valid" size="small" type="danger" @click="handleBan(scope.$index, scope.row)">封禁用户</el-button>
                  <el-button v-else size="small" type="success" @click="handleBan(scope.$index, scope.row)">解封用户</el-button>
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
import { defineComponent, onMounted, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Sort } from 'element-plus/es/components/table/src/table/defaults'
export default defineComponent({
  name: 'UsersManage',
  setup () {
    const tableData = ref([] as any[])
    const sort = ref<Sort>({
      prop: 'userid',
      order: 'ascending'
    })
    const total = ref(0)
    const state = reactive({
      param: {
        size: 10,
        page: 1
      }
    })
    const fetchdata = () => {
      Service.getAllRoleInfo(state.param.page, state.param.size, sort.value.order === 'descending' ? 'descending' : 'ascending').then((res) => {
        tableData.value = res.data
        total.value = res.total
      })
    }
    const handleBan = (index: number, row: any) => {
      return ElMessageBox.confirm('是否封禁角色' + row.name + '?')
        .then(() => {
          Service.banRole({ roleid: row.roleid }).then(
            (res) => {
              ElMessage.success(res.message)
              fetchdata()
            }
          )
        })
        .catch(() => false)
    }
    const handleDelete = (index: number, row: any) => {
      return ElMessageBox.confirm('是否删除角色' + row.name + '?')
        .then(() => {
          Service.deleteRole({ roleid: row.roleid }).then(
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
    const handleClose = (route: string, row: any) => {
      ElMessageBox.confirm('是否确认删除路由' + route + '?')
        .then(() => {
          row.routes.splice(row.routesindexOf(route), 1)
          if (row.routes.length === 0) {
            row.routes.push('/personal')
          }
          Service.updateRoleInfo({
            roleid: row.roleid,
            routes: row.routes
          }).then(
            (res) => {
              ElMessage.success(res.message)
              fetchdata()
            }
          )
        })
        .catch(() => false)
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
      handleDelete,
      handleBan,
      onCurrentChange,
      onSizeChange,
      onSortChange,
      handleClose
    }
  }
})
</script>
