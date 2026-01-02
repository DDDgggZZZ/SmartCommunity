from utils.db_utils import db

def owner_exists(owner_id):
    sql = "SELECT id FROM owner_info WHERE id = %s"
    try:
        return db.fetch_one(sql, (owner_id,))
    except Exception as e:
        print(f"[owner_exists] Error: {e}")
        return None

def create_repair(owner_id, content):
    sql = """
        INSERT INTO repair_request (owner_id, content)
        VALUES (%s, %s)
    """
    try:
        return db.execute_commit(sql, (owner_id, content))
    except Exception as e:
        print(f"[create_repair] Error: {e}")
        return None
