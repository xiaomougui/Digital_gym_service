<template>
    <div class="match-manage">
      <el-card shadow="hover">
        <div class="header">
          <h2>赛事管理</h2>
          <div class="actions">
            <el-button type="primary" @click="showCreateDialog">创建赛事</el-button>
            <el-input
              v-model="searchQuery"
              placeholder="搜索赛事..."
              style="width: 300px"
              clearable
              @clear="filterMatches"
              @keyup.enter="filterMatches"
            >
              <template #append>
                <el-button @click="filterMatches">
                  <el-icon><search /></el-icon>
                </el-button>
              </template>
            </el-input>
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
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{row}">
              <el-tag :type="getStatusTag(row.status)">{{ getStatusName(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="participants_count" label="报名人数" width="120" />
          <el-table-column label="操作" width="250">
            <template #default="{row}">
              <el-button size="small" @click="viewDetail(row)">查看</el-button>
              <el-button 
                size="small" 
                type="primary" 
                @click="editMatch(row)"
                :disabled="row.status !== 'pending'"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="deleteMatch(row)"
                :disabled="row.status === 'ongoing'"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
  
      <!-- 创建赛事对话框 -->
      <el-dialog v-model="createDialogVisible" title="创建赛事" width="50%">
        <el-form :model="createForm" :rules="rules" ref="createFormRef" label-width="120px">
          <el-form-item label="赛事名称" prop="name">
            <el-input v-model="createForm.name" placeholder="请输入赛事名称" />
          </el-form-item>
          
          <el-form-item label="赛事类型" prop="type">
            <el-select v-model="createForm.type" placeholder="请选择赛事类型">
              <el-option
                v-for="type in matchTypeOptions"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="开始时间" prop="start_time">
            <el-date-picker
              v-model="createForm.start_time"
              type="datetime"
              placeholder="选择开始时间"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
          
          <el-form-item label="结束时间" prop="end_time">
            <el-date-picker
              v-model="createForm.end_time"
              type="datetime"
              placeholder="选择结束时间"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
          
          <el-form-item label="最大参赛人数" prop="max_participants">
            <el-input-number v-model="createForm.max_participants" :min="2" :max="1000" />
          </el-form-item>
          
          <el-form-item label="赛事描述" prop="description">
            <el-input
              v-model="createForm.description"
              type="textarea"
              :rows="3"
              placeholder="请输入赛事描述"
            />
          </el-form-item>
          
          <el-form-item label="赛事规则" prop="rules">
            <el-input
              v-model="createForm.rules"
              type="textarea"
              :rows="3"
              placeholder="请输入赛事规则"
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="createDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitCreateForm">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { Search } from '@element-plus/icons-vue'
  
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
      participants_count: 0,
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
      status: 'pending',
      participants_count: 0,
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
      status: 'ongoing',
      participants_count: 15,
      max_participants: 32,
      description: '个人单打比赛',
      rules: '单淘汰制，每局11分'
    }
  ]
  
  const matches = ref([...mockMatches])
  const loading = ref(false)
  const searchQuery = ref('')
  const createDialogVisible = ref(false)
  const createFormRef = ref(null)
  
  const createForm = reactive({
    name: '',
    type: '',
    start_time: '',
    end_time: '',
    max_participants: 100,
    description: '',
    rules: ''
  })
  
  const rules = reactive({
    name: [{ required: true, message: '请输入赛事名称', trigger: 'blur' }],
    type: [{ required: true, message: '请选择赛事类型', trigger: 'change' }],
    start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
    end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
    max_participants: [{ required: true, message: '请输入最大参赛人数', trigger: 'blur' }]
  })
  
  const matchTypeOptions = [
    { value: 'basketball', label: '篮球' },
    { value: 'football', label: '足球' },
    { value: 'table_tennis', label: '乒乓球' },
    { value: 'badminton', label: '羽毛球' }
  ]
  
  const statusTypes = {
    pending: { name: '未开始', tag: 'info' },
    ongoing: { name: '进行中', tag: 'warning' },
    completed: { name: '已结束', tag: 'success' },
    cancelled: { name: '已取消', tag: 'danger' }
  }
  
  const getMatchTypeName = (type) => {
    const found = matchTypeOptions.find(t => t.value === type)
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
  
  const getStatusName = (status) => statusTypes[status]?.name || status
  const getStatusTag = (status) => statusTypes[status]?.tag || ''
  
  const filteredMatches = computed(() => {
    return matches.value.filter(match => 
      match.name.includes(searchQuery.value)
    )
  })
  
  const showCreateDialog = () => {
    createDialogVisible.value = true
  }
  
  const submitCreateForm = async () => {
    try {
      await createFormRef.value.validate()
      
      const newMatch = {
        id: matches.value.length + 1,
        ...createForm,
        status: 'pending',
        participants_count: 0
      }
      
      matches.value.unshift(newMatch)
      ElMessage.success('赛事创建成功')
      createDialogVisible.value = false
      resetCreateForm()
    } catch (error) {
      console.error(error)
    }
  }
  
  const resetCreateForm = () => {
    createFormRef.value?.resetFields()
    Object.assign(createForm, {
      name: '',
      type: '',
      start_time: '',
      end_time: '',
      max_participants: 100,
      description: '',
      rules: ''
    })
  }
  
  const viewDetail = (match) => {
    router.push(`/event/details/${match.id}`)
  }
  
  const editMatch = (match) => {
    ElMessage.info('编辑功能将在后续版本开放')
  }
  
  const deleteMatch = async (match) => {
    try {
      await ElMessageBox.confirm(`确定要删除赛事 "${match.name}" 吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      const index = matches.value.findIndex(m => m.id === match.id)
      if (index !== -1) {
        matches.value.splice(index, 1)
        ElMessage.success('删除成功')
      }
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
      }
    }
  }
  
  const filterMatches = () => {
    // 搜索功能已通过计算属性实现
  }
  </script>
  
  <style scoped>
  .match-manage {
    padding: 20px;
  }
  
  .header {
    margin-bottom: 20px;
  }
  
  .actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
  }
  </style>