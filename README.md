# 驾驶陪练系统

## 项目概述
驾驶陪练系统旨在帮助有驾驶证的人进行驾驶陪练服务，系统包含学员、教练和管理员三种角色，提供完整的注册、登录、排课、约课等功能。
这个项目是我使用AI创建的，使用的是TRAE CN + Doubao大模型。目的是学习Vibe coding以及Vue 3编程。

## 技术架构
- **前端框架**：Vue 3 + Vite
- **后端框架**：FastAPI
- **数据库**：SQLLite
- **状态管理**：Session（后端） + Pinia（前端）
- **API文档**：FastAPI自动生成OpenAPI文档

## 项目结构
```
.
├── database.sql          # 数据库表结构
├── database.py           # 数据库连接模块
├── models.py             # 数据模型
├── dao.py               # 数据访问层
├── services.py           # 业务逻辑层
├── main.py              # API接口层
├── requirements.txt      # 依赖包
├── 需求文档.md           # 需求文档
├── 设计文档.md           # 设计文档
├── 单元测试文档.md       # 单元测试文档
├── 用户测试文档.md       # 用户测试文档
├── 学员手册.md           # 学员手册
└── 教练手册.md           # 教练手册
```

## 环境搭建

### 1. 安装依赖
```bash
pip3 install -r requirements.txt
```

### 2. 创建数据库
```bash
sqlite3 drva.db < database.sql
```

### 3. 运行后端服务
```bash
python3 main.py
```

### 4. 访问API文档
- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

## 系统角色

### 1. 学员
- 注册、登录
- 查看可用课程
- 预约课程
- 取消预约
- 查看我的课程

### 2. 教练
- 注册、登录
- 设置可用时间
- 查看排课信息
- 确认课程
- 标记课程完成

### 3. 管理员
- 登录
- 区域管理
- 教练管理
- 学员管理
- 排课管理

## 默认账号
- **管理员**：admin@example.com / admin

## API接口

### 区域接口
- `GET /api/areas`：获取所有区域
- `GET /api/areas/{area_id}`：根据ID获取区域
- `POST /api/areas`：创建区域
- `PUT /api/areas/{area_id}`：更新区域
- `DELETE /api/areas/{area_id}`：删除区域

### 学员接口
- `GET /api/students`：获取所有学员
- `GET /api/students/{student_id}`：根据ID获取学员
- `POST /api/students/register`：学员注册
- `POST /api/students/login`：学员登录
- `PUT /api/students/{student_id}`：更新学员
- `PUT /api/students/{student_id}/password`：更新学员密码
- `PUT /api/students/{student_id}/reset-password`：重置学员密码
- `DELETE /api/students/{student_id}`：删除学员

### 教练接口
- `GET /api/coaches`：获取所有教练
- `GET /api/coaches/{coach_id}`：根据ID获取教练
- `POST /api/coaches/register`：教练注册
- `POST /api/coaches/login`：教练登录
- `PUT /api/coaches/{coach_id}`：更新教练
- `PUT /api/coaches/{coach_id}/password`：更新教练密码
- `PUT /api/coaches/{coach_id}/reset-password`：重置教练密码
- `DELETE /api/coaches/{coach_id}`：删除教练

### 排课接口
- `GET /api/schedules`：获取所有排课
- `GET /api/schedules/{schedule_id}`：根据ID获取排课
- `GET /api/schedules/coach/{coach_id}`：根据教练ID获取排课
- `GET /api/schedules/student/{student_id}`：根据学员ID获取排课
- `GET /api/schedules/available`：获取可用排课
- `POST /api/schedules`：创建排课
- `PUT /api/schedules/{schedule_id}`：更新排课
- `PUT /api/schedules/{schedule_id}/book`：预约排课
- `PUT /api/schedules/{schedule_id}/confirm`：确认排课
- `PUT /api/schedules/{schedule_id}/cancel`：取消排课
- `PUT /api/schedules/{schedule_id}/complete`：标记排课完成
- `DELETE /api/schedules/{schedule_id}`：删除排课

### 管理员接口
- `GET /api/admins`：获取所有管理员
- `GET /api/admins/{admin_id}`：根据ID获取管理员
- `POST /api/admins/login`：管理员登录
- `PUT /api/admins/{admin_id}`：更新管理员
- `PUT /api/admins/{admin_id}/password`：更新管理员密码
- `DELETE /api/admins/{admin_id}`：删除管理员

## 数据库表结构

### 区域表（areas）
- id：区域ID
- name：区域名称
- created_at：创建时间
- updated_at：更新时间

### 学员表（students）
- id：学员ID
- name：姓名
- phone：手机号
- email：邮箱
- password：密码
- area_id：区域ID
- status：状态（正常，已禁用）
- created_at：创建时间
- updated_at：更新时间

### 教练表（coaches）
- id：教练ID
- name：姓名
- phone：手机号
- email：邮箱
- password：密码
- area_id：区域ID
- status：状态（待确认，正常，已禁用）
- created_at：创建时间
- updated_at：更新时间

### 排课表（schedules）
- id：排课ID
- coach_id：教练ID
- schedule_date：排课日期
- schedule_time：排课时段（上午，下午，晚上）
- student_id：学员ID
- status：状态（待确认，已确认，已取消，已完成）
- created_at：创建时间
- updated_at：更新时间

### 管理员表（admins）
- id：管理员ID
- email：邮箱
- password：密码
- created_at：创建时间
- updated_at：更新时间

## 开发规范

### 1. 代码规范
- 遵循PEP8规范
- 使用4个空格缩进
- 文件名使用小写字母和下划线
- 类名使用驼峰命名法
- 函数名使用小写字母和下划线

### 2. 数据库规范
- 使用DAO模式访问数据库
- 所有数据库操作使用参数化查询
- 避免SQL注入

### 3. API规范
- 使用RESTful风格
- 接口返回统一格式
- 错误处理统一

## 测试

### 单元测试
```bash
pytest tests/ -v
```

### 集成测试
```bash
pytest tests/ --html=report.html
```

## 部署

### 开发环境
```bash
uvicorn main:app --reload
```

### 生产环境
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 版本历史

### V1.0（2023-01-01）
- 初始版本发布
- 支持学员、教练、管理员功能
- 支持排课、约课功能
- 支持区域管理

## 联系方式

- 作者：驾驶陪练系统开发团队
- 邮箱：support@example.com
- 微信：驾驶陪练系统

## 版权声明

**驾驶陪练系统** 版权所有 © 2023