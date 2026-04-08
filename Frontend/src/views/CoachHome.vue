<template>
  <div class="coach-home">
    <header class="header">
      <h1>教练首页</h1>
      <div class="header-actions">
        <button @click="showAddSchedule" class="add-schedule-btn">添加排课</button>
        <button @click="goToProfile" class="profile-btn">个人中心</button>
        <button @click="handleLogout" class="logout-btn">登出</button>
      </div>
    </header>
    
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
    
    <div class="tabs">
      <button 
        @click="activeTab = 'all'" 
        :class="{ active: activeTab === 'all' }" 
        class="tab-btn"
      >
        所有排课
      </button>
      <button 
        @click="activeTab = 'pending'" 
        :class="{ active: activeTab === 'pending' }" 
        class="tab-btn"
      >
        待确认排课
      </button>
      <button 
        @click="activeTab = 'confirmed'" 
        :class="{ active: activeTab === 'confirmed' }" 
        class="tab-btn"
      >
        已确认排课
      </button>
    </div>
    
    <div class="filter-bar">
      <label class="filter-label">时间筛选:</label>
      <select v-model="timeFilter" class="time-filter-select">
        <option value="all">全部</option>
        <option value="today">今天</option>
        <option value="tomorrow">明天</option>
        <option value="dayAfterTomorrow">后天</option>
        <option value="thisWeek">本周</option>
        <option value="nextWeek">下周</option>
        <option value="thisMonth">本月</option>
        <option value="nextMonth">下月</option>
      </select>
    </div>
    
    <div class="schedule-list">
      <div v-if="filteredSchedules.length === 0" class="empty-state">
        <p>暂无排课</p>
      </div>
      <div v-for="schedule in filteredSchedules" :key="schedule.id" class="schedule-item">
        <div class="schedule-info">
          <h3>{{ schedule.schedule_date }}</h3>
          <p>时段: {{ schedule.schedule_time }}</p>
          <p>学员: {{ schedule.student_name || '未预约' }}</p>
          <p v-if="schedule.student_phone">手机号: {{ schedule.student_phone }}</p>
          <p v-if="schedule.area_name">所在区域: {{ schedule.area_name }}</p>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import request from '../utils/request'

const router = useRouter()
const userStore = useUserStore()

const schedules = ref([])
const showAddForm = ref(false)
const activeTab = ref('all')
const timeFilter = ref('all')
const newSchedule = ref({
  date: '',
  time: '上午'
})

const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
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

const getDateRange = (filter) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  switch (filter) {
    case 'today':
      return [new Date(today), new Date(today)]
    case 'tomorrow':
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      return [new Date(tomorrow), new Date(tomorrow)]
    case 'dayAfterTomorrow':
      const dayAfterTomorrow = new Date(today)
      dayAfterTomorrow.setDate(dayAfterTomorrow.getDate() + 2)
      return [new Date(dayAfterTomorrow), new Date(dayAfterTomorrow)]
    case 'thisWeek':
      const startOfWeek = new Date(today)
      startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay())
      const endOfWeek = new Date(startOfWeek)
      endOfWeek.setDate(endOfWeek.getDate() + 6)
      return [startOfWeek, endOfWeek]
    case 'nextWeek':
      const startOfNextWeek = new Date(today)
      startOfNextWeek.setDate(startOfNextWeek.getDate() - startOfNextWeek.getDay() + 7)
      const endOfNextWeek = new Date(startOfNextWeek)
      endOfNextWeek.setDate(endOfNextWeek.getDate() + 6)
      return [startOfNextWeek, endOfNextWeek]
    case 'thisMonth':
      const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1)
      const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0)
      return [startOfMonth, endOfMonth]
    case 'nextMonth':
      const startOfNextMonth = new Date(today.getFullYear(), today.getMonth() + 1, 1)
      const endOfNextMonth = new Date(today.getFullYear(), today.getMonth() + 2, 0)
      return [startOfNextMonth, endOfNextMonth]
    default:
      return [null, null]
  }
}

const isDateInRange = (scheduleDate, startDate, endDate) => {
  if (!startDate || !endDate) return true
  const date = new Date(scheduleDate)
  date.setHours(0, 0, 0, 0)
  return date >= startDate && date <= endDate
}

const filteredSchedules = computed(() => {
  let filtered = []
  
  switch (activeTab.value) {
    case 'pending':
      filtered = schedules.value.filter(schedule => schedule.status === '待确认')
      break
    case 'confirmed':
      filtered = schedules.value.filter(schedule => schedule.status === '已确认')
      break
    default:
      filtered = schedules.value
  }
  
  if (timeFilter.value !== 'all') {
    const [startDate, endDate] = getDateRange(timeFilter.value)
    filtered = filtered.filter(schedule => isDateInRange(schedule.schedule_date, startDate, endDate))
  }
  
  return filtered
})

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

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.add-schedule-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-schedule-btn:hover {
  background-color: #359469;
}

.profile-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.profile-btn:hover {
  background-color: #359469;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #cc0000;
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

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background-color: white;
  color: #666;
  border: none;
  border-bottom: 3px solid transparent;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
}

.tab-btn:hover {
  color: #42b983;
}

.tab-btn.active {
  color: #42b983;
  border-bottom-color: #42b983;
  font-weight: bold;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-label {
  font-weight: bold;
  color: #333;
  font-size: 16px;
}

.time-filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  color: #333;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.3s;
}

.time-filter-select:hover {
  border-color: #42b983;
}

.time-filter-select:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.schedule-list {
  margin-top: 1rem;
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