import bcrypt

# 测试密码加密和验证
password = "123456"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"原始密码: {password}")
print(f"加密后密码: {hashed_password}")

# 测试验证
result = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
print(f"验证结果: {result}")

# 测试字符串密码验证（模拟数据库中存储的是字符串）
str_password = hashed_password.decode('utf-8')
print(f"字符串密码: {str_password}")
result2 = bcrypt.checkpw(password.encode('utf-8'), str_password.encode('utf-8'))
print(f"字符串密码验证结果: {result2}")