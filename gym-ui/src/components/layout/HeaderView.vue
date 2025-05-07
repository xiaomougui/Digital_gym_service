<template>
    <div class="headerview">
        <div class="svgdrag" @click="switchButton">
            <svg t="1745742749444" class="icondrag" viewBox="0 0 1024 1024" version="1.1"  p-id="4976" width="64" height="64">
                <path data-v-49e15297="" d="M408 442h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8zm-8 204c0 4.4 3.6 8 8 8h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56zm504-486H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zm0 632H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zM142.4 642.1L298.7 519a8.84 8.84 0 0 0 0-13.9L142.4 381.9c-5.8-4.6-14.4-.5-14.4 6.9v246.3a8.9 8.9 0 0 0 14.4 7z"></path>
            </svg>
        </div>
        
        <el-breadcrumb :separator-icon="ArrowRight">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        </el-breadcrumb>
        
        <el-dropdown class="box-ava">
            <span class="el-dropdown-link">
                <el-avatar :src="avatar" class='avatar'/>
                <el-icon class="el-icon--right">
                    <arrow-down />
                </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logOut">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
        </el-dropdown>
    </div>
</template>


<script setup lang="ts">
import { computed } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue' //面包屑
import { ArrowDown } from '@element-plus/icons-vue' //下拉框
import { useAuthStore } from '@/stores/auth'
import { useSideStore } from '@/stores/side'
import { useRouter } from 'vue-router'

let authStore = useAuthStore();

const router=useRouter();

//头像
const avatar = computed(() => authStore.user?.avatar)

let sideStore = useSideStore();

function switchButton(){
    sideStore.handleSwitch()
    console.log(sideStore.isCollapse)
}

function logOut(){
    //返回登录页
    router.push('/login');
    //清除数据
    authStore.logout();
}

</script>

<style lang="css" scoped>
.headerview{
    width: 100%;
    display: flex;
    height: 60px;
    align-items: center;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
}
.svgdrag{
    position: relative;
    width: 60px;
    height: 60px;
    transition: all 0.5s;
}

.icondrag{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
    width: 20px;
    height: 20px;
}
.svgdrag:hover{
    background-color: rgba(0, 0, 0, 0.1);
}
.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}

.box-ava{
    width:100px;
    display:flex;
    position:absolute;
    justify-content:center;
    align-items:center;
    right:30px
}
</style>