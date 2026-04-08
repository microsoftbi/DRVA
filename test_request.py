import requests

# 测试请求
url = "http://localhost:8000/api/schedules/available"
headers = {
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(f"状态码: {response.status_code}")
print(f"响应头: {dict(response.headers)}")
print(f"响应内容: {response.text}")