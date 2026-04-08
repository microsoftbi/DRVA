-- 驾驶陪练系统数据库表结构

-- 创建区域表
CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建学员表
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    area_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT '正常',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (area_id) REFERENCES areas(id)
);

-- 创建教练表
CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    area_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT '待确认',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (area_id) REFERENCES areas(id)
);

-- 创建排课表
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coach_id INTEGER NOT NULL,
    schedule_date DATE NOT NULL,
    schedule_time VARCHAR(20) NOT NULL,
    student_id INTEGER,
    status VARCHAR(20) DEFAULT '待确认',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coach_id) REFERENCES coaches(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- 创建管理员表
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认管理员账号 (admin/admin)
INSERT OR IGNORE INTO admins (email, password) VALUES ('admin@example.com', '$2b$12$EixZaY8W68o2BqTn9dX30O6eQbFgX8yOvX8yOvX8yOvX8yOvX8yOv');

-- 插入默认区域数据
INSERT OR IGNORE INTO areas (name) VALUES ('北京市朝阳区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市海淀区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市西城区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市东城区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市丰台区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市石景山区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市通州区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市昌平区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市顺义区');
INSERT OR IGNORE INTO areas (name) VALUES ('北京市大兴区');

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_students_phone ON students(phone);
CREATE INDEX IF NOT EXISTS idx_coaches_phone ON coaches(phone);
CREATE INDEX IF NOT EXISTS idx_schedules_coach_id ON schedules(coach_id);
CREATE INDEX IF NOT EXISTS idx_schedules_student_id ON schedules(student_id);
CREATE INDEX IF NOT EXISTS idx_schedules_date ON schedules(schedule_date);
CREATE INDEX IF NOT EXISTS idx_schedules_time ON schedules(schedule_time);