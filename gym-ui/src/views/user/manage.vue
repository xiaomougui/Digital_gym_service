<template>
  <div class="user-management-container">
    <el-card class="table-card">
      <el-table :data="userFormList" style="width: 100%" stripe border>
        <el-table-column fixed prop="username" label="用户名" width="150" align="center" />
        <el-table-column prop="gender" label="性别" width="80" align="center" />
        <el-table-column prop="email" label="邮箱" width="200" align="center" />
        <el-table-column prop="phone" label="电话" width="150" align="center" />
        <el-table-column prop="real_name" label="真实姓名" width="120" align="center" />
        <el-table-column prop="id_card" label="身份证号" width="220" align="center" />
        <el-table-column fixed="right" label="操作" width="150" align="center">
          <template #default="scope">
            <el-button 
                type="primary" 
                size="small" 
                @click="handleClick(scope.row.id)"
                plain
                round>
                修改信息
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog 
      v-model="dialogFormVisible" 
      title="修改用户信息" 
      width="600px"
      center
      class="user-edit-dialog">
      <el-form 
        :model="userFormList[id]" 
        label-position="left"
        class="edit-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" :label-width="formLabelWidth">
              <el-input v-model="userFormList[id].username" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" :label-width="formLabelWidth">
              <el-radio-group v-model="userFormList[id].gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" :label-width="formLabelWidth">
              <el-input v-model="userFormList[id].phone" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" :label-width="formLabelWidth">
              <el-input v-model="userFormList[id].email" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="真实姓名" :label-width="formLabelWidth">
              <el-input v-model="userFormList[id].real_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证号" :label-width="formLabelWidth">
              <el-input v-model="userFormList[id].id_card" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="权限" :label-width="formLabelWidth">
          <el-select 
            v-model="userFormList[id].permission_level" 
            placeholder="选择权限等级"
            class="full-width-select">
            <el-option label="admin" value="admin" />
            <el-option label="common" value="common" />
            <el-option label="superadmin" value="superadmin" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false" size="large">取消</el-button>
          <el-button type="primary" @click="submitForm" size="large">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
    import { reactive, ref } from 'vue'
    import type UserDetails from '@/types/userDetails'
    import UserService from '@/api/user'
    import { useRouter } from 'vue-router'

    const router = useRouter()

    let id=ref(0);

    const handleClick = (clickid:number) => {
        id=ref(clickid-1);
        dialogFormVisible.value=true;
    }
  
    const dialogFormVisible = ref(false)
    const formLabelWidth = '140px';

    const user = new UserService();

    //定义用户列表
    let userFormList = reactive<Array<UserDetails>>([])

    //获取用户列表
    user.getUserList().then((res)=>{
        // 正确赋值响应式数组
      userFormList.splice(0, userFormList.length, ...res.data)
      
    })

    const submitForm=()=>{
      user.modifyUserDetails(userFormList[id.value]).then(res=>{

        router.go(0) // 相当于 window.location.reload()
        dialogFormVisible.value = false
        alert(res.msg);
      })
    }
</script>

<style scoped lang="scss">
.user-management-container {
  padding: 20px;
  background-color: #f5f7fa;
  
  .table-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    
    :deep(.el-table) {
      font-size: 14px;
      
      th {
        background-color: #f8f8f9;
        font-weight: 600;
      }
    }
  }
  
  .user-edit-dialog {
    .edit-form {
      padding: 0 20px;
      
      .el-row {
        margin-bottom: 20px;
      }
      
      .full-width-select {
        width: 100%;
      }
    }
    
    .dialog-footer {
      text-align: center;
      padding-top: 20px;
      
      .el-button {
        width: 120px;
      }
    }
  }
}
</style>