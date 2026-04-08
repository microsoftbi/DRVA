
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime

# 区域模型
class Area(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 学员模型
class Student(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=11, max_length=20)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)
    area_id: int = Field(..., gt=0)
    status: str = Field(default="正常")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 教练模型
class Coach(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=11, max_length=20)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)
    area_id: int = Field(..., gt=0)
    status: str = Field(default="待确认")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 排课模型
class Schedule(BaseModel):
    id: Optional[int] = None
    coach_id: int = Field(..., gt=0)
    schedule_date: date = Field(...)
    schedule_time: str = Field(..., pattern="^(上午|下午|晚上)$")
    student_id: Optional[int] = None
    status: str = Field(default="待确认")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 管理员模型
class Admin(BaseModel):
    id: Optional[int] = None
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 登录请求模型
class LoginRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)

# 注册请求模型
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=11, max_length=20)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)
    area_id: int = Field(..., gt=0)

# 排课请求模型
class ScheduleRequest(BaseModel):
    schedule_date: date = Field(...)
    schedule_time: str = Field(..., pattern="^(上午|下午|晚上)$")

# 响应模型
class ResponseModel(BaseModel):
    success: bool = Field(default=True)
    message: str = Field(default="操作成功")
    data: Optional[dict] = None
    
    class Config:
        from_attributes = True
