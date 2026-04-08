from dao import AreaDAO, StudentDAO, CoachDAO, ScheduleDAO, AdminDAO
from models import Area, Student, Coach, Schedule, Admin, LoginRequest, RegisterRequest, ScheduleRequest
from database import Database
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import bcrypt

class AreaService:
    def __init__(self):
        self.db = Database()
        self.area_dao = AreaDAO(self.db)
    
    def get_all_areas(self) -> List[Dict[str, Any]]:
        return self.area_dao.get_all_areas()
    
    def get_area_by_id(self, area_id: int) -> Optional[Dict[str, Any]]:
        return self.area_dao.get_area_by_id(area_id)
    
    def create_area(self, area: Area) -> bool:
        # 检查区域是否已存在
        existing_area = self.area_dao.get_area_by_name(area.name)
        if existing_area:
            raise ValueError("区域已存在")
        return self.area_dao.create_area(area)
    
    def update_area(self, area: Area) -> bool:
        # 检查区域是否存在
        existing_area = self.area_dao.get_area_by_id(area.id)
        if not existing_area:
            raise ValueError("区域不存在")
        # 检查区域名称是否已存在
        area_with_same_name = self.area_dao.get_area_by_name(area.name)
        if area_with_same_name and area_with_same_name['id'] != area.id:
            raise ValueError("区域名称已存在")
        return self.area_dao.update_area(area)
    
    def delete_area(self, area_id: int) -> bool:
        # 检查区域是否存在
        existing_area = self.area_dao.get_area_by_id(area_id)
        if not existing_area:
            raise ValueError("区域不存在")
        return self.area_dao.delete_area(area_id)

class StudentService:
    def __init__(self):
        self.db = Database()
        self.student_dao = StudentDAO(self.db)
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        return self.student_dao.get_all_students()
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        return self.student_dao.get_student_by_id(student_id)
    
    def get_student_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        return self.student_dao.get_student_by_phone(phone)
    
    def register_student(self, student: Student) -> bool:
        # 检查手机号是否已存在
        existing_student = self.student_dao.get_student_by_phone(student.phone)
        if existing_student:
            raise ValueError("手机号已存在")
        # 检查邮箱是否已存在
        if student.email:
            existing_student_by_email = self.student_dao.get_student_by_email(student.email)
            if existing_student_by_email:
                raise ValueError("邮箱已存在")
        return self.student_dao.create_student(student)
    
    def login_student(self, phone: str, password: str) -> Optional[Dict[str, Any]]:
        # 检查学员是否存在
        student = self.student_dao.get_student_by_phone(phone)
        if not student:
            raise ValueError("学员不存在")
        # 检查密码是否正确
        try:
            if isinstance(student['password'], str):
                hashed_password = student['password'].encode('utf-8')
            else:
                hashed_password = student['password']
            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                raise ValueError("密码错误")
        except Exception as e:
            print(f"密码验证错误: {e}")
            raise ValueError("密码错误")
        # 检查学员状态
        if student['status'] != '正常':
            raise ValueError("学员已禁用")
        return student
    
    def update_student(self, student: Student) -> bool:
        # 检查学员是否存在
        existing_student = self.student_dao.get_student_by_id(student.id)
        if not existing_student:
            raise ValueError("学员不存在")
        # 检查手机号是否已存在
        student_with_same_phone = self.student_dao.get_student_by_phone(student.phone)
        if student_with_same_phone and student_with_same_phone['id'] != student.id:
            raise ValueError("手机号已存在")
        # 检查邮箱是否已存在
        if student.email:
            student_with_same_email = self.student_dao.get_student_by_email(student.email)
            if student_with_same_email and student_with_same_email['id'] != student.id:
                raise ValueError("邮箱已存在")
        return self.student_dao.update_student(student)
    
    def update_student_password(self, student_id: int, old_password: str, new_password: str) -> bool:
        # 检查学员是否存在
        student = self.student_dao.get_student_by_id(student_id)
        if not student:
            raise ValueError("学员不存在")
        # 检查旧密码是否正确
        if not bcrypt.checkpw(old_password.encode('utf-8'), student['password']):
            raise ValueError("旧密码错误")
        return self.student_dao.update_student_password(student_id, new_password)
    
    def reset_student_password(self, student_id: int, new_password: str) -> bool:
        # 检查学员是否存在
        student = self.student_dao.get_student_by_id(student_id)
        if not student:
            raise ValueError("学员不存在")
        return self.student_dao.update_student_password(student_id, new_password)
    
    def delete_student(self, student_id: int) -> bool:
        # 检查学员是否存在
        existing_student = self.student_dao.get_student_by_id(student_id)
        if not existing_student:
            raise ValueError("学员不存在")
        return self.student_dao.delete_student(student_id)

class CoachService:
    def __init__(self):
        self.db = Database()
        self.coach_dao = CoachDAO(self.db)
    
    def get_all_coaches(self) -> List[Dict[str, Any]]:
        return self.coach_dao.get_all_coaches()
    
    def get_coach_by_id(self, coach_id: int) -> Optional[Dict[str, Any]]:
        return self.coach_dao.get_coach_by_id(coach_id)
    
    def get_coach_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        return self.coach_dao.get_coach_by_phone(phone)
    
    def register_coach(self, coach: Coach) -> bool:
        # 检查手机号是否已存在
        existing_coach = self.coach_dao.get_coach_by_phone(coach.phone)
        if existing_coach:
            raise ValueError("手机号已存在")
        # 检查邮箱是否已存在
        if coach.email:
            existing_coach_by_email = self.coach_dao.get_coach_by_email(coach.email)
            if existing_coach_by_email:
                raise ValueError("邮箱已存在")
        return self.coach_dao.create_coach(coach)
    
    def login_coach(self, phone: str, password: str) -> Optional[Dict[str, Any]]:
        # 检查教练是否存在
        coach = self.coach_dao.get_coach_by_phone(phone)
        if not coach:
            raise ValueError("教练不存在")
        # 检查密码是否正确
        if isinstance(coach['password'], str):
            coach['password'] = coach['password'].encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), coach['password']):
            raise ValueError("密码错误")
        # 检查教练状态
        if coach['status'] != '正常':
            raise ValueError("教练已禁用")
        return coach
    
    def update_coach(self, coach: Coach) -> bool:
        # 检查教练是否存在
        existing_coach = self.coach_dao.get_coach_by_id(coach.id)
        if not existing_coach:
            raise ValueError("教练不存在")
        # 检查手机号是否已存在
        coach_with_same_phone = self.coach_dao.get_coach_by_phone(coach.phone)
        if coach_with_same_phone and coach_with_same_phone['id'] != coach.id:
            raise ValueError("手机号已存在")
        # 检查邮箱是否已存在
        if coach.email:
            coach_with_same_email = self.coach_dao.get_coach_by_email(coach.email)
            if coach_with_same_email and coach_with_same_email['id'] != coach.id:
                raise ValueError("邮箱已存在")
        return self.coach_dao.update_coach(coach)
    
    def update_coach_password(self, coach_id: int, old_password: str, new_password: str) -> bool:
        # 检查教练是否存在
        coach = self.coach_dao.get_coach_by_id(coach_id)
        if not coach:
            raise ValueError("教练不存在")
        # 检查旧密码是否正确
        if not bcrypt.checkpw(old_password.encode('utf-8'), coach['password']):
            raise ValueError("旧密码错误")
        return self.coach_dao.update_coach_password(coach_id, new_password)
    
    def reset_coach_password(self, coach_id: int, new_password: str) -> bool:
        # 检查教练是否存在
        coach = self.coach_dao.get_coach_by_id(coach_id)
        if not coach:
            raise ValueError("教练不存在")
        return self.coach_dao.update_coach_password(coach_id, new_password)
    
    def delete_coach(self, coach_id: int) -> bool:
        # 检查教练是否存在
        existing_coach = self.coach_dao.get_coach_by_id(coach_id)
        if not existing_coach:
            raise ValueError("教练不存在")
        return self.coach_dao.delete_coach(coach_id)

class ScheduleService:
    def __init__(self):
        self.db = Database()
        self.schedule_dao = ScheduleDAO(self.db)
    
    def get_all_schedules(self) -> List[Dict[str, Any]]:
        return self.schedule_dao.get_all_schedules()
    
    def get_schedule_by_id(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        return self.schedule_dao.get_schedule_by_id(schedule_id)
    
    def get_schedules_by_coach_id(self, coach_id: int) -> List[Dict[str, Any]]:
        return self.schedule_dao.get_schedules_by_coach_id(coach_id)
    
    def get_schedules_by_student_id(self, student_id: int) -> List[Dict[str, Any]]:
        return self.schedule_dao.get_schedules_by_student_id(student_id)
    
    def get_available_schedules(self, area_id: Optional[int] = None, schedule_date: Optional[date] = None, schedule_time: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.schedule_dao.get_available_schedules(area_id, schedule_date, schedule_time)
    
    def create_schedule(self, schedule: Schedule) -> bool:
        # 检查教练是否存在
        coach_service = CoachService()
        coach = coach_service.get_coach_by_id(schedule.coach_id)
        if not coach:
            raise ValueError("教练不存在")
        # 检查教练状态
        if coach['status'] != '正常':
            raise ValueError("教练未通过审核或已禁用")
        return self.schedule_dao.create_schedule(schedule)
    
    def update_schedule(self, schedule: Schedule) -> bool:
        # 检查排课是否存在
        existing_schedule = self.schedule_dao.get_schedule_by_id(schedule.id)
        if not existing_schedule:
            raise ValueError("排课不存在")
        # 检查教练是否存在
        coach_service = CoachService()
        coach = coach_service.get_coach_by_id(schedule.coach_id)
        if not coach:
            raise ValueError("教练不存在")
        # 检查教练状态
        if coach['status'] != '正常':
            raise ValueError("教练未通过审核或已禁用")
        return self.schedule_dao.update_schedule(schedule)
    
    def book_schedule(self, schedule_id: int, student_id: int) -> bool:
        # 检查排课是否存在
        schedule = self.schedule_dao.get_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError("排课不存在")
        # 检查排课状态
        if schedule['status'] != '待确认':
            raise ValueError("排课不可预约")
        # 检查学员是否存在
        student_service = StudentService()
        student = student_service.get_student_by_id(student_id)
        if not student:
            raise ValueError("学员不存在")
        # 检查学员状态
        if student['status'] != '正常':
            raise ValueError("学员已禁用")
        # 更新排课状态和学员ID
        self.schedule_dao.update_schedule_student(schedule_id, student_id)
        return self.schedule_dao.update_schedule_status(schedule_id, '待确认')
    
    def confirm_schedule(self, schedule_id: int) -> bool:
        # 检查排课是否存在
        schedule = self.schedule_dao.get_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError("排课不存在")
        # 检查排课状态
        if schedule['status'] != '待确认':
            raise ValueError("排课不可确认")
        return self.schedule_dao.update_schedule_status(schedule_id, '已确认')
    
    def cancel_schedule(self, schedule_id: int) -> bool:
        # 检查排课是否存在
        schedule = self.schedule_dao.get_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError("排课不存在")
        # 检查排课状态
        if schedule['status'] not in ['待确认', '已确认']:
            raise ValueError("排课不可取消")
        # 清空学员ID
        self.schedule_dao.update_schedule_student(schedule_id, None)
        return self.schedule_dao.update_schedule_status(schedule_id, '已取消')
    
    def complete_schedule(self, schedule_id: int) -> bool:
        # 检查排课是否存在
        schedule = self.schedule_dao.get_schedule_by_id(schedule_id)
        if not schedule:
            raise ValueError("排课不存在")
        # 检查排课状态
        if schedule['status'] != '已确认':
            raise ValueError("排课不可标记为完成")
        return self.schedule_dao.update_schedule_status(schedule_id, '已完成')
    
    def delete_schedule(self, schedule_id: int) -> bool:
        # 检查排课是否存在
        existing_schedule = self.schedule_dao.get_schedule_by_id(schedule_id)
        if not existing_schedule:
            raise ValueError("排课不存在")
        return self.schedule_dao.delete_schedule(schedule_id)

class AdminService:
    def __init__(self):
        self.db = Database()
        self.admin_dao = AdminDAO(self.db)
    
    def get_all_admins(self) -> List[Dict[str, Any]]:
        return self.admin_dao.get_all_admins()
    
    def get_admin_by_id(self, admin_id: int) -> Optional[Dict[str, Any]]:
        return self.admin_dao.get_admin_by_id(admin_id)
    
    def get_admin_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.admin_dao.get_admin_by_email(email)
    
    def login_admin(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        # 检查管理员是否存在
        admin = self.admin_dao.get_admin_by_email(email)
        if not admin:
            raise ValueError("管理员不存在")
        # 检查密码是否正确
        if isinstance(admin['password'], str):
            admin['password'] = admin['password'].encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), admin['password']):
            raise ValueError("密码错误")
        return admin
    
    def update_admin(self, admin: Admin) -> bool:
        # 检查管理员是否存在
        existing_admin = self.admin_dao.get_admin_by_id(admin.id)
        if not existing_admin:
            raise ValueError("管理员不存在")
        # 检查邮箱是否已存在
        admin_with_same_email = self.admin_dao.get_admin_by_email(admin.email)
        if admin_with_same_email and admin_with_same_email['id'] != admin.id:
            raise ValueError("邮箱已存在")
        return self.admin_dao.update_admin(admin)
    
    def update_admin_password(self, admin_id: int, old_password: str, new_password: str) -> bool:
        # 检查管理员是否存在
        admin = self.admin_dao.get_admin_by_id(admin_id)
        if not admin:
            raise ValueError("管理员不存在")
        # 检查旧密码是否正确
        if not bcrypt.checkpw(old_password.encode('utf-8'), admin['password']):
            raise ValueError("旧密码错误")
        return self.admin_dao.update_admin_password(admin_id, new_password)
    
    def delete_admin(self, admin_id: int) -> bool:
        # 检查管理员是否存在
        existing_admin = self.admin_dao.get_admin_by_id(admin_id)
        if not existing_admin:
            raise ValueError("管理员不存在")
        return self.admin_dao.delete_admin(admin_id)