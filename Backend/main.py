from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import Area, Student, Coach, Schedule, Admin, LoginRequest, RegisterRequest, ScheduleRequest, ResponseModel
from services import AreaService, StudentService, CoachService, ScheduleService, AdminService
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
import uvicorn
import jwt
import hashlib

app = FastAPI(title="驾驶陪练系统", description="驾驶陪练系统API接口", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全认证
security = HTTPBearer()

# JWT配置
SECRET_KEY = "DRVA_SECRET_KEY_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 区域接口
@app.get("/api/areas", response_model=ResponseModel, summary="获取所有区域")
async def get_all_areas():
    try:
        area_service = AreaService()
        areas = area_service.get_all_areas()
        return ResponseModel(success=True, message="获取成功", data={"areas": areas})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/areas/{area_id}", response_model=ResponseModel, summary="根据ID获取区域")
async def get_area_by_id(area_id: int):
    try:
        area_service = AreaService()
        area = area_service.get_area_by_id(area_id)
        if not area:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="区域不存在")
        return ResponseModel(success=True, message="获取成功", data={"area": area})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/areas", response_model=ResponseModel, summary="创建区域")
async def create_area(area: Area):
    try:
        area_service = AreaService()
        success = area_service.create_area(area)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建失败")
        return ResponseModel(success=True, message="创建成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/areas/{area_id}", response_model=ResponseModel, summary="更新区域")
async def update_area(area_id: int, area: Area):
    try:
        area.id = area_id
        area_service = AreaService()
        success = area_service.update_area(area)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/api/areas/{area_id}", response_model=ResponseModel, summary="删除区域")
async def delete_area(area_id: int):
    try:
        area_service = AreaService()
        success = area_service.delete_area(area_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
        return ResponseModel(success=True, message="删除成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 学员接口
@app.get("/api/students", response_model=ResponseModel, summary="获取所有学员")
async def get_all_students():
    try:
        student_service = StudentService()
        students = student_service.get_all_students()
        return ResponseModel(success=True, message="获取成功", data={"students": students})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/students/{student_id}", response_model=ResponseModel, summary="根据ID获取学员")
async def get_student_by_id(student_id: int):
    try:
        student_service = StudentService()
        student = student_service.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学员不存在")
        return ResponseModel(success=True, message="获取成功", data={"student": student})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/students/register", response_model=ResponseModel, summary="学员注册")
async def register_student(student: Student):
    try:
        student_service = StudentService()
        success = student_service.register_student(student)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="注册失败")
        return ResponseModel(success=True, message="注册成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/students/login", response_model=ResponseModel, summary="学员登录")
async def login_student(login_request: LoginRequest):
    try:
        student_service = StudentService()
        student = student_service.login_student(login_request.phone, login_request.password)
        if not student:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失败")
        token = create_token({"sub": str(student['id']), "role": "student"})
        return ResponseModel(success=True, message="登录成功", data={"user": student, "token": token})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/students/{student_id}", response_model=ResponseModel, summary="更新学员")
async def update_student(student_id: int, student: Student):
    try:
        student.id = student_id
        student_service = StudentService()
        success = student_service.update_student(student)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/students/{student_id}/password", response_model=ResponseModel, summary="更新学员密码")
async def update_student_password(student_id: int, old_password: str, new_password: str):
    try:
        student_service = StudentService()
        success = student_service.update_student_password(student_id, old_password, new_password)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/students/{student_id}/reset-password", response_model=ResponseModel, summary="重置学员密码")
async def reset_student_password(student_id: int, new_password: str):
    try:
        student_service = StudentService()
        success = student_service.reset_student_password(student_id, new_password)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="重置失败")
        return ResponseModel(success=True, message="重置成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/api/students/{student_id}", response_model=ResponseModel, summary="删除学员")
async def delete_student(student_id: int):
    try:
        student_service = StudentService()
        success = student_service.delete_student(student_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
        return ResponseModel(success=True, message="删除成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 教练接口
@app.get("/api/coaches", response_model=ResponseModel, summary="获取所有教练")
async def get_all_coaches():
    try:
        coach_service = CoachService()
        coaches = coach_service.get_all_coaches()
        return ResponseModel(success=True, message="获取成功", data={"coaches": coaches})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/coaches/{coach_id}", response_model=ResponseModel, summary="根据ID获取教练")
async def get_coach_by_id(coach_id: int):
    try:
        coach_service = CoachService()
        coach = coach_service.get_coach_by_id(coach_id)
        if not coach:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="教练不存在")
        return ResponseModel(success=True, message="获取成功", data={"coach": coach})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/coaches/register", response_model=ResponseModel, summary="教练注册")
async def register_coach(coach: Coach):
    try:
        coach_service = CoachService()
        success = coach_service.register_coach(coach)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="注册失败")
        return ResponseModel(success=True, message="注册成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/coaches/login", response_model=ResponseModel, summary="教练登录")
async def login_coach(login_request: LoginRequest):
    try:
        coach_service = CoachService()
        coach = coach_service.login_coach(login_request.phone, login_request.password)
        if not coach:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失败")
        token = create_token({"sub": str(coach['id']), "role": "coach"})
        return ResponseModel(success=True, message="登录成功", data={"user": coach, "token": token})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/coaches/{coach_id}", response_model=ResponseModel, summary="更新教练")
async def update_coach(coach_id: int, coach: Coach):
    try:
        coach.id = coach_id
        coach_service = CoachService()
        success = coach_service.update_coach(coach)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/coaches/{coach_id}/password", response_model=ResponseModel, summary="更新教练密码")
async def update_coach_password(coach_id: int, old_password: str, new_password: str):
    try:
        coach_service = CoachService()
        success = coach_service.update_coach_password(coach_id, old_password, new_password)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/coaches/{coach_id}/reset-password", response_model=ResponseModel, summary="重置教练密码")
async def reset_coach_password(coach_id: int, new_password: str):
    try:
        coach_service = CoachService()
        success = coach_service.reset_coach_password(coach_id, new_password)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="重置失败")
        return ResponseModel(success=True, message="重置成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/api/coaches/{coach_id}", response_model=ResponseModel, summary="删除教练")
async def delete_coach(coach_id: int):
    try:
        coach_service = CoachService()
        success = coach_service.delete_coach(coach_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
        return ResponseModel(success=True, message="删除成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 排课接口
@app.get("/api/schedules", response_model=ResponseModel, summary="获取所有排课")
async def get_all_schedules():
    try:
        schedule_service = ScheduleService()
        schedules = schedule_service.get_all_schedules()
        return ResponseModel(success=True, message="获取成功", data={"schedules": schedules})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/schedules/available", response_model=ResponseModel, summary="获取可用排课")
async def get_available_schedules(area_id: Optional[int] = None, schedule_date: Optional[date] = None, schedule_time: Optional[str] = None):
    try:
        schedule_service = ScheduleService()
        schedules = schedule_service.get_available_schedules(area_id, schedule_date, schedule_time)
        return ResponseModel(success=True, message="获取成功", data={"schedules": schedules})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/schedules/{schedule_id}", response_model=ResponseModel, summary="根据ID获取排课")
async def get_schedule_by_id(schedule_id: int):
    try:
        schedule_service = ScheduleService()
        schedule = schedule_service.get_schedule_by_id(schedule_id)
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="排课不存在")
        return ResponseModel(success=True, message="获取成功", data={"schedule": schedule})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/schedules/coach/{coach_id}", response_model=ResponseModel, summary="根据教练ID获取排课")
async def get_schedules_by_coach_id(coach_id: int):
    try:
        schedule_service = ScheduleService()
        schedules = schedule_service.get_schedules_by_coach_id(coach_id)
        return ResponseModel(success=True, message="获取成功", data={"schedules": schedules})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/schedules/student/{student_id}", response_model=ResponseModel, summary="根据学员ID获取排课")
async def get_schedules_by_student_id(student_id: int):
    try:
        schedule_service = ScheduleService()
        schedules = schedule_service.get_schedules_by_student_id(student_id)
        return ResponseModel(success=True, message="获取成功", data={"schedules": schedules})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/schedules", response_model=ResponseModel, summary="创建排课")
async def create_schedule(schedule: Schedule):
    try:
        schedule_service = ScheduleService()
        success = schedule_service.create_schedule(schedule)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建失败")
        return ResponseModel(success=True, message="创建成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/schedules/{schedule_id}", response_model=ResponseModel, summary="更新排课")
async def update_schedule(schedule_id: int, schedule: Schedule):
    try:
        schedule.id = schedule_id
        schedule_service = ScheduleService()
        success = schedule_service.update_schedule(schedule)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/schedules/{schedule_id}/book", response_model=ResponseModel, summary="预约排课")
async def book_schedule(schedule_id: int, student_id: int):
    try:
        schedule_service = ScheduleService()
        success = schedule_service.book_schedule(schedule_id, student_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="预约失败")
        return ResponseModel(success=True, message="预约成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/schedules/{schedule_id}/confirm", response_model=ResponseModel, summary="确认排课")
async def confirm_schedule(schedule_id: int):
    try:
        schedule_service = ScheduleService()
        success = schedule_service.confirm_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="确认失败")
        return ResponseModel(success=True, message="确认成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/schedules/{schedule_id}/cancel", response_model=ResponseModel, summary="取消排课")
async def cancel_schedule(schedule_id: int):
    try:
        schedule_service = ScheduleService()
        success = schedule_service.cancel_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="取消失败")
        return ResponseModel(success=True, message="取消成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/schedules/{schedule_id}/complete", response_model=ResponseModel, summary="标记排课完成")
async def complete_schedule(schedule_id: int):
    try:
        schedule_service = ScheduleService()
        success = schedule_service.complete_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="标记失败")
        return ResponseModel(success=True, message="标记成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/api/schedules/{schedule_id}", response_model=ResponseModel, summary="删除排课")
async def delete_schedule(schedule_id: int):
    try:
        schedule_service = ScheduleService()
        success = schedule_service.delete_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
        return ResponseModel(success=True, message="删除成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 管理员接口
@app.get("/api/admins", response_model=ResponseModel, summary="获取所有管理员")
async def get_all_admins():
    try:
        admin_service = AdminService()
        admins = admin_service.get_all_admins()
        return ResponseModel(success=True, message="获取成功", data={"admins": admins})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/admins/{admin_id}", response_model=ResponseModel, summary="根据ID获取管理员")
async def get_admin_by_id(admin_id: int):
    try:
        admin_service = AdminService()
        admin = admin_service.get_admin_by_id(admin_id)
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="管理员不存在")
        return ResponseModel(success=True, message="获取成功", data={"admin": admin})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/admins/login", response_model=ResponseModel, summary="管理员登录")
async def login_admin(login_request: LoginRequest):
    try:
        admin_service = AdminService()
        admin = admin_service.login_admin(login_request.email, login_request.password)
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失败")
        token = create_token({"sub": str(admin['id']), "role": "admin"})
        return ResponseModel(success=True, message="登录成功", data={"user": admin, "token": token})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/admins/{admin_id}", response_model=ResponseModel, summary="更新管理员")
async def update_admin(admin_id: int, admin: Admin):
    try:
        admin.id = admin_id
        admin_service = AdminService()
        success = admin_service.update_admin(admin)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/api/admins/{admin_id}/password", response_model=ResponseModel, summary="更新管理员密码")
async def update_admin_password(admin_id: int, old_password: str, new_password: str):
    try:
        admin_service = AdminService()
        success = admin_service.update_admin_password(admin_id, old_password, new_password)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="更新失败")
        return ResponseModel(success=True, message="更新成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/api/admins/{admin_id}", response_model=ResponseModel, summary="删除管理员")
async def delete_admin(admin_id: int):
    try:
        admin_service = AdminService()
        success = admin_service.delete_admin(admin_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
        return ResponseModel(success=True, message="删除成功")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 健康检查
@app.get("/health", summary="健康检查")
async def health_check():
    return {"status": "ok", "message": "系统运行正常"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)