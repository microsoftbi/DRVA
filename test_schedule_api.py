import requests
import json

# 测试获取可用排课API
url = "http://localhost:8000/api/schedules/available"

# 测试1: 不传递任何参数
response = requests.get(url)
print(f"测试1 - 不传递任何参数:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 课程数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试2: 传递区域参数
url_with_area = "http://localhost:8000/api/schedules/available?area_id=1"
response = requests.get(url_with_area)
print(f"\n测试2 - 传递区域参数:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 课程数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试3: 传递日期参数
url_with_date = "http://localhost:8000/api/schedules/available?schedule_date=2023-01-01"
response = requests.get(url_with_date)
print(f"\n测试3 - 传递日期参数:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 课程数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试4: 传递时段参数
url_with_time = "http://localhost:8000/api/schedules/available?schedule_time=上午"
response = requests.get(url_with_time)
print(f"\n测试4 - 传递时段参数:")
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 课程数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")