<template>
    <div class="venue-management">
      <el-card shadow="hover">
        <div class="header">
          <h2>场馆管理</h2>
          <div class="header-controls">
            <el-button-group>
              <el-button type="primary" @click="handleAddVenue">新增场馆</el-button>
              <el-button type="success" :disabled="!selectedVenues.length" @click="batchUpdateStatus('active')">
                开馆
              </el-button>
              <el-button type="warning" :disabled="!selectedVenues.length" @click="batchUpdateStatus('maintenance')">
                维护
              </el-button>
              <el-button type="danger" :disabled="!selectedVenues.length" @click="batchUpdateStatus('closed')">
                闭馆
              </el-button>
            </el-button-group>
          </div>
        </div>
  
        <el-table 
          :data="venues" 
          v-loading="loading"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="场馆名称" width="150" />
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
          <el-table-column prop="total_count" label="总数量" width="100" />
          <el-table-column prop="available_count" label="可用数量" width="100" />
          <el-table-column prop="capacity" label="容量" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{row}">
              <el-tag :type="getStatusTagType(row.status)">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" />
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button size="small" @click="handleEditVenue(row)">编辑</el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleDeleteVenue(row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
  
        <!-- 场馆编辑对话框 -->
        <el-dialog
          v-model="dialogVisible"
          :title="dialogTitle"
          width="50%"
        >
          <el-form :model="venueForm" label-width="100px" :rules="rules" ref="venueFormRef">
            <el-form-item label="场馆名称" prop="name">
              <el-input v-model="venueForm.name" />
            </el-form-item>
            <el-form-item label="场馆类型" prop="type">
              <el-select v-model="venueForm.type" placeholder="请选择">
                <el-option
                  v-for="item in venueTypes"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="位置" prop="location">
              <el-input v-model="venueForm.location" />
            </el-form-item>
            <el-form-item label="开放时间" required>
              <el-time-picker
                v-model="venueForm.open_time"
                format="HH:mm"
                value-format="HH:mm:ss"
                placeholder="选择时间"
              />
              <span style="margin: 0 10px">至</span>
              <el-time-picker
                v-model="venueForm.close_time"
                format="HH:mm"
                value-format="HH:mm:ss"
                placeholder="选择时间"
              />
            </el-form-item>
            <el-form-item label="总数量" prop="total_count">
              <el-input-number v-model="venueForm.total_count" :min="1" />
            </el-form-item>
            <el-form-item label="可用数量" prop="available_count">
              <el-input-number v-model="venueForm.available_count" :min="0" :max="venueForm.total_count" />
            </el-form-item>
            <el-form-item label="容量" prop="capacity">
              <el-input-number v-model="venueForm.capacity" :min="1" />
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-select v-model="venueForm.status" placeholder="请选择">
                <el-option
                  v-for="item in venueStatuses"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="描述">
              <el-input
                v-model="venueForm.description"
                type="textarea"
                :rows="3"
              />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitVenueForm">确定</el-button>
          </template>
        </el-dialog>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import VenueService, { VenueType, VenueStatus } from '@/api/venue/index'
  
  const loading = ref(false)
  const venues = ref([])
  const dialogVisible = ref(false)
  const dialogTitle = ref('新增场馆')
  const isEditMode = ref(false)
  const venueFormRef = ref(null)
  const selectedVenues = ref([])
  
  const venueTypes = [
    { value: VenueType.BASKETBALL, label: '篮球场' },
    { value: VenueType.BADMINTON, label: '羽毛球场' },
    { value: VenueType.SWIMMING, label: '游泳池' },
    { value: VenueType.GYM, label: '健身房' },
    { value: VenueType.TENNIS, label: '网球场' }
  ]
  
  const venueStatuses = [
    { value: VenueStatus.ACTIVE, label: '开放中' },
    { value: VenueStatus.MAINTENANCE, label: '维护中' },
    { value: VenueStatus.CLOSED, label: '已关闭' }
  ]
  
  const venueForm = reactive({
    name: '',
    type: '',
    location: '',
    open_time: '08:00:00',
    close_time: '22:00:00',
    total_count: 1,
    available_count: 1,
    capacity: 10,
    status: VenueStatus.ACTIVE,
    description: ''
  })
  
  const rules = {
    name: [{ required: true, message: '请输入场馆名称', trigger: 'blur' }],
    type: [{ required: true, message: '请选择场馆类型', trigger: 'change' }],
    location: [{ required: true, message: '请输入场馆位置', trigger: 'blur' }],
    total_count: [{ required: true, message: '请输入总数量', trigger: 'blur' }],
    available_count: [{ required: true, message: '请输入可用数量', trigger: 'blur' }],
    capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }],
    status: [{ required: true, message: '请选择状态', trigger: 'change' }]
  }
  
  const getVenueTypeLabel = (type) => {
    const found = venueTypes.find(item => item.value === type)
    return found ? found.label : type
  }
  
  const getStatusLabel = (status) => {
    const found = venueStatuses.find(item => item.value === status)
    return found ? found.label : status
  }
  
  const getStatusTagType = (status) => {
    switch (status) {
      case VenueStatus.ACTIVE: return 'success'
      case VenueStatus.MAINTENANCE: return 'warning'
      case VenueStatus.CLOSED: return 'danger'
      default: return 'info'
    }
  }
  
  const formatTime = (timeStr) => {
    if (!timeStr) return ''
    const [hours, minutes] = timeStr.split(':')
    return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`
  }
  
  const fetchVenues = async () => {
    loading.value = true
    try {
      const response = await VenueService.getVenues()
    //   console.log(response);
      
        
      venues.value = response.data || []
    } catch (error) {
      ElMessage.error('获取场馆列表失败')
    } finally {
      loading.value = false
    }
  }
  
  const handleAddVenue = () => {
    dialogTitle.value = '新增场馆'
    isEditMode.value = false
    resetForm()
    dialogVisible.value = true
  }
  
  const handleEditVenue = (venue) => {
    dialogTitle.value = '编辑场馆'
    isEditMode.value = true
    Object.assign(venueForm, {
      ...venue,
      open_time: venue.open_time || '08:00:00',
      close_time: venue.close_time || '22:00:00'
    })
    dialogVisible.value = true
  }
  
  const handleDeleteVenue = async (id) => {
    try {
      await ElMessageBox.confirm('确定要删除此场馆吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      const response = await VenueService.deleteVenue(id)
      if (response.code === 200) {
        ElMessage.success('删除成功')
        fetchVenues()
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
      }
    }
  }
  
  const handleSelectionChange = (selection) => {
    selectedVenues.value = selection.map(v => v.id)
  }
  
  const batchUpdateStatus = async (status) => {
    if (!selectedVenues.value.length) return
    
    try {
      const confirmMessage = `确定要将选中的${selectedVenues.value.length}个场馆设置为${getStatusLabel(status)}吗?`
      await ElMessageBox.confirm(confirmMessage, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      loading.value = true
      const promises = selectedVenues.value.map(id => 
        VenueService.updateVenue({ id, status })
      )
      
      await Promise.all(promises)
      ElMessage.success('批量更新状态成功')
      fetchVenues()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('批量更新状态失败')
      }
    } finally {
      loading.value = false
    }
  }
  
  const resetForm = () => {
    Object.assign(venueForm, {
      name: '',
      type: '',
      location: '',
      open_time: '08:00:00',
      close_time: '22:00:00',
      total_count: 1,
      available_count: 1,
      capacity: 10,
      status: VenueStatus.ACTIVE,
      description: ''
    })
  }
  
  const submitVenueForm = async () => {
    try {
      await venueFormRef.value.validate()
      
      const formData = {
        ...venueForm,
        // 确保可用数量不超过总数量
        available_count: Math.min(venueForm.available_count, venueForm.total_count)
      }
      
      if (isEditMode.value) {
        const response = await VenueService.updateVenue(formData)
        if (response.code === 200) {
          ElMessage.success('更新成功')
          fetchVenues()
          dialogVisible.value = false
        }
      } else {
        const response = await VenueService.createVenue(formData)
        if (response.code === 200) {
          ElMessage.success('添加成功')
          fetchVenues()
          dialogVisible.value = false
        }
      }
    } catch (error) {
      console.error('表单提交错误:', error)
    }
  }
  
  onMounted(() => {
    fetchVenues()
  })
  </script>
  
  <style scoped>
  .venue-management {
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
  </style>