import requests
import json

# 测试获取可用排课API
url = "http://localhost:8000/api/schedules/available"

# 测试1: 不传递任何参数
response = requests.get(url)
print(f"测试1 - 不传递任何参数:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试2: 测试获取可用排课API（传递area_id=1）
url_with_area = "http://localhost:8000/api/schedules/available?area_id=1"
response = requests.get(url_with_area)
print(f"\n测试2 - 传递area_id=1:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试3: 测试获取可用排课API（传递area_id=1和schedule_date=2023-01-01）
url_with_area_date = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01"
response = requests.get(url_with_area_date)
print(f"\n测试3 - 传递area_id=1和schedule_date=2023-01-01:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试4: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=上午）
url_with_all = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=上午"
response = requests.get(url_with_all)
print(f"\n测试4 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=上午:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")