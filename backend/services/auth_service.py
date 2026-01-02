from utils.db_utils import db

def login(username, password):
    sql = """
        SELECT id, username, role
        FROM sys_user
        WHERE username = %s AND password = %s
    """
    try:
        return db.fetch_one(sql, (username, password))
    except Exception as e:
        print(f"[login] Error: {e}")
        return None

def get_all_users():
    sql = """
        SELECT id, username, role, created_at, updated_at
        FROM sys_user
        ORDER BY id ASC
    """
    try:
        return db.fetch_all(sql)
    except Exception as e:
        print(f"[get_all_users] Error: {e}")
        return None

def get_user_by_id(user_id):
    sql = """
        SELECT id, username, role, created_at, updated_at
        FROM sys_user
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (user_id,))
    except Exception as e:
        print(f"[get_user_by_id] Error: {e}")
        return None

def create_user(username, password, role):
    sql = """
        INSERT INTO sys_user (username, password, role)
        VALUES (%s, %s, %s)
    """
    try:
        return db.execute_commit(sql, (username, password, role))
    except Exception as e:
        print(f"[create_user] Error: {e}")
        return None

def update_user(user_id, password, role):
    sql = """
        UPDATE sys_user
        SET password = %s,
            role = %s
        WHERE id = %s
    """
    args = (password, role, user_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_user] Error: {e}")
        return None

def delete_user(user_id):
    sql = "DELETE FROM sys_user WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (user_id,))
        return db.execute_commit(sql, (user_id,))
    except Exception as e:
        print(f"[delete_user] Error: {e}")
        return None
