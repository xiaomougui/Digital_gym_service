<template>
    <div class="sport-result table-tennis-result">
      <h3>乒乓球比赛结果</h3>
      
      <div class="player-info">
        <div class="player player1">
          <el-avatar :size="80" :src="match.player1.avatar" />
          <h4>{{ match.player1.name }}</h4>
          <div class="team">{{ match.player1.team }}</div>
        </div>
        
        <div class="vs">
          <div class="score">{{ match.player1.score }} : {{ match.player2.score }}</div>
        </div>
        
        <div class="player player2">
          <el-avatar :size="80" :src="match.player2.avatar" />
          <h4>{{ match.player2.name }}</h4>
          <div class="team">{{ match.player2.team }}</div>
        </div>
      </div>
      
      <div class="game-details">
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
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalPoints }}</div>
            <div class="stat-label">总得分</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.longestRally }}</div>
            <div class="stat-label">最长回合</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.aces }}</div>
            <div class="stat-label">发球得分</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.serviceErrors }}</div>
            <div class="stat-label">发球失误</div>
          </div>
        </div>
      </div>
      
      <div class="key-moments" v-if="keyMoments.length > 0">
        <h3>关键回合</h3>
        <el-timeline>
          <el-timeline-item
            v-for="(moment, index) in keyMoments"
            :key="index"
            :timestamp="'第' + moment.game + '局 ' + moment.score + '分'"
            placement="top"
          >
            <el-card>
              <p>{{ moment.description }}</p>
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
      score: 3
    },
    player2: {
      name: '李四',
      team: '电子工程系',
      avatar: 'https://via.placeholder.com/80',
      score: 1
    }
  })
  
  const gameResults = ref([
    { player1: 11, player2: 8, winner: '张三' },
    { player1: 9, player2: 11, winner: '李四' },
    { player1: 11, player2: 6, winner: '张三' },
    { player1: 11, player2: 9, winner: '张三' }
  ])
  
  const stats = ref({
    totalPoints: 76,
    longestRally: '22拍',
    aces: 7,
    serviceErrors: 5
  })
  
  const keyMoments = ref([
    { game: 1, score: '9:7', description: '张三连续3个正手进攻得分' },
    { game: 2, score: '8:10', description: '李四反手拧拉得分挽救局点' },
    { game: 3, score: '6:6', description: '张三发球抢攻连得3分' },
    { game: 4, score: '9:9', description: '李四反手失误送赛点' }
  ])
  </script>
  
  <style scoped>
  .table-tennis-result {
    margin-top: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .player-info {
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
  
  .vs {
    margin: 0 20px;
    text-align: center;
  }
  
  .vs .score {
    font-size: 2em;
    font-weight: bold;
    color: #409eff;
  }
  
  .game-details {
    margin: 30px 0;
  }
  
  .winner {
    font-weight: bold;
    color: #67c23a;
  }
  
  .match-stats {
    margin: 30px 0;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-top: 20px;
  }
  
  .stat-item {
    background-color: #fff;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .stat-value {
    font-size: 1.8em;
    font-weight: bold;
    color: #409eff;
  }
  
  .stat-label {
    color: #666;
    font-size: 0.9em;
  }
  
  .key-moments {
    margin-top: 30px;
  }
  </style>