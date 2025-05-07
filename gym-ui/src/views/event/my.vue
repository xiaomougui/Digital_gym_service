<template>
    <div class="my-matches">
      <el-card shadow="hover">
        <div class="header">
          <h2>我的赛事</h2>
          <el-tabs v-model="activeStatus" @tab-change="filterMatches">
            <el-tab-pane label="全部" name="all" />
            <el-tab-pane label="未开始" name="pending" />
            <el-tab-pane label="进行中" name="ongoing" />
            <el-tab-pane label="已结束" name="completed" />
          </el-tabs>
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
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{row}">
              <el-tag :type="getStatusTag(row.status)">{{ getStatusName(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button size="small" @click="viewDetail(row)">查看详情</el-button>
              <el-button 
                v-if="row.status === 'pending'" 
                size="small" 
                type="danger" 
                @click="cancelJoin(row)"
              >
                取消报名
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
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
      status: 'ongoing',
      participants_count: 22,
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
      status: 'completed',
      participants_count: 32,
      max_participants: 32,
      description: '个人单打比赛',
      rules: '单淘汰制，每局11分',
      result: {
        winner: '张三',
        score: '3-1'
      }
    }
  ]
  
  const matches = ref([...mockMatches])
  const loading = ref(false)
  const activeStatus = ref('all')
  
  const matchTypes = {
    basketball: { name: '篮球', tag: '' },
    football: { name: '足球', tag: 'success' },
    table_tennis: { name: '乒乓球', tag: 'warning' },
    badminton: { name: '羽毛球', tag: 'info' }
  }
  
  const statusTypes = {
    pending: { name: '未开始', tag: 'info' },
    ongoing: { name: '进行中', tag: 'warning' },
    completed: { name: '已结束', tag: 'success' },
    cancelled: { name: '已取消', tag: 'danger' }
  }
  
  const getMatchTypeName = (type) => matchTypes[type]?.name || type
  const getMatchTypeTag = (type) => matchTypes[type]?.tag || ''
  const getStatusName = (status) => statusTypes[status]?.name || status
  const getStatusTag = (status) => statusTypes[status]?.tag || ''
  
  const filteredMatches = computed(() => {
    if (activeStatus.value === 'all') return matches.value
    return matches.value.filter(match => match.status === activeStatus.value)
  })
  
  const viewDetail = (match) => {
    router.push(`/event/details/${match.id}`)
  }
  
  const cancelJoin = (match) => {
    loading.value = true
    setTimeout(() => {
      match.status = 'cancelled'
      ElMessage.success(`已取消报名 ${match.name}`)
      loading.value = false
    }, 500)
  }
  
  const filterMatches = () => {
    // 过滤功能已通过计算属性实现
  }
  </script>
  
  <style scoped>
  .my-matches {
    padding: 20px;
  }
  
  .header {
    margin-bottom: 20px;
  }
  </style>