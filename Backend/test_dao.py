from database import Database
from dao import StudentDAO

# 测试数据库连接和DAO
db = Database()
student_dao = StudentDAO(db)

# 测试获取学员
student = student_dao.get_student_by_phone('13800138001')
print(f"学员信息: {student}")

if student:
    print(f"学员ID: {student['id']}")
    print(f"姓名: {student['name']}")
    print(f"手机号: {student['phone']}")
    print(f"邮箱: {student['email']}")
    print(f"区域ID: {student['area_id']}")
    print(f"状态: {student['status']}")