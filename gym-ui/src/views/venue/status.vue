<template>
    <div class="reservation-status">
      <el-card shadow="hover">
        <div class="header">
          <h2>预约情况统计</h2>
          <div class="header-controls">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="fetchData"
            />
            <el-select
              v-model="venueType"
              placeholder="选择场馆类型"
              clearable
              @change="fetchData"
            >
              <el-option
                v-for="item in venueTypes"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </div>
  
        <!-- 统计卡片 -->
        <el-row :gutter="20" class="stats-row">
          <el-col :span="6">
            <StatCard 
              title="总预约数" 
              :value="stats.totalReservations" 
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
              title="场馆利用率" 
              :value="`${stats.utilizationRate}%`" 
              icon="el-icon-data-line"
              color="#E6A23C"
            />
          </el-col>
          <el-col :span="6">
            <StatCard 
              title="最热门场馆" 
              :value="stats.popularVenue" 
              icon="el-icon-star-on"
              color="#F56C6C"
            />
          </el-col>
        </el-row>
  
        <!-- 图表区域 -->
        <el-tabs v-model="activeTab" class="chart-tabs">
          <el-tab-pane label="预约趋势" name="trend">
            <div ref="trendChart" class="chart-container"></div>
          </el-tab-pane>
          <el-tab-pane label="场馆分布" name="venue">
            <div ref="venueChart" class="chart-container"></div>
          </el-tab-pane>
        </el-tabs>
  
        <!-- 数据表格 -->
        <el-table 
          :data="filteredReservations" 
          stripe 
          border 
          v-loading="loading"
          class="data-table"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="venue_name" label="场馆名称" width="150" />
          <el-table-column label="场馆类型" width="120">
            <template #default="{row}">
              {{ getVenueTypeLabel(row.type) }}
            </template>
          </el-table-column>
          <el-table-column prop="user_name" label="预约用户" width="120" />
          <el-table-column label="预约时间" width="220">
            <template #default="{row}">
              {{ formatDate(row.start_time) }} {{ formatTimeSlot(row.start_time, row.end_time) }}
            </template>
          </el-table-column>
          <el-table-column label="状态" width="120">
            <template #default="{row}">
              <el-tag :type="getStatusTagType(row.status)">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
  
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="pagination"
        />
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, computed, onMounted, watch, nextTick, onBeforeUnmount } from 'vue'
  import { ElMessage } from 'element-plus'
  import * as echarts from 'echarts'
  import VenueService, { VenueType, ReservationStatus } from '@/api/venue/index'
  import { useAuthStore } from '@/stores/auth'
  
  const authStore = useAuthStore()
  
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
  
  // ECharts实例
  const trendChart = ref(null)
  const venueChart = ref(null)
  let trendChartInstance = null
  let venueChartInstance = null
  
  const dateRange = ref([])
  const venueType = ref('')
  const activeTab = ref('trend')
  const loading = ref(false)
  const reservations = ref([])
  
  const pagination = reactive({
    current: 1,
    size: 10,
    total: 0
  })
  
  const venueTypes = [
    { value: VenueType.BASKETBALL, label: '篮球场' },
    { value: VenueType.BADMINTON, label: '羽毛球场' },
    { value: VenueType.SWIMMING, label: '游泳池' },
    { value: VenueType.GYM, label: '健身房' },
    { value: VenueType.TENNIS, label: '网球场' }
  ]
  
  const stats = reactive({
    totalReservations: 0,
    activeUsers: 0,
    utilizationRate: 0,
    popularVenue: '--'
  })
  
  // 获取场馆类型中文标签
  const getVenueTypeLabel = (type) => {
    const typeMap = {
      [VenueType.BASKETBALL]: '篮球场',
      [VenueType.BADMINTON]: '羽毛球场',
      [VenueType.SWIMMING]: '游泳池',
      [VenueType.GYM]: '健身房',
      [VenueType.TENNIS]: '网球场'
    }
    return typeMap[type] || type
  }
  
  // 获取状态中文标签
  const getStatusLabel = (status) => {
    const statusMap = {
      [ReservationStatus.PENDING]: '待确认',
      [ReservationStatus.CONFIRMED]: '已预约',
      [ReservationStatus.CANCELLED]: '已取消',
      [ReservationStatus.COMPLETED]: '已完成'
    }
    return statusMap[status] || status
  }
  
  // 获取状态标签类型
  const getStatusTagType = (status) => {
    switch(status) {
      case ReservationStatus.CONFIRMED: return 'success'
      case ReservationStatus.CANCELLED: return 'info'
      case ReservationStatus.COMPLETED: return 'primary'
      default: return 'primary'
    }
  }
  
  // 格式化日期为 YYYY-MM-DD
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toISOString().split('T')[0]
  }
  
  // 格式化时间段为 HH:mm-HH:mm
  const formatTimeSlot = (startTime, endTime) => {
    const start = new Date(startTime)
    const end = new Date(endTime)
    return `${start.getHours().toString().padStart(2, '0')}:${start.getMinutes().toString().padStart(2, '0')}-${end.getHours().toString().padStart(2, '0')}:${end.getMinutes().toString().padStart(2, '0')}`
  }
  
  // 过滤预约记录
  const filteredReservations = computed(() => {
    let result = reservations.value
    
    if (venueType.value) {
      result = result.filter(item => item.venue?.type === venueType.value)
    }
    
    if (dateRange.value && dateRange.value.length === 2) {
      const start = new Date(dateRange.value[0])
      const end = new Date(dateRange.value[1])
      result = result.filter(item => {
        const date = new Date(item.start_time)
        return date >= start && date <= end
      })
    }
    
    // 更新统计信息
    updateStats(result)
    
    // 更新图表
    updateCharts(result)
    
    // 分页处理
    pagination.total = result.length
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    return result.slice(start, end)
  })
  
  // 更新统计数据
  const updateStats = (data) => {
    // 总预约数
    stats.totalReservations = data.length
    
    // 活跃用户数
    const uniqueUsers = new Set(data.map(item => item.user?.id))
    stats.activeUsers = uniqueUsers.size
    
    // 场馆利用率（简化计算）
    stats.utilizationRate = Math.min(100, Math.floor(data.length / 5))
    
    // 最热门场馆
    const venueCount = {}
    data.forEach(item => {
      const name = item.venue?.name
      if (name) {
        venueCount[name] = (venueCount[name] || 0) + 1
      }
    })
    const popular = Object.entries(venueCount).sort((a, b) => b[1] - a[1])[0]
    stats.popularVenue = popular ? popular[0] : '--'
  }
  
  // 初始化趋势图表
  const initTrendChart = () => {
    if (!trendChart.value) return
    
    trendChartInstance = echarts.init(trendChart.value)
    updateTrendChart(filteredReservations.value)
    
    // 窗口大小变化时重绘图表
    window.addEventListener('resize', () => {
      trendChartInstance?.resize()
    })
  }
  
  // 更新趋势图表
  const updateTrendChart = (data) => {
    if (!trendChartInstance) return
    
    const dateCountMap = {}
    
    // 按日期统计预约数量
    data.forEach(item => {
      const date = formatDate(item.start_time)
      dateCountMap[date] = (dateCountMap[date] || 0) + 1
    })
    
    // 转换为数组并排序
    const sortedDates = Object.keys(dateCountMap).sort()
    const counts = sortedDates.map(date => dateCountMap[date])
    
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}<br/>预约数量: {c}'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: sortedDates,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '预约数量'
      },
      series: [
        {
          name: '预约数量',
          type: 'line',
          data: counts,
          smooth: true,
          itemStyle: {
            color: '#409EFF'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgba(64, 158, 255, 0.3)'
              },
              {
                offset: 1,
                color: 'rgba(64, 158, 255, 0.1)'
              }
            ])
          }
        }
      ]
    }
    
    trendChartInstance.setOption(option)
  }
  
  // 初始化场馆分布图表
  const initVenueChart = () => {
    if (!venueChart.value) return
    
    venueChartInstance = echarts.init(venueChart.value)
    updateVenueChart(filteredReservations.value)
    
    // 窗口大小变化时重绘图表
    window.addEventListener('resize', () => {
      venueChartInstance?.resize()
    })
  }
  
  // 更新场馆分布图表
  const updateVenueChart = (data) => {
    if (!venueChartInstance) return
    
    const venueCountMap = {}
    
    // 按场馆统计预约数量
    data.forEach(item => {
      const venueName = item.venue_name || '未知场馆'
      venueCountMap[venueName] = (venueCountMap[venueName] || 0) + 1
    })
    
    // 转换为数组
    const venues = Object.keys(venueCountMap)
    const counts = venues.map(venue => ({
      value: venueCountMap[venue],
      name: venue
    }))
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        data: venues
      },
      series: [
        {
          name: '预约分布',
          type: 'pie',
          radius: ['50%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: counts
        }
      ]
    }
    
    venueChartInstance.setOption(option)
  }
  
  // 更新所有图表
  const updateCharts = (data) => {
    updateTrendChart(data)
    updateVenueChart(data)
  }
  
  // 获取预约数据
  const fetchData = async () => {
    loading.value = true
    try {
      const response = await VenueService.getAllReservations(authStore.user.permission_level)
      reservations.value = response.data || []
    } catch (error) {
      ElMessage.error('获取预约数据失败')
      console.error(error)
    } finally {
      loading.value = false
    }
  }
  
  const handleSizeChange = (size) => {
    pagination.size = size
    pagination.current = 1
  }
  
  const handleCurrentChange = (current) => {
    pagination.current = current
  }
  
  // 监听tab切换
  watch(activeTab, (newVal) => {
    nextTick(() => {
      if (newVal === 'trend') {
        updateTrendChart(filteredReservations.value)
      } else if (newVal === 'venue') {
        updateVenueChart(filteredReservations.value)
      }
    })
  })
  
  onMounted(() => {
    fetchData()
    nextTick(() => {
      initTrendChart()
      initVenueChart()
    })
  })
  
  // 组件卸载时销毁图表实例
  onBeforeUnmount(() => {
    if (trendChartInstance) {
      trendChartInstance.dispose()
      trendChartInstance = null
    }
    if (venueChartInstance) {
      venueChartInstance.dispose()
      venueChartInstance = null
    }
    window.removeEventListener('resize', () => {
      trendChartInstance?.resize()
      venueChartInstance?.resize()
    })
  })
  </script>
  
  <style scoped>
  .reservation-status {
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .header h2 {
    margin: 0;
  }
  
  .header-controls {
    display: flex;
    gap: 10px;
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
    height: 400px;
    width: 100%;
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