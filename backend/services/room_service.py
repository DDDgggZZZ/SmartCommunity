from utils.db_utils import db

def unit_exists(unit_id):
    sql = "SELECT id FROM community_unit WHERE id = %s"
    try:
        return db.fetch_one(sql, (unit_id,))
    except Exception as e:
        print(f"[unit_exists] Error: {e}")
        return None

from utils.db_utils import db

def unit_in_building(building_id, unit_id):
    sql = "SELECT id FROM community_unit WHERE id = %s AND building_id = %s"
    try:
        return db.fetch_one(sql, (unit_id, building_id))
    except Exception as e:
        print(f"[unit_in_building] Error: {e}")
        return None

def get_all_rooms(building_id=None, unit_id=None):
    if building_id is None and unit_id is None:
        sql = """
            SELECT id, unit_id, room_no, area, layout, status, created_at, updated_at
            FROM community_room
            ORDER BY id ASC
        """
        args = None
    elif building_id is None and unit_id is not None:
        sql = """
            SELECT id, unit_id, room_no, area, layout, status, created_at, updated_at
            FROM community_room
            WHERE unit_id = %s
            ORDER BY id ASC
        """
        args = (unit_id,)
    elif building_id is not None and unit_id is None:
        sql = """
            SELECT r.id, r.unit_id, r.room_no, r.area, r.layout, r.status, r.created_at, r.updated_at
            FROM community_room r
            JOIN community_unit u ON r.unit_id = u.id
            WHERE u.building_id = %s
            ORDER BY r.id ASC
        """
        args = (building_id,)
    else:
        sql = """
            SELECT r.id, r.unit_id, r.room_no, r.area, r.layout, r.status, r.created_at, r.updated_at
            FROM community_room r
            JOIN community_unit u ON r.unit_id = u.id
            WHERE u.building_id = %s AND r.unit_id = %s
            ORDER BY r.id ASC
        """
        args = (building_id, unit_id)

    try:
        return db.fetch_all(sql, args)
    except Exception as e:
        print(f"[get_all_rooms] Error: {e}")
        return None

    if unit_id is None:
        sql = """
            SELECT id, unit_id, room_no, area, layout, status, created_at, updated_at
            FROM community_room
            ORDER BY id ASC
        """
        args = None
    else:
        sql = """
            SELECT id, unit_id, room_no, area, layout, status, created_at, updated_at
            FROM community_room
            WHERE unit_id = %s
            ORDER BY id ASC
        """
        args = (unit_id,)

    try:
        return db.fetch_all(sql, args)
    except Exception as e:
        print(f"[get_all_rooms] Error: {e}")
        return None

def get_room_by_id(room_id):
    sql = """
        SELECT id, unit_id, room_no, area, layout, status, created_at, updated_at
        FROM community_room
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (room_id,))
    except Exception as e:
        print(f"[get_room_by_id] Error: {e}")
        return None

def create_room(unit_id, room_no, area, layout, status):
    if status is None:
        sql = """
            INSERT INTO community_room (unit_id, room_no, area, layout)
            VALUES (%s, %s, %s, %s)
        """
        args = (unit_id, room_no, area, layout)
    else:
        sql = """
            INSERT INTO community_room (unit_id, room_no, area, layout, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        args = (unit_id, room_no, area, layout, status)

    try:
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[create_room] Error: {e}")
        return None

def update_room(room_id, unit_id, room_no, area, layout, status):
    sql = """
        UPDATE community_room
        SET unit_id = %s,
            room_no = %s,
            area = %s,
            layout = %s,
            status = %s
        WHERE id = %s
    """
    args = (unit_id, room_no, area, layout, status, room_id)
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, args)
        return db.execute_commit(sql, args)
    except Exception as e:
        print(f"[update_room] Error: {e}")
        return None

def delete_room(room_id):
    sql = "DELETE FROM community_room WHERE id = %s"
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (room_id,))
        return db.execute_commit(sql, (room_id,))
    except Exception as e:
        print(f"[delete_room] Error: {e}")
        return None
