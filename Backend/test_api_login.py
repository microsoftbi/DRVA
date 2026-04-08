
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("=== 测试学员登录API ===")
try:
    response = requests.post(f"{BASE_URL}/students/login", json={
        "phone": "13800138001",
        "password": "123456"
    })
    print(f"状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"请求错误: {e}")

print("\n=== 测试管理员登录API ===")
try:
    response = requests.post(f"{BASE_URL}/admins/login", json={
        "email": "admin@example.com",
        "password": "adminadmin"
    })
    print(f"状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"请求错误: {e}")
