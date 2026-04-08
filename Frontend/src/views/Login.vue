<template>
  <div class="login-container">
    <div class="login-form">
      <h2>驾驶陪练系统</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label :for="form.role === 'admin' ? 'email' : 'phone'">
            {{ form.role === 'admin' ? '邮箱' : '手机号' }}
          </label>
          <input
            v-if="form.role !== 'admin'"
            type="tel"
            id="phone"
            v-model="form.phone"
            placeholder="请输入手机号"
            required
          />
          <input
            v-else
            type="email"
            id="email"
            v-model="form.email"
            placeholder="请输入邮箱"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="请输入密码"
            required
          />
        </div>
        <div class="form-group">
          <label for="role">角色</label>
          <select id="role" v-model="form.role">
            <option value="student">学员</option>
            <option value="coach">教练</option>
            <option value="admin">管理员</option>
          </select>
        </div>
        <button type="submit" class="login-btn">登录</button>
      </form>
      <div class="register-link">
        <p>还没有账号？<a @click="goToRegister">立即注册</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { login, coachLogin, adminLogin } from '../api/auth'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  phone: '',
  email: '',
  password: '',
  role: 'student'
})

const handleLogin = async () => {
  try {
    let response
    if (form.value.role === 'student') {
      response = await login({ phone: form.value.phone, password: form.value.password })
    } else if (form.value.role === 'coach') {
      response = await coachLogin({ phone: form.value.phone, password: form.value.password })
    } else if (form.value.role === 'admin') {
      response = await adminLogin({ email: form.value.email, password: form.value.password })
    }
    
    if (response.success) {
      console.log('登录响应数据:', response.data)
      console.log('用户信息:', response.data.user)
      console.log('用户ID:', response.data.user?.id)
      userStore.setUserInfo(response.data.user)
      userStore.setToken(response.data.token)
      console.log('登录后 userStore.userInfo:', userStore.userInfo)
      
      if (form.value.role === 'student') {
        router.push('/student/home')
      } else if (form.value.role === 'coach') {
        router.push('/coach/home')
      } else if (form.value.role === 'admin') {
        router.push('/admin/home')
      }
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请检查账号或密码')
  }
}

const goToRegister = () => {
  // 跳转到注册页面
  console.log('跳转到注册页面')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-form h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.login-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #359469;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #42b983;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>