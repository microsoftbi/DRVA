import requests
import json

# 测试获取可用排课API
url = "http://localhost:8000/api/schedules/available"

# 测试1: 不传递任何参数
response = requests.get(url)
print(f"测试1 - 不传递任何参数:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试2: 测试获取学员排课API
url_student_schedules = "http://localhost:8000/api/schedules/student/1"
response = requests.get(url_student_schedules)
print(f"\n测试2 - 获取学员排课API:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 排课数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试3: 测试其他API
url_health = "http://localhost:8000/health"
response = requests.get(url_health)
print(f"\n测试3 - 健康检查API:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 健康状态: {data['status']}")
else:
    print(f"失败 - 错误信息: {response.json()}")