<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-08 01:18:12
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-11 22:40:18
 * @FilePath: /app/src/views/Dashboard/rolesManage.vue
-->
<template>
  <div class="page-container">
    <el-row>
      <el-col :offset="1" :span="22">
        <el-card class="box-card">
          <el-header class="card-header">
            <h1>角色管理</h1>
            <div>
              <el-button type="primary" size="small" class="ml-3" @click="createVisible = true">
                <el-icon>
                  <plus />
                </el-icon>
                新增
              </el-button>
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
            <el-table :data="tableData" :default-sort="sort" style="width: 100%" height="60vh" stripe :border="true"
              @sort-change="onSortChange" :table-layout="'auto'">
              <el-table-column fixed prop="roleid" label="序号" :sortable="'custom'" />
              <el-table-column label="角色名">
                <template #default="scope">
                  <el-tooltip :content="scope.row.description">
                    <el-tag>{{ scope.row.name }}</el-tag>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="角色状态">
                <template #default="scope">
                  <el-tooltip :content="scope.row.valid ? '正常' : '封禁中'">
                    <span class="flex items-center">
                      <el-tag v-if="scope.row.valid" type="success">正常</el-tag>
                      <el-tag v-else type="info"><i class="ic ic-lock"></i> 封禁中 </el-tag>
                    </span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column label="路由">
                <template #default="scope">
                  <div class="tag-dynamic">
                    <el-tag v-for="route in scope.row.routes" :key="route" closable :disable-transitions="false"
                      @close="handleClose(route, scope.row)">
                      <el-tooltip :content="route">
                        {{ route }}
                      </el-tooltip>
                    </el-tag>
                    <el-button class="button-new-tag" size="small" @click="editVisible=true;currentrole=scope.row">调整角色路由</el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">删除角色</el-button>
                  <el-button v-if="scope.row.valid" size="small" type="danger"
                    @click="handleBan(scope.$index, scope.row)">封禁角色</el-button>
                  <el-button v-else size="small" type="success" @click="handleBan(scope.$index, scope.row)">解封角色
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
    <el-dialog v-model="createVisible" title="新增角色" :before-close="handleCloseDialog">
      <RolesNew @success="onSuccess"/>
    </el-dialog>
    <el-dialog v-model="editVisible" title="调整角色路由" :before-close="handleCloseDialog">
      <RolesEdit :current-role="currentrole" @success="onSuccess"/>
    </el-dialog>
  </div>
</template>
<script lang="ts">
import {
  ElMessage,
  ElMessageBox
} from 'element-plus'
import { defineComponent, onActivated, reactive, ref, toRefs } from 'vue'
import dayjs from 'dayjs'
import Service from './api'
import { Sort } from 'element-plus/es/components/table/src/table/defaults'
import RolesEdit from './components/rolesEdit.vue'
import RolesNew from './components/rolesNew.vue'
import { Plus, Refresh } from '@element-plus/icons-vue'
export default defineComponent({
  name: 'RolesManage',
  components: {
    RolesEdit,
    RolesNew,
    Plus,
    Refresh
  },
  setup () {
    const tableData = ref([] as any[])
    const sort = ref<Sort>({
      prop: 'roleid',
      order: 'ascending'
    })
    const createVisible = ref(false)
    const editVisible = ref(false)
    const total = ref(0)
    const currentrole = ref()
    const state = reactive({
      param: {
        size: 10,
        page: 1
      }
    })
    const fetchdata = () => {
      Service.getAllRoleInfo(state.param.page, state.param.size, sort.value.order === 'descending' ? 'descending' : 'ascending').then((res) => {
        tableData.value = res.data.roles
        total.value = res.data.total
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
          row.routes.splice(row.routes.indexOf(route), 1)
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
      createVisible.value = editVisible.value = false
      fetchdata()
    }
    onActivated(() => {
      fetchdata()
    })
    return {
      ...toRefs(state),
      sort,
      tableData,
      dayjs,
      total,
      createVisible,
      editVisible,
      currentrole,
      handleDelete,
      handleBan,
      onCurrentChange,
      onSizeChange,
      onSortChange,
      handleClose,
      handleCloseDialog,
      fetchdata,
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
