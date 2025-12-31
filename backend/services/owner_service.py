from utils.db_utils import db

def get_all_owners():
    sql = """
        SELECT id, name, phone, id_card, move_in_date, created_at, updated_at
        FROM owner_info
        ORDER BY id ASC
    """
    try:
        return db.fetch_all(sql)
    except Exception as e:
        print(f"[get_all_owners] Error: {e}")
        return None

def get_owner_by_id(owner_id):
    sql = """
        SELECT id, name, phone, id_card, move_in_date, created_at, updated_at
        FROM owner_info
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (owner_id,))
    except Exception as e:
        print(f"[get_owner_by_id] Error: {e}")
        return None

def create_owner(name, phone, id_card, move_in_date):
    if move_in_date is None or move_in_date == "":
        sql = """
            INSERT INTO owner_info (name, phone, id_card)
            VALUES (%s, %s, %s)
        """
        args = (name, phone, id_card)
    else:
        sql = """
            INSERT INTO owner_info (name, phone, id_card, move_in_date)
            VALUES (%s, %s, %s, %s)
        """
        args = (name, phone, id_card, move_in_date)

    try:
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[create_owner] Error: {e}")
        return None

def update_owner(owner_id, name, phone, id_card, move_in_date):
    sql = """
        UPDATE owner_info
        SET name = %s,
            phone = %s,
            id_card = %s,
            move_in_date = %s
        WHERE id = %s
    """
    args = (name, phone, id_card, move_in_date, owner_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_owner] Error: {e}")
        return None

def delete_owner(owner_id):
    sql = "DELETE FROM owner_info WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (owner_id,))
        return db.execute_commit(sql, (owner_id,))
    except Exception as e:
        print(f"[delete_owner] Error: {e}")
        return None
