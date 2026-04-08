import requests
import json

# 测试健康检查
url = "http://localhost:8000/health"

response = requests.get(url)
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.json()}")