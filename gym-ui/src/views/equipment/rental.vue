<template>
    <div class="venue-reservation">
      <el-card shadow="hover">
        <div class="header">
          <h2>场馆预约</h2>
          <div class="header-controls">
            <el-date-picker
              v-model="selectedDate"
              type="date"
              placeholder="选择预约日期"
              :disabled-date="disabledDate"
              @change="handleDateChange"
            />
          </div>
        </div>
  
        <div class="table-container">
          <el-table :data="filteredVenues" v-loading="loading" style="width: 100%">
            <el-table-column prop="name" label="场馆名称" width="150" fixed />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{row}">
                {{ getVenueTypeLabel(row.type) }}
              </template>
            </el-table-column>
            <el-table-column prop="location" label="位置" width="180" />
            <el-table-column label="开放时间" width="180">
              <template #default="{row}">
                {{ formatTime(row.open_time) }} - {{ formatTime(row.close_time) }}
              </template>
            </el-table-column>
            <el-table-column prop="available_count" label="剩余数量" width="100" />
            <el-table-column label="可预约时间段" min-width="300">
              <template #default="{row}">
                <el-select 
                  v-model="row.selectedTimeSlot" 
                  placeholder="选择时间段"
                  @change="handleTimeSlotChange(row)"
                >
                  <el-option
                    v-for="slot in getAvailableTimeSlots(row)"
                    :key="slot.value"
                    :label="slot.label"
                    :value="slot.value"
                    :disabled="slot.disabled"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{row}">
                <el-button 
                  type="primary" 
                  size="small" 
                  :disabled="!row.selectedTimeSlot"
                  @click="handleReserve(row)"
                >
                  预约
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  import VenueService, { VenueType } from '@/api/venue/index'
  import { useAuthStore } from '@/stores/auth'
  
  const loading = ref(false)
  const venues = ref([])
  const reservations = ref([])
  const authStore = useAuthStore()
  const selectedDate = ref(new Date())
  
  // 禁用过去的日期
  const disabledDate = (date) => {
    return date < new Date(new Date().setHours(0, 0, 0, 0))
  }
  
  // 获取场馆类型标签
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
  
  // 格式化时间显示
  const formatTime = (timeStr) => {
    if (!timeStr) return ''
    const [hours, minutes] = timeStr.split(':')
    return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`
  }
  
  // 格式化日期时间为YYYY-MM-DD HH:mm:ss格式
  const formatDateTime = (date) => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
  }
  
  // 获取场馆列表
  const fetchVenues = async () => {
    loading.value = true
    try {
      const response = await VenueService.getVenues()
      venues.value = (response.data || []).map(venue => ({
        ...venue,
        selectedTimeSlot: null
      }))
    } catch (error) {
      ElMessage.error('获取场馆列表失败')
    } finally {
      loading.value = false
    }
  }
  
  // 获取预约记录
  const fetchReservations = async (date) => {
    try {
      const response = await VenueService.getAllReservations(authStore.user.permission_level)
      reservations.value = response.data || []
    } catch (error) {
      console.error('获取预约记录失败:', error)
    }
  }
  
  // 处理日期变化
  const handleDateChange = (date) => {
    fetchReservations(date)
  }
  
  // 生成可预约时间段
  const getAvailableTimeSlots = (venue) => {
    if (!venue.open_time || !venue.close_time) return []
    
    const slots = []
    const [openHour, openMinute] = venue.open_time.split(':').map(Number)
    const [closeHour, closeMinute] = venue.close_time.split(':').map(Number)
    
    let currentHour = openHour
    let currentMinute = openMinute
    
    while (currentHour < closeHour || (currentHour === closeHour && currentMinute < closeMinute)) {
      const startTime = `${currentHour.toString().padStart(2, '0')}:${currentMinute.toString().padStart(2, '0')}`
      
      // 增加1小时
      let endHour = currentHour + 1
      let endMinute = currentMinute
      if (endHour > closeHour || (endHour === closeHour && endMinute > closeMinute)) {
        break
      }
      
      const endTime = `${endHour.toString().padStart(2, '0')}:${endMinute.toString().padStart(2, '0')}`
      const slotValue = `${startTime}-${endTime}`
      
      // 检查该时间段是否已被预约
      const isBooked = reservations.value.some(res => {
        const resDate = new Date(res.start_time)
        return res.venue_id === venue.id && 
          resDate.toDateString() === new Date(selectedDate.value).toDateString() &&
          isTimeSlotOverlap(res, slotValue)
      })
      
      slots.push({
        label: `${startTime}~${endTime}`,
        value: slotValue,
        disabled: isBooked || venue.available_count <= 0
      })
      
      currentHour = endHour
      currentMinute = endMinute
    }
    
    return slots
  }
  
  // 检查时间段是否重叠
  const isTimeSlotOverlap = (reservation, timeSlot) => {
    const [start, end] = timeSlot.split('-')
    const resStart = new Date(reservation.start_time).toTimeString().substring(0, 5)
    const resEnd = new Date(reservation.end_time).toTimeString().substring(0, 5)
    
    return !(end <= resStart || start >= resEnd)
  }
  
  // 处理时间段选择
  const handleTimeSlotChange = (venue) => {
    console.log(`${venue.name} 选择了时间段: ${venue.selectedTimeSlot}`)
  }
  
  // 处理预约
  const handleReserve = async (venue) => {
    if (!venue.selectedTimeSlot) {
      ElMessage.warning('请选择预约时间段')
      return
    }
    
    const [startTimeStr, endTimeStr] = venue.selectedTimeSlot.split('-')
    
    // 创建北京时间
    const beijingStartDate = new Date(selectedDate.value)
    const [startHour, startMinute] = startTimeStr.split(':').map(Number)
    beijingStartDate.setHours(startHour, startMinute, 0, 0)
    
    const beijingEndDate = new Date(selectedDate.value)
    const [endHour, endMinute] = endTimeStr.split(':').map(Number)
    beijingEndDate.setHours(endHour, endMinute, 0, 0)
    
    // 转换为GMT时间（减去8小时）
    const gmtStartTime = new Date(beijingStartDate.getTime() - (8 * 60 * 60 * 1000))
    const gmtEndTime = new Date(beijingEndDate.getTime() - (8 * 60 * 60 * 1000))
    
    try {
      const reservationData = {
        venue_id: venue.id,
        user_id: authStore.user.id,
        start_time: formatDateTime(gmtStartTime), // 格式化为"2025-06-03 16:00:00"
        end_time: formatDateTime(gmtEndTime),
        notes: ''
      }
      
      const response = await VenueService.createReservation(reservationData)
      if (response.code === 200) {
        ElMessage.success('预约成功')
        fetchVenues()
        fetchReservations(selectedDate.value)
      } else {
        ElMessage.error(`错误：${response.code}：${response.msg}`)
      }
    } catch (error) {
      ElMessage.error('预约失败')
      console.error('预约错误:', error)
    }
  }
  
  // 过滤可预约场馆
  const filteredVenues = computed(() => {
    return venues.value.filter(venue => 
      venue.status === 'active' && 
      venue.available_count > 0
    )
  })
  
  onMounted(() => {
    fetchVenues()
    fetchReservations(selectedDate.value)
  })
  </script>
  
  <style scoped>
  .venue-reservation {
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
  
  .table-container {
    width: 100%;
    overflow-x: auto;
  }
  
  /* 设置表格最小宽度，确保内容不会挤压 */
  .el-table {
    min-width: 1200px;
  }
  
  /* 固定表头 */
  .el-table::v-deep .el-table__header-wrapper {
    position: sticky;
    top: 0;
    z-index: 2;
  }
  
  /* 固定列样式 */
  .el-table::v-deep .el-table__fixed, 
  .el-table::v-deep .el-table__fixed-right {
    position: sticky;
    z-index: 1;
    background: #fff;
  }
  </style>