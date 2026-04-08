import bcrypt
import sqlite3

# 连接数据库
conn = sqlite3.connect('drva.db')
cursor = conn.cursor()

# 重置所有学员密码为123456
students = cursor.execute("SELECT id, name FROM students").fetchall()
for student in students:
    student_id, name = student
    hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE students SET password = ? WHERE id = ?", (hashed_password, student_id))
    print(f"重置学员 {name} 的密码为123456")

# 重置所有教练密码为123456
coaches = cursor.execute("SELECT id, name FROM coaches").fetchall()
for coach in coaches:
    coach_id, name = coach
    hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE coaches SET password = ? WHERE id = ?", (hashed_password, coach_id))
    print(f"重置教练 {name} 的密码为123456")

# 重置管理员密码为admin
admins = cursor.execute("SELECT id, email FROM admins").fetchall()
for admin in admins:
    admin_id, email = admin
    hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE admins SET password = ? WHERE id = ?", (hashed_password, admin_id))
    print(f"重置管理员 {email} 的密码为admin")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("所有密码重置完成！")