<template>
    <div class="sport-result football-result">
      <h3>足球比赛结果</h3>
      
      <div class="match-summary">
        <div class="teams">
          <div class="team home-team">
            <h4>{{ match.home_team.name }}</h4>
            <div class="team-logo">
              <el-avatar :size="60" :src="match.home_team.logo" />
            </div>
            <div class="score">{{ match.home_team.score }}</div>
          </div>
          
          <div class="vs">VS</div>
          
          <div class="team away-team">
            <h4>{{ match.away_team.name }}</h4>
            <div class="team-logo">
              <el-avatar :size="60" :src="match.away_team.logo" />
            </div>
            <div class="score">{{ match.away_team.score }}</div>
          </div>
        </div>
        
        <div class="match-info">
          <div class="info-item">
            <span class="label">比赛时间:</span>
            <span class="value">{{ match.match_time }}</span>
          </div>
          <div class="info-item">
            <span class="label">比赛地点:</span>
            <span class="value">{{ match.location }}</span>
          </div>
          <div class="info-item">
            <span class="label">裁判:</span>
            <span class="value">{{ match.referee }}</span>
          </div>
        </div>
      </div>
      
      <div class="match-details">
        <el-tabs type="border-card">
          <el-tab-pane label="进球记录">
            <el-table :data="goals" style="width: 100%">
              <el-table-column prop="time" label="时间" width="100" />
              <el-table-column prop="player" label="球员" width="120" />
              <el-table-column prop="team" label="球队" width="120" />
              <el-table-column prop="type" label="进球类型" width="120" />
              <el-table-column prop="assist" label="助攻" width="120" />
              <el-table-column prop="description" label="描述" />
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="球员统计">
            <el-table :data="playerStats" style="width: 100%">
              <el-table-column prop="name" label="球员" width="120" />
              <el-table-column prop="team" label="球队" width="100" />
              <el-table-column prop="position" label="位置" width="100" />
              <el-table-column prop="goals" label="进球" width="80" sortable />
              <el-table-column prop="assists" label="助攻" width="80" sortable />
              <el-table-column prop="shots" label="射门" width="80" sortable />
              <el-table-column prop="shots_on_target" label="射正" width="80" sortable />
              <el-table-column prop="passes" label="传球" width="80" sortable />
              <el-table-column prop="pass_accuracy" label="传球成功率" width="120" sortable />
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="比赛事件">
            <el-timeline>
              <el-timeline-item
                v-for="(event, index) in matchEvents"
                :key="index"
                :timestamp="event.time + '分钟'"
                placement="top"
              >
                <el-card>
                  <p>{{ event.description }}</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-tab-pane>
        </el-tabs>
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
    home_team: {
      name: '计算机系',
      logo: 'https://via.placeholder.com/60',
      score: 3
    },
    away_team: {
      name: '电子工程系',
      logo: 'https://via.placeholder.com/60',
      score: 2
    },
    match_time: '2023-09-15 14:00:00',
    location: '学校足球场',
    referee: '王老师'
  })
  
  const goals = ref([
    { time: '23', player: '张三', team: '计算机系', type: '运动战', assist: '李四', description: '禁区外远射破门' },
    { time: '45+1', player: '王五', team: '电子工程系', type: '点球', assist: '', description: '点球罚进右下角' },
    { time: '56', player: '李四', team: '计算机系', type: '头球', assist: '赵六', description: '角球头球破门' },
    { time: '78', player: '张三', team: '计算机系', type: '单刀', assist: '钱七', description: '反越位成功单刀破门' },
    { time: '89', player: '孙八', team: '电子工程系', type: '直接任意球', assist: '', description: '25米任意球直接破门' }
  ])
  
  const playerStats = ref([
    { name: '张三', team: '计算机系', position: '前锋', goals: 2, assists: 0, shots: 5, shots_on_target: 3, passes: 32, pass_accuracy: '78%' },
    { name: '李四', team: '计算机系', position: '中场', goals: 1, assists: 1, shots: 3, shots_on_target: 2, passes: 45, pass_accuracy: '85%' },
    { name: '王五', team: '电子工程系', position: '前锋', goals: 1, assists: 0, shots: 4, shots_on_target: 2, passes: 28, pass_accuracy: '75%' },
    { name: '孙八', team: '电子工程系', position: '中场', goals: 1, assists: 0, shots: 2, shots_on_target: 1, passes: 38, pass_accuracy: '82%' }
  ])
  
  const matchEvents = ref([
    { time: '23', description: '计算机系 张三 进球 1-0' },
    { time: '45+1', description: '电子工程系 王五 点球破门 1-1' },
    { time: '56', description: '计算机系 李四 头球破门 2-1' },
    { time: '65', description: '计算机系 赵六 黄牌警告' },
    { time: '78', description: '计算机系 张三 进球 3-1' },
    { time: '89', description: '电子工程系 孙八 任意球破门 3-2' }
  ])
  </script>
  
  <style scoped>
  .football-result {
    margin-top: 30px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .match-summary {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .teams {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .team {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
  }
  
  .team h4 {
    margin-bottom: 10px;
  }
  
  .team-logo {
    margin: 10px 0;
  }
  
  .team .score {
    font-size: 2em;
    font-weight: bold;
    color: #409eff;
  }
  
  .vs {
    margin: 0 30px;
    font-size: 1.5em;
    font-weight: bold;
  }
  
  .match-info {
    width: 100%;
    max-width: 500px;
    background-color: #fff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .info-item {
    display: flex;
    margin-bottom: 10px;
  }
  
  .info-item .label {
    font-weight: bold;
    width: 80px;
  }
  
  .match-details {
    margin-top: 20px;
  }
  </style>