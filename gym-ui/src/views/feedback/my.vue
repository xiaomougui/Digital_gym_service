<template>
    <div class="feedback-container">
      <!-- 创建反馈表单 -->
      <el-card class="feedback-form" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>创建新反馈</span>
          </div>
        </template>
        
        <el-form :model="feedbackForm" :rules="rules" ref="formRef">
          <el-form-item prop="content">
            <el-input
              v-model="feedbackForm.content"
              type="textarea"
              :rows="4"
              placeholder="请输入您的反馈内容"
              resize="none"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitFeedback">提交反馈</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
  
      <!-- 反馈列表 -->
      <el-card class="feedback-list" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>我的反馈记录</span>
            <el-button type="primary" size="small" @click="refreshList" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </template>
        
        <el-table
          :data="feedbackList"
          v-loading="loading"
          style="width: 100%"
          stripe
          border
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="message" label="反馈内容" show-overflow-tooltip />
          <el-table-column prop="date" label="提交时间" width="180">
            <template #default="{row}">
              {{ formatDate(row.date) }}
            </template>
          </el-table-column>
          <el-table-column label="处理状态" width="120">
            <template #default="{row}">
              <el-tag :type="row.solved ? 'success' : 'warning'">
                {{ row.solved ? '已处理' : '未处理' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="处理结果" width="180">
            <template #default="{row}">
              {{ row.reason || '暂无处理结果' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="{row}">
              <el-button size="small" @click="viewDetail(row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination">
          <el-pagination
            v-model:current-page="pagination.current"
            v-model:page-size="pagination.size"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="fetchFeedbackList"
            @current-change="fetchFeedbackList"
          />
        </div>
      </el-card>
      
      <!-- 反馈详情对话框 -->
      <el-dialog v-model="detailVisible" :title="`反馈详情 - ID: ${currentFeedback.id}`" width="50%">
        <div class="feedback-detail">
          <div class="detail-item">
            <label>反馈内容：</label>
            <div class="detail-content">{{ currentFeedback.message }}</div>
          </div>
          <div class="detail-item">
            <label>提交时间：</label>
            <div class="detail-content">{{ formatDate(currentFeedback.date) }}</div>
          </div>
          <div class="detail-item">
            <label>处理状态：</label>
            <div class="detail-content">
              <el-tag :type="currentFeedback.solved ? 'success' : 'warning'">
                {{ currentFeedback.solved ? '已处理' : '未处理' }}
              </el-tag>
            </div>
          </div>
          <div class="detail-item" v-if="currentFeedback.reason">
            <label>处理结果：</label>
            <div class="detail-content">{{ currentFeedback.reason }}</div>
          </div>
        </div>
        <template #footer>
          <el-button @click="detailVisible = false">关闭</el-button>
        </template>
      </el-dialog>
    </div>
</template>
  
<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  import { Refresh } from '@element-plus/icons-vue'
  import FeedbackService from '@/api/feedback/index';
  import { useAuthStore } from '@/stores/auth'
  
  const authStore = useAuthStore()
  
  // 反馈表单数据
  const feedbackForm = reactive({
    content: ''
  })
  
  // 表单验证规则
  const rules = reactive({
    content: [
      { required: true, message: '请输入反馈内容', trigger: 'blur' },
      { min: 5, max: 1000, message: '长度在5到1000个字符', trigger: 'blur' }
    ]
  })
  
  // 反馈列表数据
  const feedbackList = ref([])
  const loading = ref(false)
  const pagination = reactive({
    current: 1,
    size: 10,
    total: 0
  })
  
  // 详情对话框
  const detailVisible = ref(false)
  const currentFeedback = ref({})
  
  // 表单引用
  const formRef = ref()
  
  // 格式化日期
  const formatDate = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleString()
  }
  
  // 提交反馈
  const submitFeedback = async () => {
    try {
      await formRef.value.validate()
      
      loading.value = true
      const response = await FeedbackService.createFeedback(
        authStore.user.id,
        feedbackForm.content
      )
      
      if (response.code === 200) {
        ElMessage.success('反馈提交成功！')
        formRef.value.resetFields()
        // 刷新列表
        refreshList()
      } else {
        ElMessage.error(response.msg || '提交反馈失败')
      }
    } catch (error) {
      if (error !== 'validate') {
        ElMessage.error('提交失败：' + (error.message || '未知错误'))
      }
    } finally {
      loading.value = false
    }
  }
  
  // 重置表单
  const resetForm = () => {
    formRef.value.resetFields()
  }
  
  // 查看详情
  const viewDetail = (feedback) => {
    currentFeedback.value = feedback
    detailVisible.value = true
  }
  
  // 获取反馈列表
  const fetchFeedbackList = async () => {
    try {
      loading.value = true
      
      const response = await FeedbackService.getMyFeedbacks(authStore.user.id)
      
      if (response.code === 200) {
        feedbackList.value = response.data
        pagination.total = response.data.length
      } else {
        ElMessage.error(response.msg || '获取反馈列表失败')
      }
    } catch (error) {
      ElMessage.error('获取反馈列表失败：' + error.message)
    } finally {
      loading.value = false
    }
  }
  
  // 刷新列表
  const refreshList = () => {
    pagination.current = 1
    fetchFeedbackList()
  }
  
  // 初始化加载
  onMounted(() => {
    fetchFeedbackList()
  })
  </script>
  
  <style scoped>
  .feedback-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .feedback-form {
    margin-bottom: 20px;
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
  
  .feedback-detail {
    padding: 10px;
  }
  
  .detail-item {
    margin-bottom: 15px;
  }
  
  .detail-item label {
    font-weight: bold;
    color: #606266;
    display: inline-block;
    width: 80px;
    vertical-align: top;
  }
  
  .detail-item .detail-content {
    display: inline-block;
    width: calc(100% - 90px);
    word-break: break-word;
  }
  </style>