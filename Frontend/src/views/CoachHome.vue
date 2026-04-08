<template>
  <div class="coach-home">
    <header class="header">
      <h1>教练首页</h1>
      <button @click="goToProfile" class="profile-btn">个人中心</button>
    </header>
    
    <div class="quick-links">
      <button @click="showTodaySchedules" class="quick-link-btn">今日已确认课程</button>
      <button @click="showTomorrowSchedules" class="quick-link-btn">明日已确认课程</button>
      <button @click="showAddSchedule" class="quick-link-btn">添加排课</button>
    </div>
    
    <div v-if="showAddForm" class="add-schedule-form">
      <h2>添加排课</h2>
      <form @submit.prevent="addSchedule">
        <div class="form-group">
          <label for="date">日期</label>
          <input type="date" id="date" v-model="newSchedule.date" required />
        </div>
        <div class="form-group">
          <label for="time">时段</label>
          <select id="time" v-model="newSchedule.time" required>
            <option value="上午">上午</option>
            <option value="下午">下午</option>
            <option value="晚上">晚上</option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit" class="submit-btn">保存</button>
          <button type="button" @click="showAddForm = false" class="cancel-btn">取消</button>
        </div>
      </form>
    </div>
    
    <div class="schedule-list">
      <h2>我的排课</h2>
      <div v-if="schedules.length === 0" class="empty-state">
        <p>暂无排课</p>
      </div>
      <div v-for="schedule in schedules" :key="schedule.id" class="schedule-item">
        <div class="schedule-info">
          <h3>{{ schedule.schedule_date }}</h3>
          <p>时段: {{ schedule.schedule_time }}</p>
          <p>学员: {{ schedule.student_name || '未预约' }}</p>
          <p>状态: {{ schedule.status }}</p>
        </div>
        <div class="schedule-actions">
          <button 
            @click="confirmSchedule(schedule.id)" 
            class="confirm-btn"
            :disabled="schedule.status !== '待确认'"
          >
            确认
          </button>
          <button 
            @click="completeSchedule(schedule.id)" 
            class="complete-btn"
            :disabled="schedule.status !== '已确认'"
          >
            完成
          </button>
          <button 
            @click="deleteSchedule(schedule.id)" 
            class="delete-btn"
            :disabled="schedule.status !== '待确认'"
          >
            删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import request from '../utils/request'

const router = useRouter()
const userStore = useUserStore()

const schedules = ref([])
const showAddForm = ref(false)
const newSchedule = ref({
  date: '',
  time: '上午'
})

const goToProfile = () => {
  router.push('/profile')
}

const showTodaySchedules = () => {
  const today = new Date().toISOString().split('T')[0]
  filterSchedules(today)
}

const showTomorrowSchedules = () => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const tomorrowStr = tomorrow.toISOString().split('T')[0]
  filterSchedules(tomorrowStr)
}

const showAddSchedule = () => {
  showAddForm.value = true
}

const getSchedules = async () => {
  try {
    const response = await request({
      url: `/schedules/coach/${userStore.userInfo.id}`,
      method: 'get'
    })
    
    if (response.success) {
      schedules.value = response.data.schedules
    }
  } catch (error) {
    console.error('获取排课失败:', error)
  }
}

const filterSchedules = (date) => {
  // 过滤指定日期的已确认课程
  const filtered = schedules.value.filter(schedule => 
    schedule.schedule_date === date && schedule.status === '已确认'
  )
  schedules.value = filtered
}

const addSchedule = async () => {
  try {
    const response = await request({
      url: '/schedules',
      method: 'post',
      data: {
        coach_id: userStore.userInfo.id,
        schedule_date: newSchedule.value.date,
        schedule_time: newSchedule.value.time
      }
    })
    
    if (response.success) {
      alert('排课添加成功')
      showAddForm.value = false
      newSchedule.value = {
        date: '',
        time: '上午'
      }
      getSchedules()
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('添加排课失败:', error)
    alert('添加失败')
  }
}

const confirmSchedule = async (scheduleId) => {
  if (confirm('确定要确认该课程吗？')) {
    try {
      const response = await request({
        url: `/schedules/${scheduleId}/confirm`,
        method: 'put'
      })
      
      if (response.success) {
        alert('确认成功')
        getSchedules()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('确认课程失败:', error)
      alert('确认失败')
    }
  }
}

const completeSchedule = async (scheduleId) => {
  if (confirm('确定要标记该课程为完成吗？')) {
    try {
      const response = await request({
        url: `/schedules/${scheduleId}/complete`,
        method: 'put'
      })
      
      if (response.success) {
        alert('标记成功')
        getSchedules()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('标记课程完成失败:', error)
      alert('标记失败')
    }
  }
}

const deleteSchedule = async (scheduleId) => {
  if (confirm('确定要删除该排课吗？')) {
    try {
      const response = await request({
        url: `/schedules/${scheduleId}`,
        method: 'delete'
      })
      
      if (response.success) {
        alert('删除成功')
        getSchedules()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('删除排课失败:', error)
      alert('删除失败')
    }
  }
}

onMounted(() => {
  getSchedules()
})
</script>

<style scoped>
.coach-home {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.header h1 {
  margin: 0;
  color: #333;
}

.profile-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.quick-links {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.quick-link-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.quick-link-btn:hover {
  background-color: #359469;
}

.add-schedule-form {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.add-schedule-form h2 {
  margin-bottom: 1rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #666;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.submit-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  padding: 0.5rem 1rem;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.schedule-list h2 {
  margin-bottom: 1rem;
  color: #333;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.schedule-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.schedule-info p {
  margin: 0.25rem 0;
  color: #666;
}

.schedule-actions {
  display: flex;
  gap: 0.5rem;
}

.confirm-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.complete-btn {
  padding: 0.5rem 1rem;
  background-color: #ff9800;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn {
  padding: 0.5rem 1rem;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-btn:disabled,
.complete-btn:disabled,
.delete-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #666;
  margin: 0;
}
</style>