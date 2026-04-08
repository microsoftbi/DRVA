import requests
import json

# 测试获取可用排课
url = "http://localhost:8000/api/schedules/available"

# 先测试不传递任何参数
response = requests.get(url)
print(f"无参数请求 - 状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 课程数量: {len(data['data']['schedules'])}")
    if data['data']['schedules']:
        print(f"第一个课程: {data['data']['schedules'][0]}")
else:
    print(f"失败 - 错误信息: {response.json()}")

# 测试传递区域参数
url_with_area = "http://localhost:8000/api/schedules/available?area_id=1"
response = requests.get(url_with_area)
print(f"\n区域1请求 - 状态码: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"成功 - 课程数量: {len(data['data']['schedules'])}")
else:
    print(f"失败 - 错误信息: {response.json()}")