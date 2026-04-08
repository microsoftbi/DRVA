
from database import Database
from services import StudentService
import bcrypt

db = Database()

print("=== 检查学员数据 ===")
students = db.execute_query("SELECT id, name, phone, status FROM students")
for student in students:
    print(student)

print("\n=== 重置学员密码为 123456 ===")
hashed_pwd = bcrypt.hashpw(b'123456', bcrypt.gensalt())
db.execute_non_query("UPDATE students SET password = ? WHERE id = 1", (hashed_pwd,))
db.execute_non_query("UPDATE students SET password = ? WHERE id = 2", (hashed_pwd,))
print("学员密码已重置为: 123456")

print("\n=== 测试学员登录 ===")
try:
    student_service = StudentService()
    student = student_service.login_student('13800138001', '123456')
    if student:
        print(f"学员登录成功: {student['name']}")
    else:
        print("学员登录失败")
except Exception as e:
    print(f"学员登录错误: {e}")

db.disconnect()
