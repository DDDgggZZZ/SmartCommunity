from utils.db_utils import db

def owner_exists(owner_id):
    sql = "SELECT id FROM owner_info WHERE id = %s"
    try:
        return db.fetch_one(sql, (owner_id,))
    except Exception as e:
        print(f"[owner_exists] Error: {e}")
        return None

def room_exists(room_id):
    sql = "SELECT id FROM community_room WHERE id = %s"
    try:
        return db.fetch_one(sql, (room_id,))
    except Exception as e:
        print(f"[room_exists] Error: {e}")
        return None

def get_all_bindings(owner_id=None, room_id=None):
    if owner_id is None and room_id is None:
        sql = """
            SELECT id, owner_id, room_id, rel_type, created_at, updated_at
            FROM owner_room_rel
            ORDER BY id ASC
        """
        args = None
    elif owner_id is not None and room_id is None:
        sql = """
            SELECT id, owner_id, room_id, rel_type, created_at, updated_at
            FROM owner_room_rel
            WHERE owner_id = %s
            ORDER BY id ASC
        """
        args = (owner_id,)
    elif owner_id is None and room_id is not None:
        sql = """
            SELECT id, owner_id, room_id, rel_type, created_at, updated_at
            FROM owner_room_rel
            WHERE room_id = %s
            ORDER BY id ASC
        """
        args = (room_id,)
    else:
        sql = """
            SELECT id, owner_id, room_id, rel_type, created_at, updated_at
            FROM owner_room_rel
            WHERE owner_id = %s AND room_id = %s
            ORDER BY id ASC
        """
        args = (owner_id, room_id)

    try:
        return db.fetch_all(sql, args)
    except Exception as e:
        print(f"[get_all_bindings] Error: {e}")
        return None

def get_binding_by_id(binding_id):
    sql = """
        SELECT id, owner_id, room_id, rel_type, created_at, updated_at
        FROM owner_room_rel
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (binding_id,))
    except Exception as e:
        print(f"[get_binding_by_id] Error: {e}")
        return None

def create_binding(owner_id, room_id, rel_type):
    sql = """
        INSERT INTO owner_room_rel (owner_id, room_id, rel_type)
        VALUES (%s, %s, %s)
    """
    try:
        return db.execute_commit(sql, (owner_id, room_id, rel_type))
    except Exception as e:
        print(f"[create_binding] Error: {e}")
        return None

def update_binding(binding_id, rel_type):
    sql = """
        UPDATE owner_room_rel
        SET rel_type = %s
        WHERE id = %s
    """
    args = (rel_type, binding_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_binding] Error: {e}")
        return None

def delete_binding(binding_id):
    sql = "DELETE FROM owner_room_rel WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (binding_id,))
        return db.execute_commit(sql, (binding_id,))
    except Exception as e:
        print(f"[delete_binding] Error: {e}")
        return None
