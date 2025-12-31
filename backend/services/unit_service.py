from utils.db_utils import db

def building_exists(building_id):
    sql = "SELECT id FROM community_building WHERE id = %s"
    try:
        return db.fetch_one(sql, (building_id,))
    except Exception as e:
        print(f"[building_exists] Error: {e}")
        return None

def get_all_units(building_id=None):
    if building_id is None:
        sql = """
            SELECT id, building_id, unit_no, created_at, updated_at
            FROM community_unit
            ORDER BY id ASC
        """
        args = None
    else:
        sql = """
            SELECT id, building_id, unit_no, created_at, updated_at
            FROM community_unit
            WHERE building_id = %s
            ORDER BY id ASC
        """
        args = (building_id,)

    try:
        return db.fetch_all(sql, args)
    except Exception as e:
        print(f"[get_all_units] Error: {e}")
        return None

def get_unit_by_id(unit_id):
    sql = """
        SELECT id, building_id, unit_no, created_at, updated_at
        FROM community_unit
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (unit_id,))
    except Exception as e:
        print(f"[get_unit_by_id] Error: {e}")
        return None

def create_unit(building_id, unit_no):
    sql = """
        INSERT INTO community_unit (building_id, unit_no)
        VALUES (%s, %s)
    """
    try:
        return db.execute_commit(sql, (building_id, unit_no))
    except Exception as e:
        print(f"[create_unit] Error: {e}")
        return None

def update_unit(unit_id, building_id, unit_no):
    sql = """
        UPDATE community_unit
        SET building_id = %s,
            unit_no = %s
        WHERE id = %s
    """
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (building_id, unit_no, unit_id))
        return db.execute_commit(sql, (building_id, unit_no, unit_id))
    except Exception as e:
        print(f"[update_unit] Error: {e}")
        return None

def delete_unit(unit_id):
    sql = "DELETE FROM community_unit WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (unit_id,))
        return db.execute_commit(sql, (unit_id,))
    except Exception as e:
        print(f"[delete_unit] Error: {e}")
        return None
