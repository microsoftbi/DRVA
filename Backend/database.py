import sqlite3
from typing import List, Dict, Any
from datetime import datetime
import os

class Database:
    def __init__(self, db_name: str = 'drva.db'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(script_dir, db_name)
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            print("Database connected successfully")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Database disconnected successfully")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return []
    
    def execute_non_query(self, query: str, params: tuple = ()) -> bool:
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Non-query execution error: {e}")
            self.connection.rollback()
            return False
    
    def get_last_insert_id(self) -> int:
        return self.cursor.lastrowid
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# 示例使用
if __name__ == "__main__":
    db = Database()
    
    # 测试查询区域
    areas = db.execute_query("SELECT * FROM areas")
    print("Areas:", areas)
    
    # 测试查询管理员
    admins = db.execute_query("SELECT * FROM admins")
    print("Admins:", admins)
    
    db.disconnect()