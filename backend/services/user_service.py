from utils.db_utils import db
def get_all_sys_users():
    """
    获取所有用户列表
    :return: 数据库查询结果 (list of dict) 或 None
    """
    # 1. 写 SQL 
    sql = "SELECT id, username, role, created_at, updated_at FROM sys_user"
    
    # 2. 查数据库
    try:
        data = db.fetch_all(sql)
        return data
    except Exception as e:
        print(f"Service Error: {e}")
        return None