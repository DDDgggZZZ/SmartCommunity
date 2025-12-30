import pymysql
from dbutils.pooled_db import PooledDB
from config import Config

class SQLHelper:
    def __init__(self):
        # 初始化数据库连接池
        self.pool = PooledDB(
            creator=pymysql,  # 使用 pymysql 连接
            maxconnections=10,  # 连接池允许的最大连接数
            mincached=2,       # 初始化时，连接池中至少创建的空闲的连接，0表示不创建
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset=Config.DB_CHARSET,
            cursorclass=pymysql.cursors.DictCursor # ★重要：返回字典格式 {'id':1, 'name':'张三'}
        )

    def fetch_all(self, sql, args=None):
        """查询多条数据"""
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchall() # 获取所有结果
            return result
        except Exception as e:
            print(f"SQL Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close() # 这里不是真的关闭，而是归还给连接池

    def fetch_one(self, sql, args=None):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"SQL Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def execute_commit(self, sql, args=None):
        """执行增删改"""
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            conn.commit() # 提交事务
            return cursor.lastrowid # 返回插入的ID
        except Exception as e:
            conn.rollback() # 出错回滚
            print(f"SQL Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def execute(self, sql, args=None):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            print(f"SQL Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


# 实例化一个对象供外部直接调用
db = SQLHelper()
