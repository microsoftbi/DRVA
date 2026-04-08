-- 测试数据插入脚本

-- 插入测试学员
INSERT OR IGNORE INTO students (name, phone, email, password, area_id, status) VALUES 
('张三', '13800138001', 'zhangsan@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 1, '正常'),
('李四', '13800138002', 'lisi@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 2, '正常'),
('王五', '13800138003', 'wangwu@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 3, '正常'),
('赵六', '13800138004', 'zhaoliu@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 4, '正常'),
('孙七', '13800138005', 'sunqi@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 5, '正常');

-- 插入测试教练
INSERT OR IGNORE INTO coaches (name, phone, email, password, area_id, status) VALUES 
('王教练', '13900139001', 'wangjiaolian@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 1, '正常'),
('李教练', '13900139002', 'lijiaolian@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 2, '正常'),
('张教练', '13900139003', 'zhangjiaolian@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 3, '正常'),
('刘教练', '13900139004', 'liujiaolian@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 4, '正常'),
('陈教练', '13900139005', 'chenjiaolian@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv', 5, '正常');

-- 插入测试排课（王教练）
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(1, '2023-01-01', '上午', NULL, '待确认'),
(1, '2023-01-01', '下午', NULL, '待确认'),
(1, '2023-01-01', '晚上', NULL, '待确认'),
(1, '2023-01-02', '上午', NULL, '待确认'),
(1, '2023-01-02', '下午', NULL, '待确认'),
(1, '2023-01-03', '上午', NULL, '待确认'),
(1, '2023-01-03', '晚上', NULL, '待确认');

-- 插入测试排课（李教练）
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(2, '2023-01-01', '上午', NULL, '待确认'),
(2, '2023-01-01', '下午', NULL, '待确认'),
(2, '2023-01-02', '上午', NULL, '待确认'),
(2, '2023-01-02', '晚上', NULL, '待确认'),
(2, '2023-01-03', '下午', NULL, '待确认'),
(2, '2023-01-04', '上午', NULL, '待确认');

-- 插入测试排课（张教练）
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(3, '2023-01-01', '上午', NULL, '待确认'),
(3, '2023-01-01', '晚上', NULL, '待确认'),
(3, '2023-01-02', '下午', NULL, '待确认'),
(3, '2023-01-03', '上午', NULL, '待确认'),
(3, '2023-01-03', '下午', NULL, '待确认'),
(3, '2023-01-04', '晚上', NULL, '待确认');

-- 插入测试排课（刘教练）
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(4, '2023-01-01', '下午', NULL, '待确认'),
(4, '2023-01-01', '晚上', NULL, '待确认'),
(4, '2023-01-02', '上午', NULL, '待确认'),
(4, '2023-01-02', '下午', NULL, '待确认'),
(4, '2023-01-03', '晚上', NULL, '待确认'),
(4, '2023-01-04', '上午', NULL, '待确认');

-- 插入测试排课（陈教练）
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(5, '2023-01-01', '上午', NULL, '待确认'),
(5, '2023-01-01', '下午', NULL, '待确认'),
(5, '2023-01-02', '晚上', NULL, '待确认'),
(5, '2023-01-03', '上午', NULL, '待确认'),
(5, '2023-01-03', '下午', NULL, '待确认'),
(5, '2023-01-04', '下午', NULL, '待确认');

-- 插入已预约课程
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(1, '2023-01-01', '上午', 1, '已确认'),
(1, '2023-01-01', '下午', 2, '待确认'),
(2, '2023-01-01', '上午', 3, '已确认'),
(3, '2023-01-01', '晚上', 4, '待确认');

-- 插入已完成课程
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(1, '2022-12-31', '上午', 1, '已完成'),
(1, '2022-12-31', '下午', 2, '已完成'),
(2, '2022-12-31', '上午', 3, '已完成'),
(3, '2022-12-31', '晚上', 4, '已完成');

-- 插入已取消课程
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(1, '2023-01-02', '上午', 1, '已取消'),
(2, '2023-01-02', '下午', 2, '已取消');

-- 插入今日和明日课程
INSERT OR IGNORE INTO schedules (coach_id, schedule_date, schedule_time, student_id, status) VALUES 
(1, date('now'), '上午', NULL, '待确认'),
(1, date('now'), '下午', NULL, '待确认'),
(1, date('now'), '晚上', NULL, '待确认'),
(1, date('now', '+1 day'), '上午', NULL, '待确认'),
(1, date('now', '+1 day'), '下午', NULL, '待确认'),
(2, date('now'), '上午', NULL, '待确认'),
(2, date('now'), '晚上', NULL, '待确认'),
(2, date('now', '+1 day'), '下午', NULL, '待确认'),
(3, date('now'), '下午', NULL, '待确认'),
(3, date('now', '+1 day'), '上午', NULL, '待确认');