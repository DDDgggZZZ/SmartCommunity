from utils.db_utils import db

def get_all_notices():
    sql = """
        SELECT id, title, content, publish_time, created_at, updated_at
        FROM sys_notice
        ORDER BY publish_time DESC, id DESC
    """
    try:
        return db.fetch_all(sql)
    except Exception as e:
        print(f"[get_all_notices] Error: {e}")
        return None

def get_notice_by_id(notice_id):
    sql = """
        SELECT id, title, content, publish_time, created_at, updated_at
        FROM sys_notice
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (notice_id,))
    except Exception as e:
        print(f"[get_notice_by_id] Error: {e}")
        return None

def create_notice(title, content, publish_time=None):
    if publish_time is None or publish_time == "":
        sql = """
            INSERT INTO sys_notice (title, content)
            VALUES (%s, %s)
        """
        args = (title, content)
    else:
        sql = """
            INSERT INTO sys_notice (title, content, publish_time)
            VALUES (%s, %s, %s)
        """
        args = (title, content, publish_time)

    try:
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[create_notice] Error: {e}")
        return None

def update_notice(notice_id, title, content, publish_time=None):
    sql = """
        UPDATE sys_notice
        SET title = %s,
            content = %s,
            publish_time = %s
        WHERE id = %s
    """
    args = (title, content, publish_time, notice_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_notice] Error: {e}")
        return None

def delete_notice(notice_id):
    sql = "DELETE FROM sys_notice WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (notice_id,))
        return db.execute_commit(sql, (notice_id,))
    except Exception as e:
        print(f"[delete_notice] Error: {e}")
        return None
