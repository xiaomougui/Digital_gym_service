<template>
  <div class="equipment-rental-stats">
    <el-card shadow="hover">
      <!-- 头部标题和日期筛选 -->
      <div class="header">
        <h2>设备租赁统计分析</h2>
        <div class="header-controls">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 360px"
            @change="fetchData"
          />
          <el-button-group class="time-toggle">
            <el-button 
              size="small" 
              :type="timeUnit === 'day' ? 'primary' : ''"
              @click="changeTimeUnit('day')"
            >
              按天
            </el-button>
            <el-button 
              size="small" 
              :type="timeUnit === 'month' ? 'primary' : ''"
              @click="changeTimeUnit('month')"
            >
              按月
            </el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <StatCard 
            title="总租赁次数" 
            :value="stats.totalRentals" 
            icon="el-icon-s-order"
            color="#409EFF"
          />
        </el-col>
        <el-col :span="6">
          <StatCard 
            title="活跃用户" 
            :value="stats.activeUsers" 
            icon="el-icon-user"
            color="#67C23A"
          />
        </el-col>
        <el-col :span="6">
          <StatCard 
            title="设备利用率" 
            :value="`${stats.utilizationRate}%`" 
            icon="el-icon-data-line"
            color="#E6A23C"
          />
        </el-col>
        <el-col :span="6">
          <StatCard 
            title="最受欢迎设备" 
            :value="stats.popularEquipment" 
            icon="el-icon-star-on"
            color="#F56C6C"
          />
        </el-col>
      </el-row>

      <!-- 图表区域 - 使用v-if实现懒加载 -->
      <el-tabs v-model="activeTab" class="chart-tabs">
        <el-tab-pane label="设备租赁趋势" name="trend">
          <div v-if="activeTab === 'trend'" ref="trendChart" class="chart-container"></div>
          <div v-else class="chart-placeholder"></div>
        </el-tab-pane>
        <el-tab-pane label="器材租赁分布" name="equipment">
          <div v-if="activeTab === 'equipment'" ref="equipmentChart" class="chart-container"></div>
          <div v-else class="chart-placeholder"></div>
        </el-tab-pane>
      </el-tabs>

      <!-- 数据表格 -->
      <el-table 
        :data="paginatedData" 
        stripe 
        border 
        v-loading="loading"
        class="data-table"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user_name" label="用户" width="120" />
        <el-table-column prop="equipment_name" label="设备名称" width="150" />
        <el-table-column prop="type" label="设备类型" width="120" />
        <el-table-column label="租赁日期" width="220">
          <template #default="{row}">
            {{ formatDate(row.rental_date) }} 至 {{ formatDate(row.expected_return_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="rental_quantity" label="数量" width="80" align="center" />
        <el-table-column label="状态" width="120" align="center">
          <template #default="{row}">
            <el-tag :type="getStatusTagType(row.rental_status)">
              {{ row.rental_status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.current"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import EquipmentService from '@/api/equipment/index'

// 统计卡片子组件
const StatCard = {
  props: ['title', 'value', 'icon', 'color'],
  template: `
    <div class="stat-card">
      <div class="stat-icon" :style="{backgroundColor: color + '20', color: color}">
        <i :class="icon"></i>
      </div>
      <div class="stat-content">
        <div class="stat-title">{{ title }}</div>
        <div class="stat-value" :style="{color: color}">{{ value }}</div>
      </div>
    </div>
  `
}

// 数据状态
const dateRange = ref([])
const activeTab = ref('trend')
const loading = ref(false)
const rawData = ref([])
const timeUnit = ref('day') // 'day' or 'month'

// 图表DOM引用
const trendChart = ref(null)
const equipmentChart = ref(null)

// 图表实例
let trendChartInstance = null
let equipmentChartInstance = null

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 统计信息
const stats = reactive({
  totalRentals: 0,
  activeUsers: 0,
  utilizationRate: 0,
  popularEquipment: '--'
})

// 获取状态标签类型
const getStatusTagType = (status) => {
  switch(status) {
    case '租借中': return 'primary'
    case '已归还': return 'success'
    case '已取消': return 'info'
    case '逾期未还': return 'danger'
    default: return 'primary'
  }
}

// 检查是否逾期
const isOverdue = (item) => {
  if (item.rental_status !== '租借中') return false
  const now = new Date()
  const returnDate = new Date(item.expected_return_date)
  return now > returnDate
}

// 分页数据
const paginatedData = computed(() => {
  const start = (pagination.current - 1) * pagination.size
  const end = start + pagination.size
  return rawData.value.slice(start, end)
})

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '--'
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// 初始化图表
const initChart = (chartRef, chartInstance, type) => {
  if (!chartRef.value) return
  
  // 销毁旧实例
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  
  // 创建新实例
  chartInstance = echarts.init(chartRef.value)
  
  // 根据类型设置不同的图表实例
  if (type === 'trend') {
    trendChartInstance = chartInstance
  } else {
    equipmentChartInstance = chartInstance
  }
  
  // 更新图表
  updateChart(type)
}

// 更新图表数据
const updateChart = (type) => {
  if (!rawData.value.length) return
  
  const chartInstance = type === 'trend' ? trendChartInstance : equipmentChartInstance
  if (!chartInstance) return
  
  // 统计设备类型分布
  const typeDistribution = {}
  rawData.value.forEach(item => {
    const type = item.type || '未知类型'
    typeDistribution[type] = (typeDistribution[type] || 0) + 1
  })
  
  // 按时间统计租赁趋势
  const timeTrends = {}
  const equipmentTypes = [...new Set(rawData.value.map(item => item.type))]
  const allDates = []
  
  rawData.value.forEach(item => {
    const date = new Date(item.rental_date)
    let timeKey = timeUnit.value === 'day' 
      ? `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
      : `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}`
    
    allDates.push(timeKey)
    
    if (!timeTrends[timeKey]) {
      timeTrends[timeKey] = {}
      equipmentTypes.forEach(type => {
        timeTrends[timeKey][type] = 0
      })
    }
    
    timeTrends[timeKey][item.type] += item.rental_quantity
  })
  
  const sortedTimeKeys = [...new Set(allDates)].sort((a, b) => new Date(a) - new Date(b))
  const displayTimeKeys = sortedTimeKeys.map(key => {
    if (timeUnit.value === 'day') {
      const [year, month, day] = key.split('-')
      return `${parseInt(month)}月${parseInt(day)}日`
    } else {
      const [year, month] = key.split('-')
      return `${year}年${parseInt(month)}月`
    }
  })
  
  if (type === 'trend') {
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        data: equipmentTypes,
        textStyle: {
          color: '#606266'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: displayTimeKeys,
        axisLabel: {
          color: '#606266',
          rotate: timeUnit.value === 'day' ? 45 : 0
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#606266'
        }
      },
      series: equipmentTypes.map(type => ({
        name: type,
        type: 'line',
        stack: '总量',
        areaStyle: {
          opacity: 0.8,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: getRandomColor(0.5) },
            { offset: 1, color: getRandomColor(0.1) }
          ])
        },
        data: sortedTimeKeys.map(key => timeTrends[key][type] || 0)
      }))
    }
    chartInstance.setOption(option)
  } else {
    const option = {
      title: {
        text: '器材租赁占比',
        left: 'center',
        textStyle: {
          fontSize: 16,
          color: '#606266'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: '5%',
        top: 'center',
        textStyle: {
          color: '#606266'
        }
      },
      series: [
        {
          name: '租赁占比',
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 5,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {d}%',
            color: '#606266'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: true
          },
          data: Object.entries(typeDistribution).map(([name, value]) => ({
            name,
            value
          }))
        }
      ],
      color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#B37FEB']
    }
    chartInstance.setOption(option)
  }
  
  // 延迟确保渲染完成
  setTimeout(() => chartInstance.resize(), 100)
}

// 生成随机颜色
const getRandomColor = (opacity = 1) => {
  const r = Math.floor(Math.random() * 255)
  const g = Math.floor(Math.random() * 255)
  const b = Math.floor(Math.random() * 255)
  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}

// 获取数据
const fetchData = async () => {
  try {
    loading.value = true
    
    // 获取所有租赁记录
    const response = await EquipmentService.getAllRentals()
    
    if (response.code === 200) {
      rawData.value = response.data.map(item => {
        // 自动标记逾期状态
        if (item.rental_status === '租借中' && isOverdue(item)) {
          return {...item, rental_status: '逾期未还'}
        }
        return item
      })
      pagination.total = rawData.value.length
      
      // 更新统计数据
      updateStats()
      
      // 更新当前活动图表
      if (activeTab.value === 'trend') {
        updateChart('trend')
      } else {
        updateChart('equipment')
      }
    } else {
      ElMessage.error(response.msg || '获取租赁记录失败')
    }
  } catch (error) {
    ElMessage.error('数据加载失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 更新统计信息
const updateStats = () => {
  if (!rawData.value.length) return
  
  // 总租赁次数
  stats.totalRentals = rawData.value.length
  
  // 活跃用户数
  const uniqueUsers = new Set(rawData.value.map(item => item.user_id))
  stats.activeUsers = uniqueUsers.size
  
  // 设备利用率（这里简化计算，实际应根据业务逻辑）
  stats.utilizationRate = Math.min(100, Math.floor(rawData.value.length / 5))
  
  // 最受欢迎设备
  const equipmentCount = {}
  rawData.value.forEach(item => {
    const name = item.equipment_name
    equipmentCount[name] = (equipmentCount[name] || 0) + 1
  })
  const popular = Object.entries(equipmentCount).sort((a, b) => b[1] - a[1])[0]
  stats.popularEquipment = popular ? popular[0] : '--'
}

// 改变时间单位
const changeTimeUnit = (unit) => {
  timeUnit.value = unit
  if (activeTab.value === 'trend') {
    updateChart('trend')
  }
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.current = 1
}

// 当前页变化
const handleCurrentChange = (current) => {
  pagination.current = current
}

// 监听tab切换
watch(activeTab, (newTab) => {
  nextTick(() => {
    if (newTab === 'trend') {
      initChart(trendChart, trendChartInstance, 'trend')
    } else {
      initChart(equipmentChart, equipmentChartInstance, 'equipment')
    }
  })
})

// 窗口大小变化时重新调整图表大小
const handleResize = () => {
  if (trendChartInstance) trendChartInstance.resize()
  if (equipmentChartInstance) equipmentChartInstance.resize()
}

onMounted(() => {
  // 设置默认日期范围（最近30天）
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)
  dateRange.value = [start, end]
  
  // 初始化数据
  fetchData()
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onUnmounted(() => {
  if (trendChartInstance) {
    trendChartInstance.dispose()
    trendChartInstance = null
  }
  if (equipmentChartInstance) {
    equipmentChartInstance.dispose()
    equipmentChartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.equipment-rental-stats {
  padding: 20px;
}

.header {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 18px;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.time-toggle {
  margin-left: 10px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.chart-tabs {
  margin-top: 20px;
}

.chart-container {
  width: 100%;
  height: 400px;
}

.chart-placeholder {
  width: 100%;
  height: 400px;
  background-color: #f5f7fa;
}

.data-table {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>  