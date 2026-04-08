from database import Database
from models import Area, Student, Coach, Schedule, Admin
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import bcrypt

class AreaDAO:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_areas(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM areas ORDER BY created_at DESC"
        return self.db.execute_query(query)
    
    def get_area_by_id(self, area_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM areas WHERE id = ?"
        result = self.db.execute_query(query, (area_id,))
        return result[0] if result else None
    
    def get_area_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM areas WHERE name = ?"
        result = self.db.execute_query(query, (name,))
        return result[0] if result else None
    
    def create_area(self, area: Area) -> bool:
        query = "INSERT INTO areas (name) VALUES (?)"
        return self.db.execute_non_query(query, (area.name,))
    
    def update_area(self, area: Area) -> bool:
        query = "UPDATE areas SET name = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (area.name, datetime.now(), area.id))
    
    def delete_area(self, area_id: int) -> bool:
        query = "DELETE FROM areas WHERE id = ?"
        return self.db.execute_non_query(query, (area_id,))

class StudentDAO:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        query = """
            SELECT s.*, a.name as area_name
            FROM students s
            LEFT JOIN areas a ON s.area_id = a.id
            ORDER BY s.created_at DESC
        """
        return self.db.execute_query(query)
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT s.*, a.name as area_name
            FROM students s
            LEFT JOIN areas a ON s.area_id = a.id
            WHERE s.id = ?
        """
        result = self.db.execute_query(query, (student_id,))
        return result[0] if result else None
    
    def get_student_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT s.*, a.name as area_name
            FROM students s
            LEFT JOIN areas a ON s.area_id = a.id
            WHERE s.phone = ?
        """
        result = self.db.execute_query(query, (phone,))
        return result[0] if result else None
    
    def get_student_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT s.*, a.name as area_name
            FROM students s
            LEFT JOIN areas a ON s.area_id = a.id
            WHERE s.email = ?
        """
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None
    
    def create_student(self, student: Student) -> bool:
        # 加密密码
        hashed_password = bcrypt.hashpw(student.password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO students (name, phone, email, password, area_id) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_non_query(query, (student.name, student.phone, student.email, hashed_password, student.area_id))
    
    def update_student(self, student: Student) -> bool:
        query = "UPDATE students SET name = ?, phone = ?, email = ?, area_id = ?, status = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (student.name, student.phone, student.email, student.area_id, student.status, datetime.now(), student.id))
    
    def update_student_password(self, student_id: int, new_password: str) -> bool:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE students SET password = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (hashed_password, datetime.now(), student_id))
    
    def delete_student(self, student_id: int) -> bool:
        query = "DELETE FROM students WHERE id = ?"
        return self.db.execute_non_query(query, (student_id,))

class CoachDAO:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_coaches(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM coaches ORDER BY created_at DESC"
        return self.db.execute_query(query)
    
    def get_coach_by_id(self, coach_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM coaches WHERE id = ?"
        result = self.db.execute_query(query, (coach_id,))
        return result[0] if result else None
    
    def get_coach_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM coaches WHERE phone = ?"
        result = self.db.execute_query(query, (phone,))
        return result[0] if result else None
    
    def get_coach_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM coaches WHERE email = ?"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None
    
    def create_coach(self, coach: Coach) -> bool:
        # 加密密码
        hashed_password = bcrypt.hashpw(coach.password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO coaches (name, phone, email, password, area_id) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_non_query(query, (coach.name, coach.phone, coach.email, hashed_password, coach.area_id))
    
    def update_coach(self, coach: Coach) -> bool:
        query = "UPDATE coaches SET name = ?, phone = ?, email = ?, area_id = ?, status = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (coach.name, coach.phone, coach.email, coach.area_id, coach.status, datetime.now(), coach.id))
    
    def update_coach_password(self, coach_id: int, new_password: str) -> bool:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE coaches SET password = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (hashed_password, datetime.now(), coach_id))
    
    def delete_coach(self, coach_id: int) -> bool:
        query = "DELETE FROM coaches WHERE id = ?"
        return self.db.execute_non_query(query, (coach_id,))

class ScheduleDAO:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_schedules(self) -> List[Dict[str, Any]]:
        query = """
            SELECT s.*, 
                   c.name as coach_name, c.phone as coach_phone,
                   st.name as student_name, st.phone as student_phone,
                   a.name as area_name
            FROM schedules s
            LEFT JOIN coaches c ON s.coach_id = c.id
            LEFT JOIN students st ON s.student_id = st.id
            LEFT JOIN areas a ON c.area_id = a.id
            ORDER BY s.schedule_date DESC, s.schedule_time ASC
        """
        return self.db.execute_query(query)
    
    def get_schedule_by_id(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM schedules WHERE id = ?"
        result = self.db.execute_query(query, (schedule_id,))
        return result[0] if result else None
    
    def get_schedules_by_coach_id(self, coach_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM schedules WHERE coach_id = ? ORDER BY schedule_date DESC, schedule_time ASC"
        return self.db.execute_query(query, (coach_id,))
    
    def get_schedules_by_student_id(self, student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT s.*, c.name as coach_name, c.phone as coach_phone, a.name as area_name
            FROM schedules s
            JOIN coaches c ON s.coach_id = c.id
            JOIN areas a ON c.area_id = a.id
            WHERE s.student_id = ?
            ORDER BY s.schedule_date DESC, s.schedule_time ASC
        """
        return self.db.execute_query(query, (student_id,))
    
    def get_available_schedules(self, area_id: Optional[int] = None, schedule_date: Optional[date] = None, schedule_time: Optional[str] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT s.*, c.name as coach_name, c.phone as coach_phone, a.name as area_name
            FROM schedules s
            JOIN coaches c ON s.coach_id = c.id
            JOIN areas a ON c.area_id = a.id
            WHERE s.status = '待确认' AND s.student_id IS NULL
        """
        params = []
        
        if area_id:
            query += " AND c.area_id = ?"
            params.append(area_id)
        
        if schedule_date:
            query += " AND s.schedule_date = ?"
            params.append(schedule_date)
        
        if schedule_time:
            query += " AND s.schedule_time = ?"
            params.append(schedule_time)
        
        query += " ORDER BY s.schedule_date DESC, s.schedule_time ASC"
        return self.db.execute_query(query, tuple(params))
    
    def create_schedule(self, schedule: Schedule) -> bool:
        query = "INSERT INTO schedules (coach_id, schedule_date, schedule_time) VALUES (?, ?, ?)"
        return self.db.execute_non_query(query, (schedule.coach_id, schedule.schedule_date, schedule.schedule_time))
    
    def update_schedule(self, schedule: Schedule) -> bool:
        query = "UPDATE schedules SET coach_id = ?, schedule_date = ?, schedule_time = ?, student_id = ?, status = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (schedule.coach_id, schedule.schedule_date, schedule.schedule_time, schedule.student_id, schedule.status, datetime.now(), schedule.id))
    
    def update_schedule_status(self, schedule_id: int, status: str) -> bool:
        query = "UPDATE schedules SET status = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (status, datetime.now(), schedule_id))
    
    def update_schedule_student(self, schedule_id: int, student_id: int) -> bool:
        query = "UPDATE schedules SET student_id = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (student_id, datetime.now(), schedule_id))
    
    def delete_schedule(self, schedule_id: int) -> bool:
        query = "DELETE FROM schedules WHERE id = ?"
        return self.db.execute_non_query(query, (schedule_id,))

class AdminDAO:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all_admins(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM admins ORDER BY created_at DESC"
        return self.db.execute_query(query)
    
    def get_admin_by_id(self, admin_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM admins WHERE id = ?"
        result = self.db.execute_query(query, (admin_id,))
        return result[0] if result else None
    
    def get_admin_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM admins WHERE email = ?"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None
    
    def create_admin(self, admin: Admin) -> bool:
        # 加密密码
        hashed_password = bcrypt.hashpw(admin.password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO admins (email, password) VALUES (?, ?)"
        return self.db.execute_non_query(query, (admin.email, hashed_password))
    
    def update_admin(self, admin: Admin) -> bool:
        query = "UPDATE admins SET email = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (admin.email, datetime.now(), admin.id))
    
    def update_admin_password(self, admin_id: int, new_password: str) -> bool:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE admins SET password = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_non_query(query, (hashed_password, datetime.now(), admin_id))
    
    def delete_admin(self, admin_id: int) -> bool:
        query = "DELETE FROM admins WHERE id = ?"
        return self.db.execute_non_query(query, (admin_id,))