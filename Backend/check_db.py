
from database import Database
import bcrypt

db = Database()

print("=== 学员数据 ===")
students = db.execute_query("SELECT id, name, phone, status FROM students")
for student in students:
    print(student)

print("\n=== 管理员表结构 ===")
admin_columns = db.execute_query("PRAGMA table_info(admins)")
for col in admin_columns:
    print(col)

print("\n=== 管理员数据 ===")
admins = db.execute_query("SELECT * FROM admins")
for admin in admins:
    print(admin)

print("\n=== 重置学员和管理员密码 ===")

# 重置学员密码为 123456
hashed_pwd = bcrypt.hashpw(b'123456', bcrypt.gensalt())
db.execute_non_query("UPDATE students SET password = ? WHERE id = 1", (hashed_pwd,))
db.execute_non_query("UPDATE students SET password = ? WHERE id = 2", (hashed_pwd,))
print("学员密码已重置为: 123456")

# 检查并重置管理员账号
if not admins:
    print("没有管理员，创建默认管理员...")
    admin_pwd = bcrypt.hashpw(b'admin', bcrypt.gensalt())
    db.execute_non_query("INSERT INTO admins (email, password, name) VALUES (?, ?, ?)", 
                        ('admin@example.com', admin_pwd, '系统管理员'))
    print("管理员创建成功: admin@example.com / admin")
else:
    admin_pwd = bcrypt.hashpw(b'admin', bcrypt.gensalt())
    db.execute_non_query("UPDATE admins SET password = ? WHERE id = 1", (admin_pwd,))
    print("管理员密码已重置为: admin")

db.disconnect()
print("\n完成！")
