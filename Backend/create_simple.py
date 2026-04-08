
# 创建一个简单的StudentHome.vue文件
template_part = '''&lt;template&gt;
  &lt;div class="student-home"&gt;
    &lt;header class="header"&gt;
      &lt;h1&gt;学员首页&lt;/h1&gt;
      &lt;button @click="goToProfile" class="profile-btn"&gt;个人中心&lt;/button&gt;
    &lt;/header&gt;
  &lt;/div&gt;
&lt;/template&gt;
'''

script_part = '''&lt;script setup&gt;
import { useRouter } from 'vue-router'

const router = useRouter()

const goToProfile = () =&gt; {
  router.push('/profile')
}
&lt;/script&gt;
'''

style_part = '''&lt;style scoped&gt;
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
&lt;/style&gt;
'''

full_content = template_part + '\n' + script_part + '\n' + style_part

with open('/Users/wadesong/Desktop/DRVA/Frontend/src/views/StudentHome.vue', 'w', encoding='utf-8') as f:
    f.write(full_content)

print('简单文件创建成功')
