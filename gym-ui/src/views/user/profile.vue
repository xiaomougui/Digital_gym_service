<template>
  <div class="personal-info-container">
    <div class="left-panel">
      <h3 class="panel-title">个人信息</h3>
      <div class="avatar-container">
        <el-avatar
          size="large"
          :src="avatar"
          class="avatar-profile"
        ></el-avatar>
      </div>
      <div class="divider"></div>
      <div class="info-item">
        <el-icon class="info-icon"><User /></el-icon>
        <span class="info-label">用户名称：</span>
        <span class="info-value">{{ userForm.username }}</span>
      </div>
      <div class="info-item">
        <el-icon class="info-icon"><Phone /></el-icon>
        <span class="info-label">手机号码：</span>
        <span class="info-value">{{ userForm.phone }}</span>
      </div>
      <div class="info-item">
        <el-icon class="info-icon"><Compass /></el-icon>
        <span class="info-label">用户邮箱：</span>
        <span class="info-value">{{ userForm.email }}</span>
      </div>
      <div class="info-item">
        <el-icon class="info-icon"><Male /></el-icon>
        <span class="info-label">性别：</span>
        <span class="info-value">{{ userForm.gender }}</span>
      </div>
      <div class="info-item">
        <el-icon class="info-icon"><UserFilled /></el-icon>
        <span class="info-label">所属角色：</span>
        <span class="info-value">{{ userForm.permission_level }}</span>
      </div>
    </div>
    <div class="right-panel">
      <h3 class="panel-title">基本资料</h3>
      <el-tabs v-model="activeTab" type="card" class="custom-tabs">
        <el-tab-pane label="基本资料" name="basic">
          <el-form :model="userForm" :rules="rules" ref="formRef" label-width="120px" class="form-container">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="userForm.username" placeholder="请输入用户昵称"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="userForm.phone" placeholder="请输入手机号码"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="userForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="性别">
              <el-radio-group v-model="userForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item class="form-actions">
              <el-button type="primary" @click="submitForm">保存</el-button>
              <el-button @click="cancel">关闭</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="修改密码" name="password">
          <el-form :model="passwordForm" :rules="rules" ref="formRef" label-width="120px" class="form-container">
            <el-form-item label="旧密码" prop="old_password">
              <el-input v-model="passwordForm.old_password" placeholder="请输入旧密码" show-password></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="passwordForm.new_password" placeholder="请输入新密码" show-password></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input v-model="passwordForm.confirm_password" placeholder="请再次输入密码" show-password></el-input>
            </el-form-item>
            <el-form-item class="form-actions">
              <el-button type="primary" @click="submitPWForm">修改</el-button>
              <el-button @click="cancel">关闭</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, toRefs,computed, onMounted} from 'vue'
//   import { User, Phone, Mail, Office, Date } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import UserService from '@/api/user/index'
import type UserDetails from '@/types/userDetails'
import { useRouter } from 'vue-router'

  const router = useRouter()


const activeTab = ref('basic')
let authStore = useAuthStore();

let userService=new UserService();

let userForm = reactive<UserDetails>({
  id:authStore.user!.id,
  username: '',
  password:'',
  phone: '',
  email: '',
  gender: '男',
  permission_level:authStore.user!.permission_level,
  avatar:null,
})

//获取个人信息
userService.getUserDetails(authStore.user!.id).then((res)=>{
  console.log(res);
  Object.assign(userForm,res)
})

//头像
const avatar = computed(() => authStore.user?.avatar)



const passwordForm = reactive({
  old_password:'',
  new_password:'',
  confirm_password:'',
})

  const validatePass = (rule: any, value: any, callback: any) => {
      if (value === '') {
          callback(new Error('Please input the password again'))
      } else if (value !== passwordForm.new_password) {
          callback(new Error("两次密码不一致"))
      } else {
          callback()
      }
  }

const rules = {
  old_password: [
    { required: true, message: '旧密码不能为空', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '新密码不能为空', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, trigger: 'blur',validator: validatePass}
  ],
  
}
const formRef = ref(null)

//提交表单
const submitForm = () => {
  userService.modifyUserDetails(userForm).then(res=>{
      console.log(res)
      if(res.code===200){
          router.go(0) // 相当于 window.location.reload()
      }
      alert(res.msg);
  })
}

const submitPWForm = () =>{
  let data={
      id:authStore.user!.id,
      old_password:passwordForm.old_password,
      new_password:passwordForm.new_password,
  }
  userService.modfiyPassword(data).then(res=>{
      if(res.code===200){
          router.push('/login');
      }
      alert(res.msg)}
  );
  
}

const cancel = () => {
  ElMessage.info('操作已取消')
}
</script>

<style scoped lang="scss">
.personal-info-container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  gap: 20px;
}

.left-panel {
  flex: 0 0 300px;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
  .panel-title {
    margin-bottom: 20px;
    color: #303133;
    text-align: center;
    font-size: 18px;
    font-weight: 500;
  }
  
  .avatar-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    
    .avatar-profile {
      width: 100px;
      height: 100px;
    }
  }
  
  .divider {
    height: 1px;
    background: #ebeef5;
    margin: 20px 0;
  }
  
  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    font-size: 14px;
    
    .info-icon {
      margin-right: 10px;
      color: #909399;
    }
    
    .info-label {
      color: #909399;
      margin-right: 5px;
    }
    
    .info-value {
      color: #303133;
    }
  }
}

.right-panel {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
  .panel-title {
    margin-bottom: 20px;
    color: #303133;
    font-size: 18px;
    font-weight: 500;
  }
  
  .custom-tabs {
    :deep(.el-tabs__item) {
      height: 40px;
      line-height: 40px;
    }
  }
  
  .form-container {
    padding: 20px 10px 0 0;
    
    .form-actions {
      margin-top: 30px;
    }
  }
}

@media (max-width: 768px) {
  .personal-info-container {
    flex-direction: column;
  }
  
  .left-panel {
    flex: 1;
    width: 100%;
    margin-bottom: 20px;
  }
}
</style>