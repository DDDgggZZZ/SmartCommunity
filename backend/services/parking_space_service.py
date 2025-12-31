from utils.db_utils import db

def get_all_spaces(status=None):
    if status is None:
        sql = """
            SELECT id, space_no, status, created_at, updated_at
            FROM parking_space
            ORDER BY id ASC
        """
        args = None
    else:
        sql = """
            SELECT id, space_no, status, created_at, updated_at
            FROM parking_space
            WHERE status = %s
            ORDER BY id ASC
        """
        args = (status,)

    try:
        return db.fetch_all(sql, args)
    except Exception as e:
        print(f"[get_all_spaces] Error: {e}")
        return None

def get_space_by_id(space_id):
    sql = """
        SELECT id, space_no, status, created_at, updated_at
        FROM parking_space
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (space_id,))
    except Exception as e:
        print(f"[get_space_by_id] Error: {e}")
        return None

def create_space(space_no, status=None):
    if status is None:
        sql = """
            INSERT INTO parking_space (space_no)
            VALUES (%s)
        """
        args = (space_no,)
    else:
        sql = """
            INSERT INTO parking_space (space_no, status)
            VALUES (%s, %s)
        """
        args = (space_no, status)

    try:
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[create_space] Error: {e}")
        return None

def update_space(space_id, space_no, status):
    sql = """
        UPDATE parking_space
        SET space_no = %s,
            status = %s
        WHERE id = %s
    """
    args = (space_no, status, space_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_space] Error: {e}")
        return None

def delete_space(space_id):
    sql = "DELETE FROM parking_space WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (space_id,))
        return db.execute_commit(sql, (space_id,))
    except Exception as e:
        print(f"[delete_space] Error: {e}")
        return None
