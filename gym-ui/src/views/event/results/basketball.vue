<template>
    <div class="sport-result basketball-result">
      <h3>篮球比赛结果</h3>
      
      <div class="score-board">
        <div class="team">
          <h4>{{ match.team_a.name }}</h4>
          <div class="quarter-scores">
            <div v-for="(score, i) in match.team_a.scores" :key="i" class="quarter">
              <span>第{{ i+1 }}节</span>
              <span class="score">{{ score }}</span>
            </div>
          </div>
          <div class="total-score">
            <span>总分</span>
            <span class="score">{{ totalScoreA }}</span>
          </div>
        </div>
        
        <div class="vs">VS</div>
        
        <div class="team">
          <h4>{{ match.team_b.name }}</h4>
          <div class="quarter-scores">
            <div v-for="(score, i) in match.team_b.scores" :key="i" class="quarter">
              <span>第{{ i+1 }}节</span>
              <span class="score">{{ score }}</span>
            </div>
          </div>
          <div class="total-score">
            <span>总分</span>
            <span class="score">{{ totalScoreB }}</span>
          </div>
        </div>
      </div>
      
      <div class="players">
        <h3>球员数据统计</h3>
        <el-table :data="playerStats" border style="width: 100%">
          <el-table-column prop="name" label="球员" width="120" />
          <el-table-column prop="team" label="队伍" width="100" />
          <el-table-column prop="points" label="得分" width="80" sortable />
          <el-table-column prop="rebounds" label="篮板" width="80" sortable />
          <el-table-column prop="assists" label="助攻" width="80" sortable />
          <el-table-column prop="steals" label="抢断" width="80" sortable />
          <el-table-column prop="blocks" label="盖帽" width="80" sortable />
          <el-table-column prop="turnovers" label="失误" width="80" sortable />
          <el-table-column prop="minutes" label="上场时间" width="100" />
        </el-table>
      </div>
      
      <div class="match-highlights" v-if="highlights.length > 0">
        <h3>比赛精彩瞬间</h3>
        <div class="highlight-list">
          <div v-for="(highlight, index) in highlights" :key="index" class="highlight-item">
            <p><strong>第{{ highlight.time }}分钟</strong>: {{ highlight.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  
  const props = defineProps({
    matchId: {
      type: Number,
      required: true
    }
  })
  
  // 内置伪数据 - 根据matchId获取对应比赛数据
  const match = ref({
    id: props.matchId,
    team_a: { name: '计算机系', scores: [20, 22, 25, 22] },
    team_b: { name: '机械系', scores: [18, 24, 18, 16] }
  })
  
  const playerStats = ref([
    { name: '张三', team: '计算机系', points: 28, rebounds: 10, assists: 5, steals: 2, blocks: 1, turnovers: 3, minutes: '32:15' },
    { name: '李四', team: '计算机系', points: 18, rebounds: 8, assists: 7, steals: 3, blocks: 0, turnovers: 2, minutes: '28:45' },
    { name: '王五', team: '机械系', points: 22, rebounds: 12, assists: 3, steals: 1, blocks: 2, turnovers: 4, minutes: '35:20' },
    { name: '赵六', team: '机械系', points: 16, rebounds: 6, assists: 4, steals: 2, blocks: 1, turnovers: 2, minutes: '30:10' }
  ])
  
  const highlights = ref([
    { time: '5', description: '张三快攻上篮得分' },
    { time: '12', description: '王五三分命中' },
    { time: '28', description: '李四抢断后助攻张三扣篮' },
    { time: '42', description: '赵六关键三分追平比分' }
  ])
  
  const totalScoreA = computed(() => {
    return match.value.team_a.scores.reduce((sum, score) => sum + score, 0)
  })
  
  const totalScoreB = computed(() => {
    return match.value.team_b.scores.reduce((sum, score) => sum + score, 0)
  })
  </script>
  
  <style scoped>
  .basketball-result {
    margin-top: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .score-board {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 20px 0;
    padding: 15px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .team {
    text-align: center;
    flex: 1;
  }
  
  .quarter-scores {
    display: flex;
    justify-content: center;
    margin: 15px 0;
  }
  
  .quarter {
    margin: 0 10px;
    display: flex;
    flex-direction: column;
  }
  
  .quarter span.score {
    font-weight: bold;
    font-size: 1.2em;
  }
  
  .total-score {
    margin-top: 10px;
    font-size: 1.2em;
  }
  
  .total-score .score {
    font-weight: bold;
    font-size: 1.5em;
    color: #409eff;
  }
  
  .vs {
    font-size: 1.5em;
    font-weight: bold;
    margin: 0 20px;
  }
  
  .players {
    margin-top: 30px;
  }
  
  .match-highlights {
    margin-top: 30px;
  }
  
  .highlight-item {
    padding: 10px;
    margin: 5px 0;
    background-color: #fff;
    border-left: 4px solid #409eff;
  }
  </style>