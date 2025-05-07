<template>
    <div class="match-detail">
      <el-card shadow="hover">
        <div class="header">
          <h2>{{ match.name }}</h2>
          <el-tag :type="getStatusTag(match.status)">{{ getStatusName(match.status) }}</el-tag>
        </div>
        
        <div class="match-info">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="赛事类型">{{ getMatchTypeName(match.type) }}</el-descriptions-item>
            <el-descriptions-item label="开始时间">{{ match.start_time }}</el-descriptions-item>
            <el-descriptions-item label="结束时间">{{ match.end_time }}</el-descriptions-item>
            <el-descriptions-item label="参赛人数">{{ match.participants_count }}/{{ match.max_participants }}</el-descriptions-item>
          </el-descriptions>
          
          <div class="description">
            <h3>赛事描述</h3>
            <p>{{ match.description || '暂无描述' }}</p>
          </div>
          
          <div class="rules" v-if="match.rules">
            <h3>赛事规则</h3>
            <p>{{ match.rules }}</p>
          </div>
        </div>
        
        <!-- 动态组件加载不同类型的结果组件 -->
        <component 
          :is="resultComponent" 
          v-if="resultComponent && match.status === 'completed'"
          :match-id="matchId"
        />
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useRoute } from 'vue-router'
  import { defineAsyncComponent } from 'vue'
  
  // 内置伪数据
  const mockMatches = [
    {
      id: 1,
      name: '2023校园篮球联赛',
      type: 'basketball',
      start_time: '2023-06-01 09:00:00',
      end_time: '2023-06-30 18:00:00',
      status: 'completed',
      participants_count: 24,
      max_participants: 24,
      description: '年度校园篮球盛事',
      rules: '采用FIBA最新篮球规则',
      result: {
        winner: '计算机系',
        score: '89-76'
      }
    },
    {
      id: 2,
      name: '秋季足球友谊赛',
      type: 'football',
      start_time: '2023-09-15 14:00:00',
      end_time: '2023-09-15 16:30:00',
      status: 'completed',
      participants_count: 22,
      max_participants: 22,
      description: '院系间足球友谊赛',
      rules: '11人制，上下半场各45分钟',
      result: {
        winner: '电子工程系',
        score: '3-2'
      }
    },
    {
      id: 3,
      name: '乒乓球个人挑战赛',
      type: 'tabletennis',
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
  
  const route = useRoute()
  const matchId = route.params.id
  const match = ref({})
  
  const matchTypes = {
    basketball: { name: '篮球', component: 'basketball' },
    football: { name: '足球', component: 'football' },
    table_tennis: { name: '乒乓球', component: 'tabletennis' },
    badminton: { name: '羽毛球', component: 'badminton' }
  }
  
  const statusTypes = {
    pending: { name: '未开始', tag: 'info' },
    ongoing: { name: '进行中', tag: 'warning' },
    completed: { name: '已结束', tag: 'success' },
    cancelled: { name: '已取消', tag: 'danger' }
  }
  
  const getMatchTypeName = (type) => matchTypes[type]?.name || type
  const getStatusName = (status) => statusTypes[status]?.name || status
  const getStatusTag = (status) => statusTypes[status]?.tag || ''
  
  const resultComponent = computed(() => {
    if (!match.value.type || match.value.status !== 'completed') return null
    console.log(matchTypes[match.value.type].component)
    return defineAsyncComponent(() => 
      import(`./results/${matchTypes[match.value.type].component}.vue`)
    )
  })
  
  // 从伪数据中查找匹配的赛事
  match.value = mockMatches.find(m => m.id === Number(matchId)) || {}
  </script>
  
  <style scoped>
  .match-detail {
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .description, .rules {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
  }
  
  .rules {
    margin-top: 15px;
  }
  </style>