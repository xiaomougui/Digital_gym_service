<template>
    <div class="feedback-container">
      <div class="header">
        <h1 class="title">用户反馈</h1>
        <div class="filter-section">
          <el-input
            v-model="dateFilter"
            placeholder="筛选日期 (YYYY-MM-DD)"
            clearable
            @keyup.enter="filterFeedbacks"
            style="width: 240px; margin-right: 10px;"
          />
          <el-button type="primary" @click="filterFeedbacks">筛选</el-button>
        </div>
      </div>
  
      <div class="feedback-list">
        <div 
          v-for="(feedback, index) in filteredFeedbacks" 
          :key="index" 
          class="feedback-card"
          :class="{ 'solved': feedback.solved, 'unsolved': !feedback.solved }"
          @click="showReason(feedback)"
        >
          <div class="card-content">
            <div class="message">{{ feedback.message }}</div>
            <div class="meta">
              <span class="date">{{ formatDate(feedback.created_at) }}</span>
              <el-tag 
                :type="feedback.solved ? 'success' : 'warning'" 
                size="small"
                class="status-tag"
              >
                {{ feedback.solved ? '已解决' : '待处理' }}
              </el-tag>
            </div>
          </div>
          <div class="status-icon" @click.stop="showStatusDialog(feedback)">
            <el-icon :size="20" :color="feedback.solved ? '#67C23A' : '#E6A23C'">
              <component :is="feedback.solved ? Check : Close" />
            </el-icon>
          </div>
        </div>
      </div>
  
      <!-- 反馈详情对话框 -->
      <el-dialog 
        v-model="detailDialogVisible" 
        :title="`反馈详情 - ${currentFeedback.solved ? '已解决' : '待处理'}`"
        width="500px"
      >
        <div class="reason-content">
          {{ currentFeedback.reason || '暂无处理原因' }}
        </div>
        <template #footer>
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </template>
      </el-dialog>
  
      <!-- 状态修改对话框 -->
      <el-dialog 
        v-model="statusDialogVisible" 
        :title="`标记为 ${currentFeedback.solved ? '未解决' : '已解决'}`"
        width="500px"
      >
        <el-form :model="statusForm" label-width="80px">
          <el-form-item label="处理原因">
            <el-input
              v-model="statusForm.reason"
              type="textarea"
              :rows="4"
              placeholder="请输入处理原因"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="statusDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmStatusChange">确认</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { Check, Close } from '@element-plus/icons-vue';
  import FeedbackService from '@/api/feedback/index';
  import { ElMessage } from 'element-plus';
  
  // 数据状态
  const dateFilter = ref('');
  const feedbacks = ref([]);
  const detailDialogVisible = ref(false);
  const statusDialogVisible = ref(false);
  const currentFeedback = ref({});
  const statusForm = ref({
    reason: ''
  });
  const loading = ref(false);
  
  // 格式化日期
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
  };
  
  // 获取反馈列表
  const fetchFeedbacks = async () => {
    try {
      loading.value = true;
      const response = await FeedbackService.getAllFeedbacks();
      if (response.code === 200) {
        feedbacks.value = response.data;
      } else {
        ElMessage.error(response.msg || '获取反馈列表失败');
      }
    } catch (error) {
      ElMessage.error('网络错误，请稍后重试');
      console.error(error);
    } finally {
      loading.value = false;
    }
  };
  
  // 筛选反馈
  const filteredFeedbacks = computed(() => {
    if (!dateFilter.value) return feedbacks.value;
    return feedbacks.value.filter(feedback => 
      formatDate(feedback.created_at) === dateFilter.value
    );
  });
  
  const filterFeedbacks = () => {
    // 计算属性会自动更新
  };
  
  // 显示反馈详情
  const showReason = (feedback) => {
    currentFeedback.value = feedback;
    detailDialogVisible.value = true;
  };
  
  // 显示状态修改对话框
  const showStatusDialog = (feedback) => {
    currentFeedback.value = feedback;
    statusForm.value.reason = feedback.reason || '';
    statusDialogVisible.value = true;
  };
  
  // 确认状态修改
  const confirmStatusChange = async () => {
    try {
      loading.value = true;
      const response = await FeedbackService.handleFeedback(
        currentFeedback.value.id,
        !currentFeedback.value.solved,
        statusForm.value.reason
      );
      
      if (response.code === 200) {
        ElMessage.success('反馈状态已更新');
        // 更新本地数据
        const index = feedbacks.value.findIndex(f => f.id === currentFeedback.value.id);
        if (index !== -1) {
          feedbacks.value[index].solved = !currentFeedback.value.solved;
          feedbacks.value[index].reason = statusForm.value.reason;
        }
        statusDialogVisible.value = false;
      } else {
        ElMessage.error(response.msg || '更新反馈状态失败');
      }
    } catch (error) {
      ElMessage.error('网络错误，请稍后重试');
      console.error(error);
    } finally {
      loading.value = false;
    }
  };
  
  // 初始化加载数据
  onMounted(() => {
    fetchFeedbacks();
  });
  </script>
  
  <style scoped>
  .feedback-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .title {
    color: #303133;
    font-size: 24px;
    margin: 0;
  }
  
  .filter-section {
    display: flex;
    align-items: center;
  }
  
  .feedback-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .feedback-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-radius: 8px;
    background-color: #ffffff;
    box-shadow: 0 1px 8px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .feedback-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  }
  
  .solved {
    border-left: 4px solid #67C23A;
  }
  
  .unsolved {
    border-left: 4px solid #E6A23C;
  }
  
  .card-content {
    flex: 1;
  }
  
  .message {
    font-size: 16px;
    color: #303133;
    margin-bottom: 8px;
  }
  
  .meta {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .date {
    font-size: 13px;
    color: #909399;
  }
  
  .status-tag {
    margin-left: 8px;
  }
  
  .status-icon {
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.2s;
  }
  
  .status-icon:hover {
    background-color: rgba(0, 0, 0, 0.04);
  }
  
  .reason-content {
    padding: 16px;
    background-color: #f5f7fa;
    border-radius: 4px;
    line-height: 1.6;
  }
  </style>