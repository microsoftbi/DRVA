import requests
import json

# 测试获取可用排课API
url = "http://localhost:8000/api/schedules/available"

# 测试1: 不传递任何参数
response = requests.get(url)
print(f"测试1 - 不传递任何参数:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试2: 测试获取可用排课API（使用POST方法）
response = requests.post(url)
print(f"\n测试2 - 使用POST方法:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试3: 测试获取可用排课API（使用PUT方法）
response = requests.put(url)
print(f"\n测试3 - 使用PUT方法:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试4: 测试获取可用排课API（使用DELETE方法）
response = requests.delete(url)
print(f"\n测试4 - 使用DELETE方法:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")