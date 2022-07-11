<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-11 08:30:45
 * @FilePath: /app/src/views/Dashboard/usersManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>用户管理</h1>
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
              <el-table-column fixed prop="userid" label="序号" :sortable="'custom'" />
              <el-table-column label="用户名">
                <template #default="scope">
                  <el-tooltip :content="scope.row.description ?? '该用户暂时没有填写简介'">
                    <el-tag>{{ scope.row.name }}</el-tag>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="邮箱">
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
              <el-table-column label="中传账号">
                <template #default="scope">
                  <el-tooltip :content="scope.row.cucaccount ?? '该账号未与中传SSO账号绑定'">
                    <span class="flex items-center">
                      {{ scope.row.cucaccount ?? '该账号未与中传SSO账号绑定' }}
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="账号创建时间">
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
              <el-table-column label="上次登录时间">
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
              <el-table-column label="上次登录IP">
                <template #default="scope">
                  <el-tooltip :content="scope.row.last_login_ip ?? '账号未曾登录'">
                    <span class="flex items-center">
                      <el-tag>{{ scope.row.last_login_ip ?? '账号未曾登录' }}</el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="账号状态">
                <template #default="scope">
                  <el-tooltip :content="scope.row.valid ? '正常' : '封禁中'">
                    <span class="flex items-center">
                      <el-tag v-if="scope.row.valid" type="success">正常</el-tag>
                      <el-tag v-else type="info"><i class="ic ic-lock"></i> 封禁中 </el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="角色">
                <template #default="scope">
                  <div class="tag-dynamic">
                    <el-tag v-for="role in scope.row.role" :key="role.name" closable :disable-transitions="false"
                      @close="handleClose(role.name, scope.row)">
                      <el-tooltip :content="role.description">
                        {{ role.name }}
                      </el-tooltip>
                    </el-tag>
                    <el-button class="button-new-tag" size="small" @click="editVisible=true;currentuser=scope.row">调整用户角色</el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除用户</el-button>
                  <el-button v-if="scope.row.valid" size="small" type="danger"
                    @click="handleBan(scope.$index, scope.row)">封禁用户</el-button>
                  <el-button v-else size="small" type="success" @click="handleBan(scope.$index, scope.row)">解封用户
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
    <el-dialog v-model="editVisible" title="调整用户角色" :before-close="handleCloseDialog">
      <UsersEdit :current-user="currentuser" @success="onSuccess"/>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import {
  ElMessage,
  ElMessageBox
} from 'element-plus'
import { MessageBox, Timer } from '@element-plus/icons-vue'
import { defineComponent, onMounted, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Sort } from 'element-plus/es/components/table/src/table/defaults'
import UsersEdit from './components/usersEdit.vue'
export default defineComponent({
  name: 'UsersManage',
  components: {
    Timer,
    MessageBox,
    UsersEdit
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
      Service.getAllUserInfo(state.param.page, state.param.size, sort.value.order === 'descending' ? 'descending' : 'ascending').then((res) => {
        tableData.value = res.data.users
        total.value = res.data.total
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
          const rolenames = []
          row.role.forEach((role: { name: string }) => {
            if (role.name !== rolename) {
              rolenames.push(role.name)
            }
          })
          if (rolenames.length === 0) {
            rolenames.push('standard')
          }
          Service.updateUserInfo({
            userid: row.userid,
            role: rolenames
          }).then(
            (res) => {
              ElMessage.success(res.message)
              fetchdata()
            }
          ).catch((err:any) => {
            ElMessage.error(err.message)
          })
        })
        .catch(() => false)
    }
    const handleCloseDialog = (done: () => void) => {
      ElMessageBox.confirm('是否取消新增？')
        .then(() => {
          done()
        })
        .catch(() => {
        })
    }
    const onSuccess = () => {
      editVisible.value = false
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
      handleBan,
      onCurrentChange,
      onSizeChange,
      onSortChange,
      handleClose,
      fetchdata,
      handleCloseDialog,
      onSuccess
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
