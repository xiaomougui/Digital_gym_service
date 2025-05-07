<template>
    <div class="equipment-management">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>设备管理</span>
            <div>
              <el-button type="primary" size="small" @click="showAddDialog">新增设备</el-button>
              <el-button size="small" @click="refreshList">刷新</el-button>
            </div>
          </div>
        </template>
  
        <el-table :data="equipmentData" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="设备ID" width="100" />
          <el-table-column prop="name" label="设备名称" width="150" />
          <el-table-column prop="type" label="设备类型" width="120" />
          <el-table-column prop="total_quantity" label="总数" width="80" />
          <el-table-column prop="available_quantity" label="可租数量" width="100" />
          <el-table-column prop="price" label="单价(元)" width="120">
            <template #default="{row}">
              {{ row.price }}
            </template>
          </el-table-column>
          <el-table-column prop="location" label="存放位置" width="150" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{row}">
              <el-tag :type="row.status === '正常' ? 'success' : 'danger'">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
              <el-button
                size="small"
                type="danger"
                @click="deleteEquipment(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
  
        <div class="pagination">
          <el-pagination
            v-model:current-page="pagination.current"
            v-model:page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="fetchEquipment"
            @current-change="fetchEquipment"
          />
        </div>
      </el-card>
  
      <!-- 新增/编辑设备对话框 -->
      <el-dialog
        v-model="editDialogVisible"
        :title="isEditMode ? '编辑设备' : '新增设备'"
        width="600px"
      >
        <el-form :model="equipmentForm" :rules="rules" ref="formRef" label-width="100px">
          <el-form-item label="设备名称" prop="name">
            <el-input v-model="equipmentForm.name" placeholder="请输入设备名称" />
          </el-form-item>
          <el-form-item label="设备类型" prop="type">
            <el-select v-model="equipmentForm.type" placeholder="请选择设备类型">
              <el-option
                v-for="item in equipmentTypes"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="设备总数" prop="total_quantity">
            <el-input-number v-model="equipmentForm.total_quantity" :min="1" />
          </el-form-item>
          <el-form-item label="可租数量" prop="available_quantity">
            <el-input-number 
              v-model="equipmentForm.available_quantity" 
              :min="0" 
              :max="equipmentForm.total_quantity" 
            />
          </el-form-item>
          <el-form-item label="购买单价" prop="price">
            <el-input-number 
              v-model="equipmentForm.price" 
              :min="0" 
              :precision="2" 
              :step="0.1"
              placeholder="请输入购买单价"
            />
          </el-form-item>
          <el-form-item label="存放位置" prop="location">
            <el-input v-model="equipmentForm.location" placeholder="请输入存放位置" />
          </el-form-item>
          <el-form-item label="设备状态" prop="status">
            <el-select v-model="equipmentForm.status" placeholder="请选择设备状态">
              <el-option label="正常" value="正常" />
              <el-option label="维修中" value="维修中" />
              <el-option label="报废" value="报废" />
            </el-select>
          </el-form-item>
          <el-form-item label="购买日期" prop="purchase_date">
            <el-date-picker
              v-model="equipmentForm.purchase_date"
              type="date"
              placeholder="选择购买日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="设备描述" prop="description">
            <el-input
              v-model="equipmentForm.description"
              type="textarea"
              :rows="3"
              placeholder="请输入设备描述"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确认</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import EquipmentService from '@/api/equipment/index'
  
  // 设备类型选项（与后端enum保持一致）
  const equipmentTypes = [
    { value: '篮球类', label: '篮球类' },
    { value: '足球类', label: '足球类' },
    { value: '羽毛球类', label: '羽毛球类' },
    { value: '乒乓球类', label: '乒乓球类' },
    { value: '健身器材', label: '健身器材' },
    { value: '户外装备', label: '户外装备' },
    { value: '水上器材', label: '水上器材' },
    { value: '其他', label: '其他' }
  ]
  
  // 分页信息
  const pagination = reactive({
    current: 1,
    size: 10,
    total: 0
  })
  
  // 加载状态
  const loading = ref(false)
  
  // 设备数据
  const equipmentData = ref([])
  
  // 表单引用
  const formRef = ref()
  
  // 对话框显示状态
  const editDialogVisible = ref(false)
  
  // 是否为编辑模式
  const isEditMode = ref(false)
  
  // 当前编辑的设备ID
  const currentEquipmentId = ref(null)
  
  // 设备表单
  const equipmentForm = reactive({
    name: '',
    type: '',
    total_quantity: 1,
    available_quantity: 1,
    price: 0,
    location: '',
    status: '正常',
    purchase_date: '',
    description: ''
  })
  
  // 表单验证规则
  const rules = reactive({
    name: [
      { required: true, message: '请输入设备名称', trigger: 'blur' },
      { min: 2, max: 100, message: '长度在2到100个字符', trigger: 'blur' }
    ],
    type: [
      { required: true, message: '请选择设备类型', trigger: 'change' }
    ],
    total_quantity: [
      { required: true, message: '请输入设备总数', trigger: 'blur' },
      { type: 'number', min: 1, message: '数量必须大于0', trigger: 'blur' }
    ],
    available_quantity: [
      { required: true, message: '请输入可租数量', trigger: 'blur' },
      { 
        validator: (rule, value, callback) => {
          if (value > equipmentForm.total_quantity) {
            callback(new Error('可租数量不能大于总数'))
          } else {
            callback()
          }
        },
        trigger: 'blur'
      }
    ],
    price: [
      { required: true, message: '请输入购买单价', trigger: 'blur' },
      { type: 'number', min: 0, message: '价格不能为负数', trigger: 'blur' }
    ],
    location: [
      { required: true, message: '请输入存放位置', trigger: 'blur' }
    ],
    status: [
      { required: true, message: '请选择设备状态', trigger: 'change' }
    ]
  })
  
  // 获取设备列表
  const fetchEquipment = async () => {
    try {
      loading.value = true
      const response = await EquipmentService.getEquipmentList()
      
      if (response.code === 200) {
        equipmentData.value = response.data.map(item => ({
          ...item,
          purchase_date: item.purchase_date ? formatDate(item.purchase_date) : ''
        }))
        pagination.total = response.data.length
      } else {
        ElMessage.error(response.msg || '获取设备列表失败')
      }
    } catch (error) {
      ElMessage.error('获取设备列表失败: ' + error.message)
      console.error(error)
    } finally {
      loading.value = false
    }
  }
  
  // 格式化日期
  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toISOString().split('T')[0]
  }
  
  // 刷新列表
  const refreshList = () => {
    pagination.current = 1
    fetchEquipment()
  }
  
  // 显示新增对话框
  const showAddDialog = () => {
    isEditMode.value = false
    currentEquipmentId.value = null
    resetForm()
    editDialogVisible.value = true
  }
  
  // 显示编辑对话框
  const showEditDialog = (equipment) => {
    isEditMode.value = true
    currentEquipmentId.value = equipment.id
    Object.assign(equipmentForm, {
      ...equipment,
      total_quantity: equipment.total_quantity,
      available_quantity: equipment.available_quantity,
      purchase_date: equipment.purchase_date ? formatDate(equipment.purchase_date) : ''
    })
    editDialogVisible.value = true
  }
  
  // 重置表单
  const resetForm = () => {
    Object.assign(equipmentForm, {
      name: '',
      type: '',
      total_quantity: 1,
      available_quantity: 1,
      price: 0,
      location: '',
      status: '正常',
      purchase_date: '',
      description: ''
    })
  }
  
  // 提交表单
  const submitForm = async () => {
    try {
      await formRef.value.validate()
      
      loading.value = true
      let response
      
      if (isEditMode.value) {
        response = await EquipmentService.updateEquipment(
          currentEquipmentId.value,
          equipmentForm
        )
      } else {
        response = await EquipmentService.addEquipment(equipmentForm)
      }
      
      if (response.code === 200) {
        ElMessage.success(isEditMode.value ? '更新成功' : '添加成功')
        editDialogVisible.value = false
        fetchEquipment()
      } else {
        ElMessage.error(response.msg || '操作失败')
      }
    } catch (error) {
      if (error !== 'validate') {
        ElMessage.error('操作失败: ' + error.message)
        console.error(error)
      }
    } finally {
      loading.value = false
    }
  }
  
  // 删除设备
  const deleteEquipment = (equipment) => {
    ElMessageBox.confirm(`确定要删除设备【${equipment.name}】吗?`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        const response = await EquipmentService.deleteEquipment(equipment.id)
        
        if (response.code === 200) {
          ElMessage.success('删除成功')
          fetchEquipment()
        } else {
          ElMessage.error(response.msg || '删除失败')
        }
      } catch (error) {
        ElMessage.error('删除失败: ' + error.message)
        console.error(error)
      }
    }).catch(() => {})
  }
  
  onMounted(() => {
    fetchEquipment()
  })
  </script>
  
  <style scoped>
  .equipment-management {
    padding: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  </style>