
from database import Database
from services import StudentService, AdminService
import bcrypt

db = Database()

print("=== 测试学员登录 ===")
try:
    student_service = StudentService()
    # 测试张三登录
    student = student_service.login_student('13800138001', '123456')
    if student:
        print(f"学员登录成功: {student['name']}")
    else:
        print("学员登录失败")
except Exception as e:
    print(f"学员登录错误: {e}")

print("\n=== 测试管理员登录 ===")
try:
    admin_service = AdminService()
    admin = admin_service.login_admin('admin@example.com', 'admin')
    if admin:
        print(f"管理员登录成功: {admin['email']}")
    else:
        print("管理员登录失败")
except Exception as e:
    print(f"管理员登录错误: {e}")

db.disconnect()
