<template>
    <!-- 有子菜单的情况 -->
    <el-sub-menu
      v-if="item.children?.length"
      :index="item.path"
      popper-append-to-body
    >
      <template #title>
        <el-icon >
            <component :is="getIconComponent(item.icon!)" />
        </el-icon>
        <span>{{ item.title }}</span>
      </template>
      <SideItem
        v-for="child in item.children"
        :key="child.path"
        :item="child"
      />
    </el-sub-menu>
    
    <!-- 无子菜单的情况 -->
    <el-menu-item
      v-else
      :index="item.path"
      :route="{ path: item.path }" 
    >
      <el-icon >
        <component :is="getIconComponent(item.icon!)" />
      </el-icon>
      <template #title>{{ item.title }}</template>
    </el-menu-item>
</template>
  
<script setup lang="ts">
  import { defineProps } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import type { RoutForm } from '@/types/routform'
  import * as ElementPlusIconsVue from '@element-plus/icons-vue'
  
  const props = defineProps<{
    item: RoutForm
  }>()

    // 定义图标名称类型
    type IconName = keyof typeof ElementPlusIconsVue


  
    const authStore = useAuthStore()
    //获取图标组件
    const getIconComponent = (name:string) => {
        return ElementPlusIconsVue[name as IconName] || ElementPlusIconsVue['QuestionFilled']
    }
</script>