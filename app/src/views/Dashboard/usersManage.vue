<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:25:58
 * @FilePath: /app/src/views/Dashboard/usersManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>用户管理</h1>
          </el-header>
          <el-divider />
          <el-main>
            <el-table :data="tableData" :default-sort="sort" style="width: 100%" height="60vh" stripe :border="true"
              @sort-change="onSortChange">
              <el-table-column fixed prop="userid" label="序号" :sortable="'custom'" width="100" />
              <el-table-column label="用户名" width="100">
                <template #default="scope">
                  <el-tooltip :content="scope.row.name">
                    <el-tag>{{ scope.row.name }}</el-tag>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="邮箱" width="150">
                <template #default="scope">
                  <el-tooltip :content="scope.row.email">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <MessageBox />
                      </ElIcon>
                      {{ scope.row.email }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="中传" width="150">
                <template #default="scope">
                  <el-tooltip :content="scope.row.cucaccount ?? '该账号未与中传SSO账号绑定'">
                    <span class="flex items-center">
                      {{ scope.row.cucaccount ?? '该账号未与中传SSO账号绑定' }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="账号创建时间" width="150">
                <template #default="scope">
                  <el-tooltip :content="dayjs(scope.row.created_on).format('YYYY/MM/DD HH:mm:ss')">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <Timer />
                      </ElIcon>
                      {{ dayjs(scope.row.created_on).format('YYYY/MM/DD') }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="上次登录时间" width="150">
                <template #default="scope">
                  <el-tooltip :content="dayjs(scope.row.last_login).format('YYYY/MM/DD HH:mm:ss')">
                    <span class="flex items-center">
                      <ElIcon class="mr-3">
                        <Timer />
                      </ElIcon>
                      {{ dayjs(scope.row.last_login).format('YYYY/MM/DD') }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="上次登录IP" width="150">
                <template #default="scope">
                  <el-tooltip :content="scope.row.last_login_ip ?? '账号未曾登录'">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.last_login_ip ?? '账号未曾登录' }}</el-tag>
                    </span>
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
              <el-table-column label="角色" width="100">
                <template #default="scope">
                  <div v-for="rolename in scope.row.role" :key="rolename">
                    <el-tooltip :content="rolename">
                      <el-tag closable :disable-transitions="false" @close="handleClose(rolename,scope.row)">{{ rolename }}</el-tag>
                    </el-tooltip>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="用户简介" width="150">
                <template #default="scope">
                  <el-tooltip :content="scope.row.description ?? '该用户暂时没有填写简介'">
                    <span class="flex items-center">
                      {{ scope.row.description ?? '该用户暂时没有填写简介' }}
                    </span>
                  </el-tooltip>
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
import { MessageBox, Timer } from '@element-plus/icons-vue'
import { defineComponent, onMounted, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Sort } from 'element-plus/es/components/table/src/table/defaults'
export default defineComponent({
  name: 'UsersManage',
  components: {
    Timer,
    MessageBox
  },
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
      Service.getAllUserInfo(state.param.page, state.param.size, sort.value.order === 'descending' ? 'descending' : 'ascending').then((res) => {
        tableData.value = res.data
        total.value = res.total
      })
    }
    const handleBan = (index: number, row: any) => {
      return ElMessageBox.confirm('是否封禁用户' + row.name + '?')
        .then(() => {
          Service.banUser({ userid: row.userid }).then(
            (res) => {
              ElMessage.success(res.message)
              fetchdata()
            }
          )
        })
        .catch(() => false)
    }
    const handleDelete = (index: number, row: any) => {
      return ElMessageBox.confirm('是否删除用户' + row.name + '?')
        .then(() => {
          Service.deleteUser({ userid: row.userid }).then(
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
    const handleClose = (rolename: string, row: any) => {
      ElMessageBox.confirm('是否确认删除角色' + rolename + '?')
        .then(() => {
          row.role.splice(row.role.indexOf(rolename), 1)
          if (row.role.length === 0) {
            row.role.push('standard')
          }
          Service.updateUserInfo({
            userid: row.userid,
            role: row.role
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
