<template>
    <div class="my-reservations">
      <el-card shadow="hover">
        <div class="header">
          <h2>我的预约</h2>
          <div class="header-controls">
            <el-select v-model="statusFilter" placeholder="预约状态" clearable>
              <el-option
                v-for="item in statusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
            />
            <el-button type="primary" @click="fetchReservations">查询</el-button>
          </div>
        </div>
  
        <el-table :data="filteredReservations" v-loading="loading" style="width: 100%">
          <el-table-column prop="id" label="预约号" width="100" />
          <el-table-column prop="venue_name" label="场馆名称" width="150" />
          <el-table-column label="场馆类型" width="120">
            <template #default="{row}">
              {{ getVenueTypeLabel(row.type) }}
            </template>
          </el-table-column>
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
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button
                size="small"
                type="danger"
                @click="cancelReservation(row)"
                :disabled="row.status !== 'confirmed'"
              >
                取消
              </el-button>
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
  import { ref, computed, onMounted, reactive } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import VenueService, { VenueType, ReservationStatus } from '@/api/venue/index'
  import { useAuthStore } from '@/stores/auth'
  
  const authStore = useAuthStore()
  const loading = ref(false)
  const reservations = ref([])
  const statusFilter = ref('')
  const dateRange = ref([])
  
  const pagination = reactive({
    current: 1,
    size: 10,
    total: 0
  })
  
  const statusOptions = [
    { value: 'confirmed', label: '已预约' },
    { value: 'cancelled', label: '已取消' },
    { value: 'completed', label: '已完成' }
  ]
  
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
      case ReservationStatus.COMPLETED: return ''
      default: return ''
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
    
    if (statusFilter.value) {
      result = result.filter(item => item.status === statusFilter.value)
    }
    
    if (dateRange.value && dateRange.value.length === 2) {
      const start = new Date(dateRange.value[0])
      const end = new Date(dateRange.value[1])
      result = result.filter(item => {
        const date = new Date(item.start_time)
        return date >= start && date <= end
      })
    }
    
    // 分页处理
    pagination.total = result.length
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    return result.slice(start, end)
  })
  
  // 获取我的预约记录
  const fetchReservations = async () => {
    loading.value = true
    try {
      const response = await VenueService.getMyReservations(authStore.user.id)
      reservations.value = response.data || []
    } catch (error) {
      ElMessage.error('获取预约记录失败')
      console.error(error)
    } finally {
      loading.value = false
    }
  }
  
  // 取消预约
  const cancelReservation = async (reservation) => {
    try {
      await ElMessageBox.confirm('确定要取消此预约吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      const response = await VenueService.cancelReservation(reservation.id)
      if (response.code === 200) {
        ElMessage.success('取消预约成功')
        // 更新本地状态
        const index = reservations.value.findIndex(r => r.id === reservation.id)
        if (index !== -1) {
          reservations.value[index].status = ReservationStatus.CANCELLED
        }
      } else {
        ElMessage.error(response.msg || '取消预约失败')
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('取消预约失败')
      }
    }
  }
  
  const handleSizeChange = (size) => {
    pagination.size = size
    pagination.current = 1
  }
  
  const handleCurrentChange = (current) => {
    pagination.current = current
  }
  
  onMounted(() => {
    fetchReservations()
  })
  </script>
  
  <style scoped>
  .my-reservations {
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
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  </style>