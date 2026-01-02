from utils.db_utils import db

def get_all_fee_types():
    sql = """
        SELECT id, name, unit_price, unit, created_at, updated_at
        FROM fee_type
        ORDER BY id ASC
    """
    try:
        return db.fetch_all(sql)
    except Exception as e:
        print(f"[get_all_fee_types] Error: {e}")
        return None

def get_fee_type_by_id(fee_type_id):
    sql = """
        SELECT id, name, unit_price, unit, created_at, updated_at
        FROM fee_type
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (fee_type_id,))
    except Exception as e:
        print(f"[get_fee_type_by_id] Error: {e}")
        return None

def create_fee_type(name, unit_price, unit):
    sql = """
        INSERT INTO fee_type (name, unit_price, unit)
        VALUES (%s, %s, %s)
    """
    try:
        return db.execute_commit(sql, (name, unit_price, unit))
    except Exception as e:
        print(f"[create_fee_type] Error: {e}")
        return None

def update_fee_type(fee_type_id, name, unit_price, unit):
    sql = """
        UPDATE fee_type
        SET name = %s,
            unit_price = %s,
            unit = %s
        WHERE id = %s
    """
    args = (name, unit_price, unit, fee_type_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_fee_type] Error: {e}")
        return None

def delete_fee_type(fee_type_id):
    sql = "DELETE FROM fee_type WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (fee_type_id,))
        return db.execute_commit(sql, (fee_type_id,))
    except Exception as e:
        print(f"[delete_fee_type] Error: {e}")
        return None
