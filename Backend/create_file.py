
content = '''&lt;template&gt;
  &lt;div class="student-home"&gt;
    &lt;header class="header"&gt;
      &lt;h1&gt;学员首页&lt;/h1&gt;
      &lt;button @click="goToProfile" class="profile-btn"&gt;个人中心&lt;/button&gt;
    &lt;/header&gt;
    
    &lt;div class="tabs"&gt;
      &lt;button 
        :class="['tab-btn', { active: activeTab === 'available' }]"
        @click="activeTab = 'available'"
      &gt;
        可选课程
      &lt;/button&gt;
      &lt;button 
        :class="['tab-btn', { active: activeTab === 'my' }]"
        @click="activeTab = 'my'"
      &gt;
        我的课程
      &lt;/button&gt;
    &lt;/div&gt;
    
    &lt;div v-if="activeTab === 'available'" class="tab-content"&gt;
      &lt;div class="filter-section"&gt;
        &lt;div class="filter-group"&gt;
          &lt;label for="area"&gt;区域&lt;/label&gt;
          &lt;select id="area" v-model="filters.areaId"&gt;
            &lt;option value=""&gt;所有区域&lt;/option&gt;
            &lt;option v-for="area in areas" :key="area.id" :value="area.id"&gt;
              {{ area.name }}
            &lt;/option&gt;
          &lt;/select&gt;
        &lt;/div&gt;
        
        &lt;div class="filter-group"&gt;
          &lt;label for="date"&gt;日期&lt;/label&gt;
          &lt;input type="date" id="date" v-model="filters.date" /&gt;
        &lt;/div&gt;
        
        &lt;div class="filter-group"&gt;
          &lt;label for="time"&gt;时段&lt;/label&gt;
          &lt;select id="time" v-model="filters.time"&gt;
            &lt;option value=""&gt;所有时段&lt;/option&gt;
            &lt;option value="上午"&gt;上午&lt;/option&gt;
            &lt;option value="下午"&gt;下午&lt;/option&gt;
            &lt;option value="晚上"&gt;晚上&lt;/option&gt;
          &lt;/select&gt;
        &lt;/div&gt;
        
        &lt;button @click="searchSchedules" class="search-btn"&gt;搜索&lt;/button&gt;
      &lt;/div&gt;
      
      &lt;div class="schedule-list"&gt;
        &lt;div v-if="schedules.length === 0" class="empty-state"&gt;
          &lt;p&gt;暂无可用课程&lt;/p&gt;
        &lt;/div&gt;
        &lt;div v-for="schedule in schedules" :key="schedule.id" class="schedule-item"&gt;
          &lt;div class="schedule-info"&gt;
            &lt;h3&gt;{{ schedule.coach_name }}&lt;/h3&gt;
            &lt;p&gt;日期: {{ schedule.schedule_date }}&lt;/p&gt;
            &lt;p&gt;时段: {{ schedule.schedule_time }}&lt;/p&gt;
            &lt;p&gt;区域: {{ schedule.area_name }}&lt;/p&gt;
          &lt;/div&gt;
          &lt;button @click="bookSchedule(schedule.id)" class="book-btn"&gt;预约&lt;/button&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
    
    &lt;div v-if="activeTab === 'my'" class="tab-content"&gt;
      &lt;div class="filter-section"&gt;
        &lt;label for="myTimeFilter"&gt;时间筛选：&lt;/label&gt;
        &lt;select id="myTimeFilter" v-model="selectedMyTimeFilter" @change="filterMySchedules"&gt;
          &lt;option v-for="option in timeFilterOptions" :key="option.value" :value="option.value"&gt;
            {{ option.label }}
          &lt;/option&gt;
        &lt;/select&gt;
      &lt;/div&gt;
      &lt;div class="schedule-list"&gt;
        &lt;div v-if="filteredMySchedules.length === 0" class="empty-state"&gt;
          &lt;p&gt;暂无已预约课程&lt;/p&gt;
        &lt;/div&gt;
        &lt;div v-for="schedule in filteredMySchedules" :key="schedule.id" class="schedule-item" :class="getScheduleStatusClass(schedule.status)"&gt;
          &lt;div class="schedule-info"&gt;
            &lt;h3&gt;{{ schedule.coach_name }}&lt;/h3&gt;
            &lt;p&gt;日期: {{ schedule.schedule_date }}&lt;/p&gt;
            &lt;p&gt;时段: {{ schedule.schedule_time }}&lt;/p&gt;
            &lt;p&gt;教练电话: {{ schedule.coach_phone }}&lt;/p&gt;
            &lt;p&gt;区域: {{ schedule.area_name }}&lt;/p&gt;
            &lt;p&gt;状态: {{ schedule.status }}&lt;/p&gt;
          &lt;/div&gt;
          &lt;button 
            @click="cancelSchedule(schedule.id)" 
            class="cancel-btn"
            :disabled="schedule.status !== '待确认'"
          &gt;
            取消
          &lt;/button&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup&gt;
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import request from '../utils/request'

const router = useRouter()
const userStore = useUserStore()

const areas = ref([])
const filters = ref({
  areaId: '',
  date: '',
  time: ''
})
const schedules = ref([])
const mySchedules = ref([])
const activeTab = ref('available')
const selectedMyTimeFilter = ref('all')
const timeFilterOptions = ref([
  { value: 'all', label: '全部' },
  { value: 'today', label: '今天' },
  { value: 'tomorrow', label: '明天' },
  { value: 'dayAfterTomorrow', label: '后天' },
  { value: 'thisWeek', label: '本周' },
  { value: 'nextWeek', label: '下周' },
  { value: 'thisMonth', label: '本月' },
  { value: 'nextMonth', label: '下个月' }
])
const filteredMySchedules = ref([])

const goToProfile = () =&gt; {
  router.push('/profile')
}

const getAreas = async () =&gt; {
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

const searchSchedules = async () =&gt; {
  try {
    const params = new URLSearchParams()
    if (filters.value.areaId) {
      params.append('area_id', filters.value.areaId)
    }
    if (filters.value.date) {
      params.append('schedule_date', filters.value.date)
    }
    if (filters.value.time) {
      params.append('schedule_time', filters.value.time)
    }
    
    const response = await request({
      url: `/schedules/available?${params}`,
      method: 'get'
    })
    
    if (response.success) {
      schedules.value = response.data.schedules
    }
  } catch (error) {
    console.error('搜索课程失败:', error)
  }
}

const bookSchedule = async (scheduleId) =&gt; {
  try {
    console.log('开始预约课程, scheduleId:', scheduleId)
    console.log('userStore.userInfo:', userStore.userInfo)
    console.log('userStore.userInfo.id:', userStore.userInfo?.id)
    
    const response = await request({
      url: `/schedules/${scheduleId}/book?student_id=${userStore.userInfo.id}`,
      method: 'put'
    })
    console.log('预约响应:', response)
    
    if (response.success) {
      alert('预约成功')
      searchSchedules()
      getMySchedules()
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('预约课程失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
    alert('预约失败')
  }
}

const getMySchedules = async () =&gt; {
  try {
    const response = await request({
      url: `/schedules/student/${userStore.userInfo.id}`,
      method: 'get'
    })
    
    if (response.success) {
      mySchedules.value = response.data.schedules
      filterMySchedules()
    }
  } catch (error) {
    console.error('获取我的课程失败:', error)
  }
}

const startOfDay = (date) =&gt; new Date(date.getFullYear(), date.getMonth(), date.getDate())
const endOfDay = (date) =&gt; new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59)

const getStartOfWeek = (date) =&gt; {
  const d = new Date(date)
  const day = d.getDay()
  const diff = d.getDate() - day + (day === 0 ? -6 : 1)
  return new Date(d.setDate(diff))
}

const getStartOfMonth = (date) =&gt; new Date(date.getFullYear(), date.getMonth(), 1)

const getDateRange = (filter) =&gt; {
  const today = new Date()
  
  if (filter === 'today') {
    return { start: startOfDay(today), end: endOfDay(today) }
  }
  
  if (filter === 'tomorrow') {
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    return { start: startOfDay(tomorrow), end: endOfDay(tomorrow) }
  }
  
  if (filter === 'dayAfterTomorrow') {
    const dayAfterTomorrow = new Date(today)
    dayAfterTomorrow.setDate(dayAfterTomorrow.getDate() + 2)
    return { start: startOfDay(dayAfterTomorrow), end: endOfDay(dayAfterTomorrow) }
  }
  
  if (filter === 'thisWeek') {
    const weekStart = getStartOfWeek(today)
    const weekEnd = new Date(weekStart)
    weekEnd.setDate(weekEnd.getDate() + 6)
    return { start: startOfDay(weekStart), end: endOfDay(weekEnd) }
  }
  
  if (filter === 'nextWeek') {
    const nextWeekStart = getStartOfWeek(today)
    nextWeekStart.setDate(nextWeekStart.getDate() + 7)
    const nextWeekEnd = new Date(nextWeekStart)
    nextWeekEnd.setDate(nextWeekEnd.getDate() + 6)
    return { start: startOfDay(nextWeekStart), end: endOfDay(nextWeekEnd) }
  }
  
  if (filter === 'thisMonth') {
    const monthStart = getStartOfMonth(today)
    const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0)
    return { start: startOfDay(monthStart), end: endOfDay(monthEnd) }
  }
  
  if (filter === 'nextMonth') {
    const nextMonthStart = new Date(today.getFullYear(), today.getMonth() + 1, 1)
    const nextMonthEnd = new Date(today.getFullYear(), today.getMonth() + 2, 0)
    return { start: startOfDay(nextMonthStart), end: endOfDay(nextMonthEnd) }
  }
  
  return null
}

const filterMySchedules = () =&gt; {
  if (selectedMyTimeFilter.value === 'all') {
    filteredMySchedules.value = mySchedules.value
    return
  }
  
  const range = getDateRange(selectedMyTimeFilter.value)
  if (!range) {
    filteredMySchedules.value = mySchedules.value
    return
  }
  
  filteredMySchedules.value = mySchedules.value.filter(schedule =&gt; {
    const scheduleDate = new Date(schedule.schedule_date)
    return scheduleDate &gt;= range.start &amp;&amp; scheduleDate &lt;= range.end
  })
}

const getScheduleStatusClass = (status) =&gt; {
  switch (status) {
    case '已确认':
      return 'status-confirmed'
    case '待确认':
      return 'status-pending'
    case '已取消':
      return 'status-cancelled'
    case '已完成':
      return 'status-completed'
    default:
      return ''
  }
}

const cancelSchedule = async (scheduleId) =&gt; {
  if (confirm('确定要取消预约吗？')) {
    try {
      const response = await request({
        url: `/schedules/${scheduleId}/cancel`,
        method: 'put'
      })
      
      if (response.success) {
        alert('取消成功')
        searchSchedules()
        getMySchedules()
      } else {
        alert(response.message)
      }
    } catch (error) {
      console.error('取消预约失败:', error)
      alert('取消失败')
    }
  }
}

onMounted(() =&gt; {
  console.log('StudentHome 加载, userStore.userInfo:', userStore.userInfo)
  console.log('userStore.token:', userStore.token)
  console.log('localStorage.userInfo:', localStorage.getItem('userInfo'))
  
  const setDefaultArea = () =&gt; {
    if (userStore.userInfo?.area_id) {
      filters.value.areaId = userStore.userInfo.area_id
    } else {
      const storedUserInfo = localStorage.getItem('userInfo')
      if (storedUserInfo) {
        try {
          const parsed = JSON.parse(storedUserInfo)
          if (parsed.area_id) {
            filters.value.areaId = parsed.area_id
          }
        } catch (e) {
          console.error('解析 localStorage 中的 userInfo 失败', e)
        }
      }
    }
  }
  
  setDefaultArea()
  getAreas()
  searchSchedules()
  getMySchedules()
})
&lt;/script&gt;

&lt;style scoped&gt;
.student-home {
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

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.tab-btn {
  padding: 0.75rem 2rem;
  background-color: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

.tab-btn.active {
  background-color: #42b983;
  color: white;
}

.tab-content {
  width: 100%;
}

.filter-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: bold;
  color: #666;
}

.filter-group select,
.filter-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-btn {
  align-self: flex-end;
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.schedule-list,
.my-schedules {
  margin-bottom: 2rem;
}

.schedule-list h2,
.my-schedules h2 {
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

.schedule-item.status-confirmed {
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
}

.schedule-item.status-pending {
  background-color: #fff8e1;
  border-left: 4px solid #ffc107;
}

.schedule-item.status-cancelled {
  background-color: #f5f5f5;
  border-left: 4px solid #9e9e9e;
}

.schedule-item.status-completed {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.schedule-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.schedule-info p {
  margin: 0.25rem 0;
  color: #666;
}

.book-btn {
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

.cancel-btn:disabled {
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
&lt;/style&gt;
'''

with open('/Users/wadesong/Desktop/DRVA/Frontend/src/views/StudentHome.vue', 'w', encoding='utf-8') as f:
    f.write(content)

print('文件创建成功')
