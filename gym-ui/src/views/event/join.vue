<template>
    <div class="join-match">
      <el-card shadow="hover">
        <div class="header">
          <h2>可参加赛事</h2>
          <el-input
            v-model="searchQuery"
            placeholder="搜索赛事..."
            style="width: 300px"
            clearable
            @clear="filterMatches"
            @keyup.enter="filterMatches"
          >
            <template #append>
              <el-button @click="filterMatches">
                <el-icon><search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
        
        <el-table :data="filteredMatches" style="width: 100%" v-loading="loading">
          <el-table-column prop="name" label="赛事名称" width="200" />
          <el-table-column prop="type" label="赛事类型" width="120">
            <template #default="{row}">
              <el-tag :type="getMatchTypeTag(row.type)">{{ getMatchTypeName(row.type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_time" label="开始时间" width="180" />
          <el-table-column prop="end_time" label="结束时间" width="180" />
          <el-table-column prop="participants_count" label="已报名人数" width="120" />
          <el-table-column prop="max_participants" label="人数上限" width="120" />
          <el-table-column label="操作" width="150">
            <template #default="{row}">
              <el-button 
                type="primary" 
                size="small" 
                @click="joinMatch(row)"
                :disabled="row.participants_count >= row.max_participants"
              >
                报名
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { Search } from '@element-plus/icons-vue'
  
  // 内置伪数据
  const mockMatches = [
    {
      id: 1,
      name: '2023校园篮球联赛',
      type: 'basketball',
      start_time: '2023-06-01 09:00:00',
      end_time: '2023-06-30 18:00:00',
      status: 'pending',
      participants_count: 20,
      max_participants: 24,
      description: '年度校园篮球盛事',
      rules: '采用FIBA最新篮球规则'
    },
    {
      id: 2,
      name: '秋季足球友谊赛',
      type: 'football',
      start_time: '2023-09-15 14:00:00',
      end_time: '2023-09-15 16:30:00',
      status: 'pending',
      participants_count: 18,
      max_participants: 22,
      description: '院系间足球友谊赛',
      rules: '11人制，上下半场各45分钟'
    },
    {
      id: 3,
      name: '乒乓球个人挑战赛',
      type: 'table_tennis',
      start_time: '2023-10-10 10:00:00',
      end_time: '2023-10-12 18:00:00',
      status: 'pending',
      participants_count: 28,
      max_participants: 32,
      description: '个人单打比赛',
      rules: '单淘汰制，每局11分'
    }
  ]
  
  const matches = ref([...mockMatches])
  const loading = ref(false)
  const searchQuery = ref('')
  
  const matchTypes = {
    basketball: { name: '篮球', tag: '' },
    football: { name: '足球', tag: 'success' },
    table_tennis: { name: '乒乓球', tag: 'warning' },
    badminton: { name: '羽毛球', tag: 'info' }
  }
  
  const getMatchTypeName = (type) => matchTypes[type]?.name || type
  const getMatchTypeTag = (type) => matchTypes[type]?.tag || ''
  
  const filteredMatches = computed(() => {
    return matches.value.filter(match => 
      match.name.includes(searchQuery.value) && 
      match.status === 'pending'
    )
  })
  
  const joinMatch = (match) => {
    loading.value = true
    setTimeout(() => {
      match.participants_count++
      ElMessage.success(`成功报名 ${match.name}`)
      loading.value = false
    }, 500)
  }
  
  const filterMatches = () => {
    // 搜索功能已通过计算属性实现
  }
  </script>
  
  <style scoped>
  .join-match {
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  </style>