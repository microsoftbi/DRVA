import requests
import json

# 测试获取可用排课
url = "http://localhost:8000/api/schedules/available"

response = requests.get(url)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    print(f"响应内容: {response.json()}")
else:
    print(f"错误信息: {response.json()}")