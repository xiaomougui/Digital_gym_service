<template>
    <!-- <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
      <el-radio-button :value="false">expand</el-radio-button>
      <el-radio-button :value="true">collapse</el-radio-button>
    </el-radio-group> -->
  <el-menu
    :default-active="activeMenu"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    :router="true"
    unique-opened
  >
    <SideItem
      v-for="item in permissionRoutes"
      :key="item.path"
      :item="item"
    />
  </el-menu>
</template>
  
<script lang="ts" setup>
  import { ref, computed } from 'vue'
  import { storeToRefs } from 'pinia'
  import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
  } from '@element-plus/icons-vue'
  import { useAuthStore } from '@/stores/auth'
  import { useSideStore } from '@/stores/side'
  import { useRoute } from 'vue-router'
  import SideItem from './SideItem.vue'
  
  
  
  let authStore = useAuthStore();

  let sideStore = useSideStore();

  const isCollapse = computed(() => sideStore.isCollapse)

  console.log(isCollapse)

  //路由对象
  let route = useRoute();

  //路由结构数组
  let permissionRoutes = authStore.permissionRoutes;

  const activeMenu = computed(()=>route.path);



</script>
  
<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>