<template>
    <div class="match-results">
      <el-card shadow="hover">
        <div class="header">
          <h2>赛事结果</h2>
          <div class="filters">
            <el-select v-model="filterType" placeholder="全部类型" clearable @change="filterMatches">
              <el-option
                v-for="type in matchTypes"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="filterMatches"
            />
          </div>
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
          <el-table-column label="比赛结果" width="200">
            <template #default="{row}">
              <div v-if="row.result">
                {{ row.result.winner }} 胜 ({{ row.result.score }})
              </div>
              <div v-else>暂无结果</div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="{row}">
              <el-button size="small" @click="viewDetail(row)">查看详情</el-button>
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
  const filterType = ref('')
  const dateRange = ref([])
  
  const matchTypes = [
    { value: 'basketball', label: '篮球' },
    { value: 'football', label: '足球' },
    { value: 'table_tennis', label: '乒乓球' },
    { value: 'badminton', label: '羽毛球' }
  ]
  
  const getMatchTypeName = (type) => {
    const found = matchTypes.find(t => t.value === type)
    return found ? found.label : type
  }
  
  const getMatchTypeTag = (type) => {
    switch(type) {
      case 'basketball': return ''
      case 'football': return 'success'
      case 'table_tennis': return 'warning'
      case 'badminton': return 'info'
      default: return ''
    }
  }
  
  const filteredMatches = computed(() => {
    return matches.value
      .filter(match => 
        match.status === 'completed' &&
        (filterType.value ? match.type === filterType.value : true) &&
        (dateRange.value?.length === 2 ? 
          new Date(match.start_time) >= new Date(dateRange.value[0]) &&
          new Date(match.end_time) <= new Date(dateRange.value[1]) : 
          true)
      )
      .map(match => ({
        ...match,
        result: match.result || {
          winner: '未知',
          score: '0-0'
        }
      }))
  })
  
  const viewDetail = (match) => {
    router.push(`/main/event/details/${match.id}`)
  }
  
  const filterMatches = () => {
    // 过滤功能已通过计算属性实现
  }
  </script>
  
  <style scoped>
  .match-results {
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .filters {
    display: flex;
    gap: 15px;
  }
  </style>