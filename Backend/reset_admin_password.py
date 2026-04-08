
from database import Database
import bcrypt

db = Database()

print("=== 重置管理员密码 ===")

# 重置管理员密码为 adminadmin
admin_pwd = bcrypt.hashpw(b'adminadmin', bcrypt.gensalt())
db.execute_non_query("UPDATE admins SET password = ? WHERE id = 1", (admin_pwd,))

print("管理员密码已重置为: adminadmin")
print("登录账号: admin@example.com")

db.disconnect()
