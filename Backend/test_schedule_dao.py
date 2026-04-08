from database import Database
from dao import ScheduleDAO

# 测试ScheduleDAO
db = Database()
schedule_dao = ScheduleDAO(db)

# 测试获取可用排课
schedules = schedule_dao.get_available_schedules(None, None, None)
print(f"可用排课数量: {len(schedules)}")
if schedules:
    print(f"第一个排课: {schedules[0]}")

# 测试获取区域1的排课
schedules_area1 = schedule_dao.get_available_schedules(1, None, None)
print(f"\n区域1可用排课数量: {len(schedules_area1)}")
if schedules_area1:
    print(f"区域1第一个排课: {schedules_area1[0]}")