<template>
    <div class="sport-result badminton-result">
      <h3>羽毛球比赛结果</h3>
      
      <div class="match-header">
        <div class="player player1">
          <el-avatar :size="80" :src="match.player1.avatar" />
          <h4>{{ match.player1.name }}</h4>
          <div class="team">{{ match.player1.team }}</div>
        </div>
        
        <div class="score">
          <div class="final-score">{{ match.player1.score }} : {{ match.player2.score }}</div>
          <div class="match-type">{{ match.type }}</div>
        </div>
        
        <div class="player player2">
          <el-avatar :size="80" :src="match.player2.avatar" />
          <h4>{{ match.player2.name }}</h4>
          <div class="team">{{ match.player2.team }}</div>
        </div>
      </div>
      
      <div class="game-results">
        <h3>各局比分</h3>
        <el-table :data="gameResults" style="width: 100%" border>
          <el-table-column label="局数" width="80">
            <template #default="{ $index }">
              第{{ $index + 1 }}局
            </template>
          </el-table-column>
          <el-table-column label="比分" width="120">
            <template #default="{ row }">
              {{ row.player1 }} : {{ row.player2 }}
            </template>
          </el-table-column>
          <el-table-column label="持续时间" width="120" prop="duration" />
          <el-table-column label="获胜方">
            <template #default="{ row }">
              <span :class="row.winner === match.player1.name ? 'winner' : ''">
                {{ row.winner }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <div class="match-stats">
        <h3>比赛统计</h3>
        <div class="stats-container">
          <div class="player-stats player1-stats">
            <h4>{{ match.player1.name }}</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ stats.player1.smashes }}</div>
                <div class="stat-label">杀球</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.player1.netPoints }}</div>
                <div class="stat-label">网前得分</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.player1.servicePoints }}</div>
                <div class="stat-label">发球得分</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.player1.errors }}</div>
                <div class="stat-label">失误</div>
              </div>
            </div>
          </div>
          
          <div class="player-stats player2-stats">
            <h4>{{ match.player2.name }}</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ stats.player2.smashes }}</div>
                <div class="stat-label">杀球</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.player2.netPoints }}</div>
                <div class="stat-label">网前得分</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.player2.servicePoints }}</div>
                <div class="stat-label">发球得分</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.player2.errors }}</div>
                <div class="stat-label">失误</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="key-points" v-if="keyPoints.length > 0">
        <h3>关键分记录</h3>
        <el-timeline>
          <el-timeline-item
            v-for="(point, index) in keyPoints"
            :key="index"
            :timestamp="'第' + point.game + '局 ' + point.score"
            placement="top"
          >
            <el-card>
              <p>{{ point.description }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const props = defineProps({
    matchId: {
      type: Number,
      required: true
    }
  })
  
  // 内置伪数据
  const match = ref({
    id: props.matchId,
    player1: {
      name: '张三',
      team: '计算机系',
      avatar: 'https://via.placeholder.com/80',
      score: 2
    },
    player2: {
      name: '李四',
      team: '电子工程系',
      avatar: 'https://via.placeholder.com/80',
      score: 1
    },
    type: '男子单打',
    duration: '45分钟'
  })
  
  const gameResults = ref([
    { player1: 21, player2: 15, winner: '张三', duration: '12分钟' },
    { player1: 18, player2: 21, winner: '李四', duration: '15分钟' },
    { player1: 21, player2: 14, winner: '张三', duration: '18分钟' }
  ])
  
  const stats = ref({
    player1: {
      smashes: 15,
      netPoints: 8,
      servicePoints: 5,
      errors: 12
    },
    player2: {
      smashes: 12,
      netPoints: 6,
      servicePoints: 4,
      errors: 15
    }
  })
  
  const keyPoints = ref([
    { game: 1, score: '18:14', description: '张三连续3记杀球得分' },
    { game: 2, score: '19:19', description: '李四网前假动作得分' },
    { game: 3, score: '14:14', description: '张三连续5分锁定胜局' }
  ])
  </script>
  
  <style scoped>
  .badminton-result {
    margin-top: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .match-header {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .player {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
  }
  
  .player h4 {
    margin: 10px 0 5px;
    font-size: 1.2em;
  }
  
  .team {
    color: #666;
    font-size: 0.9em;
  }
  
  .score {
    text-align: center;
    margin: 0 20px;
  }
  
  .final-score {
    font-size: 2em;
    font-weight: bold;
    color: #409eff;
  }
  
  .match-type {
    color: #666;
    font-size: 0.9em;
    margin-top: 5px;
  }
  
  .game-results {
    margin: 30px 0;
  }
  
  .winner {
    font-weight: bold;
    color: #67c23a;
  }
  
  .match-stats {
    margin: 30px 0;
  }
  
  .stats-container {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .player-stats {
    flex: 1;
    padding: 15px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .player-stats h4 {
    text-align: center;
    margin-bottom: 15px;
    color: #409eff;
  }
  
  .player1-stats {
    margin-right: 15px;
  }
  
  .player2-stats {
    margin-left: 15px;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .stat-item {
    text-align: center;
    padding: 10px;
  }
  
  .stat-value {
    font-size: 1.5em;
    font-weight: bold;
  }
  
  .stat-label {
    color: #666;
    font-size: 0.9em;
  }
  
  .key-points {
    margin-top: 30px;
  }
  </style>