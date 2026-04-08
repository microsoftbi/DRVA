import requests
import json

# 测试获取可用排课API
url = "http://localhost:8000/api/schedules/available"

# 测试1: 不传递任何参数
response = requests.get(url)
print(f"测试1 - 不传递任何参数:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试2: 测试获取排课详情API
url_schedule = "http://localhost:8000/api/schedules/1"
response = requests.get(url_schedule)
print(f"\n测试2 - 获取排课详情API:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 排课信息: {data['data']['schedule']}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试3: 测试获取教练排课API
url_coach_schedules = "http://localhost:8000/api/schedules/coach/1"
response = requests.get(url_coach_schedules)
print(f"\n测试3 - 获取教练排课API:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 排课数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")