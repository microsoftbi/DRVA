import requests
import json

# 测试获取可用排课API
url = "http://localhost:8000/api/schedules/available"

# 测试1: 不传递任何参数
response = requests.get(url)
print(f"测试1 - 不传递任何参数:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试2: 测试其他API
url_areas = "http://localhost:8000/api/areas"
response = requests.get(url_areas)
print(f"\n测试2 - 获取区域API:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 区域数量: {len(data['data']['areas'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试3: 测试获取学员API
url_students = "http://localhost:8000/api/students"
response = requests.get(url_students)
print(f"\n测试3 - 获取学员API:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 学员数量: {len(data['data']['students'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")