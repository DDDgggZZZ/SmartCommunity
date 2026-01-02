from utils.db_utils import db

def get_repair_basic(repair_id):
    sql = "SELECT id, status FROM repair_request WHERE id = %s"
    try:
        return db.fetch_one(sql, (repair_id,))
    except Exception as e:
        print(f"[get_repair_basic] Error: {e}")
        return None

def update_repair_status(repair_id, status, feedback):
    sql = """
        UPDATE repair_request
        SET status = %s,
            feedback = %s
        WHERE id = %s
    """
    args = (status, feedback, repair_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_repair_status] Error: {e}")
        return None
