<template>
  <div class="admin-home">
    <header class="header">
      <h1>管理员首页</h1>
      <div class="header-actions">
        <button @click="goToProfile" class="profile-btn">个人中心</button>
        <button @click="handleLogout" class="logout-btn">登出</button>
      </div>
    </header>
    
    <div class="nav-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        class="tab-btn"
        :class="{ active: activeTab === tab.id }"
      >
        {{ tab.name }}
      </button>
    </div>
    
    <!-- 区域管理 -->
    <div v-if="activeTab === 1" class="tab-content">
      <h2>区域管理</h2>
      <button @click="showAddAreaForm = true" class="add-btn">添加区域</button>
      
      <div v-if="showAddAreaForm" class="add-form">
        <h3>添加区域</h3>
        <form @submit.prevent="addArea">
          <div class="form-group">
            <label for="areaName">区域名称</label>
            <input
              type="text"
              id="areaName"
              v-model="newArea.name"
              placeholder="请输入区域名称"
              required
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="submit-btn">保存</button>
            <button type="button" @click="showAddAreaForm = false" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
      
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>区域名称</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="area in areas" :key="area.id">
              <td>{{ area.id }}</td>
              <td>{{ area.name }}</td>
              <td>{{ area.created_at }}</td>
              <td>
                <button @click="editArea(area)" class="edit-btn">编辑</button>
                <button @click="deleteArea(area.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 教练管理 -->
    <div v-if="activeTab === 2" class="tab-content">
      <h2>教练管理</h2>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>手机号</th>
              <th>区域</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="coach in coaches" :key="coach.id">
              <td>{{ coach.id }}</td>
              <td>{{ coach.name }}</td>
              <td>{{ coach.phone }}</td>
              <td>{{ coach.area_name }}</td>
              <td>{{ coach.status }}</td>
              <td>
                <button @click="confirmCoach(coach.id)" class="confirm-btn" v-if="coach.status === '待确认'">确认</button>
                <button @click="resetCoachPassword(coach.id)" class="reset-btn">重置密码</button>
                <button @click="deleteCoach(coach.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 学员管理 -->
    <div v-if="activeTab === 3" class="tab-content">
      <h2>学员管理</h2>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>手机号</th>
              <th>区域</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.name }}</td>
              <td>{{ student.phone }}</td>
              <td>{{ student.area_name }}</td>
              <td>{{ student.status }}</td>
              <td>
                <button @click="resetStudentPassword(student.id)" class="reset-btn">重置密码</button>
                <button @click="deleteStudent(student.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 排课管理 -->
    <div v-if="activeTab === 4" class="tab-content">
      <h2>排课管理</h2>
      <div class="filter-section">
        <label for="timeFilter">时间筛选：</label>
        <select id="timeFilter" v-model="selectedTimeFilter" @change="filterSchedules">
          <option v-for="option in timeFilterOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>教练</th>
              <th>教练电话</th>
              <th>区域</th>
              <th>日期</th>
              <th>时段</th>
              <th>学员</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="schedule in schedules" :key="schedule.id">
              <td>{{ schedule.id }}</td>
              <td>{{ schedule.coach_name }}</td>
              <td>{{ schedule.coach_phone }}</td>
              <td>{{ schedule.area_name }}</td>
              <td>{{ schedule.schedule_date }}</td>
              <td>{{ schedule.schedule_time }}</td>
              <td>{{ schedule.student_name || '未预约' }}</td>
              <td>{{ schedule.status }}</td>
              <td>
                <button @click="confirmSchedule(schedule.id)" class="confirm-btn" v-if="schedule.status === '待确认' && schedule.student_id">确认</button>
                <button @click="deleteSchedule(schedule.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
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

const activeTab = ref(1)
const tabs = ref([
  { id: 1, name: '区域管理' },
  { id: 2, name: '教练管理' },
  { id: 3, name: '学员管理' },
  { id: 4, name: '排课管理' }
])

// 区域管理
const areas = ref([])
const showAddAreaForm = ref(false)
const newArea = ref({ name: '' })

// 教练管理
const coaches = ref([])

// 学员管理
const students = ref([])

// 排课管理
const schedules = ref([])
const allSchedules = ref([])
const selectedTimeFilter = ref('all')

const timeFilterOptions = [
  { value: 'all', label: '全部' },
  { value: 'today', label: '今天' },
  { value: 'tomorrow', label: '明天' },
  { value: 'dayAfterTomorrow', label: '后天' },
  { value: 'thisWeek', label: '本周' },
  { value: 'nextWeek', label: '下周' },
  { value: 'thisMonth', label: '本月' },
  { value: 'nextMonth', label: '下个月' }
]

const getDateRange = (filter) => {
  const today = new Date()
  const startOfDay = (date) => new Date(date.getFullYear(), date.getMonth(), date.getDate())
  const endOfDay = (date) => new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59)
  
  const getStartOfWeek = (date) => {
    const d = new Date(date)
    const day = d.getDay()
    const diff = d.getDate() - day + (day === 0 ? -6 : 1)
    return new Date(d.setDate(diff))
  }
  
  const getStartOfMonth = (date) => new Date(date.getFullYear(), date.getMonth(), 1)
  
  switch (filter) {
    case 'today':
      return { start: startOfDay(today), end: endOfDay(today) }
    case 'tomorrow':
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      return { start: startOfDay(tomorrow), end: endOfDay(tomorrow) }
    case 'dayAfterTomorrow':
      const dayAfterTomorrow = new Date(today)
      dayAfterTomorrow.setDate(dayAfterTomorrow.getDate() + 2)
      return { start: startOfDay(dayAfterTomorrow), end: endOfDay(dayAfterTomorrow) }
    case 'thisWeek':
      const weekStart = getStartOfWeek(today)
      const weekEnd = new Date(weekStart)
      weekEnd.setDate(weekEnd.getDate() + 6)
      return { start: startOfDay(weekStart), end: endOfDay(weekEnd) }
    case 'nextWeek':
      const nextWeekStart = getStartOfWeek(today)
      nextWeekStart.setDate(nextWeekStart.getDate() + 7)
      const nextWeekEnd = new Date(nextWeekStart)
      nextWeekEnd.setDate(nextWeekEnd.getDate() + 6)
      return { start: startOfDay(nextWeekStart), end: endOfDay(nextWeekEnd) }
    case 'thisMonth':
      const monthStart = getStartOfMonth(today)
      const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0)
      return { start: startOfDay(monthStart), end: endOfDay(monthEnd) }
    case 'nextMonth':
      const nextMonthStart = new Date(today.getFullYear(), today.getMonth() + 1, 1)
      const nextMonthEnd = new Date(today.getFullYear(), today.getMonth() + 2, 0)
      return { start: startOfDay(nextMonthStart), end: endOfDay(nextMonthEnd) }
    default:
      return null
  }
}

const filterSchedules = () => {
  if (selectedTimeFilter.value === 'all') {
    schedules.value = [...allSchedules.value]
    return
  }
  
  const range = getDateRange(selectedTimeFilter.value)
  if (!range) {
    schedules.value = [...allSchedules.value]
    return
  }
  
  schedules.value = allSchedules.value.filter(schedule => {
    const scheduleDate = new Date(schedule.schedule_date)
    return scheduleDate >= range.start && scheduleDate <= range.end
  })
}

const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 区域管理方法
const getAreas = async () => {
  try {
    const response = await request({
      url: '/areas',
      method: 'get'
    })
    if (response.success) {
      areas.value = response.data.areas
    }
  } catch (error) {
    console.error('获取区域失败:', error)
  }
}

const addArea = async () => {
  try {
    const response = await request({
      url: '/areas',
      method: 'post',
      data: newArea.value
    })
    
    if (response.success) {
      alert('区域添加成功')
      showAddAreaForm.value = false
      newArea.value = { name: '' }
      getAreas()
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('添加区域失败:', error)
    alert('添加失败')
  }
}

const editArea = (area) => {
  // 编辑区域逻辑
  console.log('编辑区域:', area)
}

const deleteArea = async (areaId) => {
  if (confirm('确定要删除该区域吗？')) {
    try {
      const response = await request({
        url: `/areas/${areaId}`,
        method: 'delete'
      })
      
      if (response.success) {
        alert('删除成功')
        getAreas()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('删除区域失败:', error)
      alert('删除失败')
    }
  }
}

// 教练管理方法
const getCoaches = async () => {
  try {
    const response = await request({
      url: '/coaches',
      method: 'get'
    })
    if (response.success) {
      coaches.value = response.data.coaches
    }
  } catch (error) {
    console.error('获取教练失败:', error)
  }
}

const confirmCoach = async (coachId) => {
  if (confirm('确定要确认该教练吗？')) {
    try {
      const response = await request({
        url: `/coaches/${coachId}`,
        method: 'put',
        data: { status: '正常' }
      })
      
      if (response.success) {
        alert('确认成功')
        getCoaches()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('确认教练失败:', error)
      alert('确认失败')
    }
  }
}

const resetCoachPassword = async (coachId) => {
  const newPassword = prompt('请输入新密码:')
  if (newPassword) {
    try {
      const response = await request({
        url: `/coaches/${coachId}/reset-password`,
        method: 'put',
        data: { new_password: newPassword }
      })
      
      if (response.success) {
        alert('密码重置成功')
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('重置教练密码失败:', error)
      alert('重置失败')
    }
  }
}

const deleteCoach = async (coachId) => {
  if (confirm('确定要删除该教练吗？')) {
    try {
      const response = await request({
        url: `/coaches/${coachId}`,
        method: 'delete'
      })
      
      if (response.success) {
        alert('删除成功')
        getCoaches()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('删除教练失败:', error)
      alert('删除失败')
    }
  }
}

// 学员管理方法
const getStudents = async () => {
  try {
    const response = await request({
      url: '/students',
      method: 'get'
    })
    if (response.success) {
      students.value = response.data.students
    }
  } catch (error) {
    console.error('获取学员失败:', error)
  }
}

const resetStudentPassword = async (studentId) => {
  const newPassword = prompt('请输入新密码:')
  if (newPassword) {
    try {
      const response = await request({
        url: `/students/${studentId}/reset-password`,
        method: 'put',
        data: { new_password: newPassword }
      })
      
      if (response.success) {
        alert('密码重置成功')
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('重置学员密码失败:', error)
      alert('重置失败')
    }
  }
}

const deleteStudent = async (studentId) => {
  if (confirm('确定要删除该学员吗？')) {
    try {
      const response = await request({
        url: `/students/${studentId}`,
        method: 'delete'
      })
      
      if (response.success) {
        alert('删除成功')
        getStudents()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('删除学员失败:', error)
      alert('删除失败')
    }
  }
}

// 排课管理方法
const getSchedules = async () => {
  try {
    const response = await request({
      url: '/schedules',
      method: 'get'
    })
    if (response.success) {
      allSchedules.value = response.data.schedules
      filterSchedules()
    }
  } catch (error) {
    console.error('获取排课失败:', error)
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
  getAreas()
  getCoaches()
  getStudents()
  getSchedules()
})
</script>

<style scoped>
.admin-home {
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

.nav-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 0.5rem 1rem;
  background-color: #ddd;
  color: #333;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.tab-btn.active {
  background-color: #42b983;
  color: white;
}

.tab-content {
  margin-bottom: 2rem;
}

.tab-content h2 {
  margin-bottom: 1rem;
  color: #333;
}

.filter-section {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-section label {
  font-weight: bold;
  color: #666;
}

.filter-section select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.add-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.add-form {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.add-form h3 {
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

.form-group input {
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

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.data-table th,
.data-table td {
  padding: 0.8rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.data-table th {
  background-color: #f5f5f5;
  font-weight: bold;
  color: #666;
}

.edit-btn {
  padding: 0.3rem 0.8rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.delete-btn {
  padding: 0.3rem 0.8rem;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.confirm-btn {
  padding: 0.3rem 0.8rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.reset-btn {
  padding: 0.3rem 0.8rem;
  background-color: #ff9800;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}
</style>