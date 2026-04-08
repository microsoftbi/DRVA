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

# 测试5: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=下午）
url_with_all2 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=下午"
response = requests.get(url_with_all2)
print(f"\n测试5 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=下午:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试6: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all3 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all3)
print(f"\n测试6 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试7: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all4 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all4)
print(f"\n测试7 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试8: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all5 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all5)
print(f"\n测试8 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试9: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all6 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all6)
print(f"\n测试9 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试10: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all7 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all7)
print(f"\n测试10 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试11: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all8 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all8)
print(f"\n测试11 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试12: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all9 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all9)
print(f"\n测试12 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试13: 测试获取可用排课API（传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上）
url_with_all10 = "http://localhost:8000/api/schedules/available?area_id=1&schedule_date=2023-01-01&schedule_time=晚上"
response = requests.get(url_with_all10)
print(f"\n测试13 - 传递area_id=1、schedule_date=2023-01-01和schedule_time=晚上:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")