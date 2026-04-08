<template>
  <div class="profile">
    <header class="header">
      <h1>个人中心</h1>
      <button @click="logout" class="logout-btn">退出登录</button>
    </header>
    
    <div class="profile-info">
      <h2>个人信息</h2>
      <div class="info-item">
        <label>姓名</label>
        <span>{{ userInfo.name }}</span>
      </div>
      <div class="info-item">
        <label>手机号</label>
        <span>{{ userInfo.phone }}</span>
      </div>
      <div class="info-item" v-if="userInfo.email">
        <label>邮箱</label>
        <span>{{ userInfo.email }}</span>
      </div>
      <div class="info-item">
        <label>区域</label>
        <span>{{ userInfo.area_name }}</span>
      </div>
      <div class="info-item">
        <label>状态</label>
        <span>{{ userInfo.status }}</span>
      </div>
    </div>
    
    <div class="change-password">
      <h2>修改密码</h2>
      <form @submit.prevent="changePassword">
        <div class="form-group">
          <label for="oldPassword">旧密码</label>
          <input
            type="password"
            id="oldPassword"
            v-model="passwordForm.oldPassword"
            placeholder="请输入旧密码"
            required
          />
        </div>
        <div class="form-group">
          <label for="newPassword">新密码</label>
          <input
            type="password"
            id="newPassword"
            v-model="passwordForm.newPassword"
            placeholder="请输入新密码"
            required
            minlength="6"
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">确认新密码</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="passwordForm.confirmPassword"
            placeholder="请再次输入新密码"
            required
            minlength="6"
          />
        </div>
        <button type="submit" class="submit-btn">修改密码</button>
      </form>
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

const userInfo = ref({})
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const logout = () => {
  if (confirm('确定要退出登录吗？')) {
    userStore.logout()
    router.push('/')
  }
}

const getUserInfo = async () => {
  try {
    let response
    if (userStore.userInfo.role === 'student') {
      response = await request({
        url: `/students/${userStore.userInfo.id}`,
        method: 'get'
      })
    } else if (userStore.userInfo.role === 'coach') {
      response = await request({
        url: `/coaches/${userStore.userInfo.id}`,
        method: 'get'
      })
    } else if (userStore.userInfo.role === 'admin') {
      response = await request({
        url: `/admins/${userStore.userInfo.id}`,
        method: 'get'
      })
    }
    
    if (response.success) {
      userInfo.value = response.data.user
    }
  } catch (error) {
    console.error('获取个人信息失败:', error)
  }
}

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('两次输入的新密码不一致')
    return
  }
  
  try {
    let response
    if (userStore.userInfo.role === 'student') {
      response = await request({
        url: `/students/${userStore.userInfo.id}/password`,
        method: 'put',
        data: {
          old_password: passwordForm.value.oldPassword,
          new_password: passwordForm.value.newPassword
        }
      })
    } else if (userStore.userInfo.role === 'coach') {
      response = await request({
        url: `/coaches/${userStore.userInfo.id}/password`,
        method: 'put',
        data: {
          old_password: passwordForm.value.oldPassword,
          new_password: passwordForm.value.newPassword
        }
      })
    } else if (userStore.userInfo.role === 'admin') {
      response = await request({
        url: `/admins/${userStore.userInfo.id}/password`,
        method: 'put',
        data: {
          old_password: passwordForm.value.oldPassword,
          new_password: passwordForm.value.newPassword
        }
      })
    }
    
    if (response.success) {
      alert('密码修改成功')
      passwordForm.value = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    alert('修改失败')
  }
}

onMounted(() => {
  getUserInfo()
})
</script>

<style scoped>
.profile {
  padding: 1rem;
  max-width: 800px;
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

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.profile-info,
.change-password {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.profile-info h2,
.change-password h2 {
  margin-bottom: 1rem;
  color: #333;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: white;
  border-radius: 4px;
}

.info-item label {
  font-weight: bold;
  color: #666;
}

.info-item span {
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

.submit-btn {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>