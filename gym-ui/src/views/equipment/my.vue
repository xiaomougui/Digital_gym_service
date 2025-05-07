<template>
    <div class="my-rentals">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>我的租赁记录</span>
            <el-button type="primary" size="small" @click="refreshList">刷新</el-button>
          </div>
        </template>
  
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="全部" name="all"></el-tab-pane>
          <el-tab-pane label="租借中" name="renting"></el-tab-pane>
          <el-tab-pane label="已归还" name="returned"></el-tab-pane>
          <el-tab-pane label="已取消" name="canceled"></el-tab-pane>
          <el-tab-pane label="逾期未还" name="overdue"></el-tab-pane>
        </el-tabs>
  
        <el-table 
          :data="paginatedData" 
          style="width: 100%" 
          v-loading="loading"
          border
          stripe>
          <el-table-column prop="id" label="租赁ID" width="100" align="center" />
          <el-table-column prop="equipment_name" label="设备名称" width="150" align="center" />
          <el-table-column label="设备类型" width="120" align="center">
            <template #default="{row}">
              <el-tag>{{ getEquipmentType(row.equipment_id) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="租赁日期" width="220" align="center">
            <template #default="{row}">
              {{ formatDate(row.rental_date) }} 至 {{ formatDate(row.expected_return_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="rental_quantity" label="数量" width="80" align="center" />
          <el-table-column label="状态" width="120" align="center">
            <template #default="{row}">
              <el-tag :type="getStatusTagType(row)">
                {{ row.rental_status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="center" fixed="right">
            <template #default="{row}">
              <el-button
                v-if="row.rental_status === '租借中' && !isOverdue(row)"
                type="danger"
                size="small"
                @click="cancelRental(row.id)"
                plain
              >
                取消
              </el-button>
              <el-button
                v-if="row.rental_status === '租借中'"
                type="success"
                size="small"
                @click="returnEquipment(row.id)"
                plain
              >
                归还
              </el-button>
              <el-button 
                size="small" 
                @click="showDetail(row)"
                plain
              >
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
  
        <div class="pagination">
          <el-pagination
            v-model:current-page="pagination.current"
            v-model:page-size="pagination.size"
            :total="filteredData.length"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
  
      <!-- 租赁详情对话框 -->
      <el-dialog v-model="detailDialogVisible" title="租赁详情" width="700px" center>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="租赁ID">{{ currentRental.id }}</el-descriptions-item>
          <el-descriptions-item label="设备名称">{{ currentRental.equipment_name }}</el-descriptions-item>
          <el-descriptions-item label="设备类型">{{ getEquipmentType(currentRental.equipment_id) }}</el-descriptions-item>
          <el-descriptions-item label="租赁数量">{{ currentRental.rental_quantity }}</el-descriptions-item>
          <el-descriptions-item label="租赁日期">
            {{ formatDate(currentRental.rental_date) }} 至 {{ formatDate(currentRental.expected_return_date) }}
          </el-descriptions-item>
          <el-descriptions-item label="实际归还日期">
            {{ currentRental.actual_return_date ? formatDate(currentRental.actual_return_date) : '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="租赁状态">
            <el-tag :type="getStatusTagType(currentRental)">
              {{ currentRental.rental_status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="押金">{{ currentRental.deposit?.toFixed(2) || '0.00' }}元</el-descriptions-item>
          <el-descriptions-item label="租赁费用">{{ currentRental.rental_fee?.toFixed(2) || '0.00' }}元</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentRental.notes || '无' }}</el-descriptions-item>
        </el-descriptions>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, computed, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import EquipmentService from '@/api/equipment/index'
  import { useAuthStore } from '@/stores/auth'
  
  const authStore = useAuthStore()
  
  // 设备类型缓存
  const equipmentTypes = ref({})
  
  // 当前激活的标签页
  const activeTab = ref('all')
  
  // 分页信息
  const pagination = reactive({
    current: 1,
    size: 10
  })
  
  // 加载状态
  const loading = ref(false)
  
  // 租赁数据
  const rentals = ref([])
  
  // 当前查看的租赁记录
  const currentRental = ref({})
  
  // 对话框显示状态
  const detailDialogVisible = ref(false)
  
  // 根据标签页过滤租赁记录
  const filteredData = computed(() => {
    let result = rentals.value
    
    if (activeTab.value !== 'all') {
      if (activeTab.value === 'overdue') {
        result = result.filter(item => isOverdue(item))
      } else {
        const statusMap = {
          renting: '租借中',
          returned: '已归还',
          canceled: '已取消'
        }
        result = result.filter(item => item.rental_status === statusMap[activeTab.value])
      }
    }
    
    return result
  })
  
  // 分页数据
  const paginatedData = computed(() => {
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    return filteredData.value.slice(start, end)
  })
  
  // 获取设备类型
  const getEquipmentType = (equipmentId) => {
    return equipmentTypes.value[equipmentId] || '未知类型'
  }
  
  // 获取状态标签类型
  const getStatusTagType = (rental) => {
    if (isOverdue(rental)) return 'danger'
    switch(rental.rental_status) {
      case '租借中': return ''
      case '已归还': return 'success'
      case '已取消': return 'info'
      default: return ''
    }
  }
  
  // 检查是否逾期
  const isOverdue = (rental) => {
    if (rental.rental_status !== '租借中') return false
    const now = new Date()
    const returnDate = new Date(rental.expected_return_date)
    return now > returnDate
  }
  
  // 格式化日期
  const formatDate = (dateString) => {
    if (!dateString) return '--'
    const date = new Date(dateString)
    return date.toLocaleDateString()
  }
  
  // 获取租赁记录
  const fetchRentals = async () => {
    try {
      loading.value = true
      const userId = authStore.user?.id
      if (!userId) {
        ElMessage.error('用户信息获取失败')
        return
      }
  
      const response = await EquipmentService.getMyRentals(userId)
      
      if (response.code === 200) {
        rentals.value = response.data.map(item => {
          // 自动标记逾期状态
          if (item.rental_status === '租借中' && isOverdue(item)) {
            return {...item, rental_status: '逾期未还'}
          }
          return item
        })
        
        // 缓存设备类型信息
        response.data.forEach(rental => {
          if (!equipmentTypes.value[rental.equipment_id]) {
            fetchEquipmentType(rental.equipment_id)
          }
        })
      } else {
        ElMessage.error(response.msg || '获取租赁记录失败')
      }
    } catch (error) {
      ElMessage.error('获取租赁记录失败: ' + error.message)
    } finally {
      loading.value = false
    }
  }
  
  // 获取设备类型信息
  const fetchEquipmentType = async (equipmentId) => {
    try {
      const response = await EquipmentService.getEquipmentList()
      if (response.code === 200) {
        const equipment = response.data.find(e => e.id === equipmentId)
        if (equipment) {
          equipmentTypes.value[equipmentId] = equipment.type
        }
      }
    } catch (error) {
      console.error('获取设备类型失败:', error)
    }
  }
  
  // 标签页变化
  const handleTabChange = () => {
    pagination.current = 1
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
  
  // 刷新列表
  const refreshList = () => {
    pagination.current = 1
    fetchRentals()
  }
  
  // 取消租赁
  const cancelRental = async (rentalId) => {
    try {
      await ElMessageBox.confirm('确定要取消这条租赁记录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      const response = await EquipmentService.cancelRental(rentalId)
      
      if (response.code === 200) {
        ElMessage.success('取消成功')
        refreshList()
      } else {
        ElMessage.error(response.msg || '取消失败')
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('取消失败: ' + error.message)
      }
    }
  }
  
  // 归还设备
  const returnEquipment = async (rentalId) => {
    try {
      await ElMessageBox.confirm('确定要归还设备吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      const response = await EquipmentService.returnEquipment(rentalId)
      
      if (response.code === 200) {
        ElMessage.success('归还成功')
        refreshList()
      } else {
        ElMessage.error(response.msg || '归还失败')
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('归还失败: ' + error.message)
      }
    }
  }
  
  // 查看详情
  const showDetail = (rental) => {
    currentRental.value = rental
    detailDialogVisible.value = true
  }
  
  onMounted(() => {
    fetchRentals()
  })
  </script>
  
  <style scoped lang="scss">
  .my-rentals {
    padding: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      
      span {
        font-size: 18px;
        font-weight: bold;
      }
    }
    
    .pagination {
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
    
    :deep(.el-tabs) {
      margin-bottom: 20px;
    }
    
    :deep(.el-table) {
      margin-top: 10px;
      
      .el-button {
        margin: 2px;
      }
    }
  }
  </style>