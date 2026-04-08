
from database import Database
import os

print("当前工作目录:", os.getcwd())
print("脚本所在目录:", os.path.dirname(os.path.abspath(__file__)))

db = Database()
print("\n数据库连接成功")

print("\n=== 检查学员数据 ===")
students = db.execute_query("SELECT id, name, phone, status FROM students")
for student in students:
    print(student)

print("\n=== 检查管理员数据 ===")
admins = db.execute_query("SELECT * FROM admins")
for admin in admins:
    print(admin)

db.disconnect()
