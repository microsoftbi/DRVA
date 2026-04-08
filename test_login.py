import requests
import json

# 测试学员登录
url = "http://localhost:8000/api/students/login"
data = {
    "phone": "13800138001",
    "password": "123456"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(data), headers=headers)
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.json()}")