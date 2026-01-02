from utils.db_utils import db

def get_all_repairs(owner_id=None, status=None):
    base_sql = """
        SELECT
            r.id,
            r.owner_id,
            o.name AS owner_name,
            o.phone AS owner_phone,
            r.content,
            r.submit_time,
            r.status,
            r.feedback,
            r.updated_at
        FROM repair_request r
        JOIN owner_info o ON r.owner_id = o.id
    """

    where = []
    args = []

    if owner_id is not None:
        where.append("r.owner_id = %s")
        args.append(owner_id)

    if status is not None:
        where.append("r.status = %s")
        args.append(status)

    if where:
        base_sql += " WHERE " + " AND ".join(where)

    base_sql += " ORDER BY r.id ASC"

    try:
        return db.fetch_all(base_sql, tuple(args) if args else None)
    except Exception as e:
        print(f"[get_all_repairs] Error: {e}")
        return None

def get_repair_by_id(repair_id):
    sql = """
        SELECT
            r.id,
            r.owner_id,
            o.name AS owner_name,
            o.phone AS owner_phone,
            r.content,
            r.submit_time,
            r.status,
            r.feedback,
            r.updated_at
        FROM repair_request r
        JOIN owner_info o ON r.owner_id = o.id
        WHERE r.id = %s
    """
    try:
        return db.fetch_one(sql, (repair_id,))
    except Exception as e:
        print(f"[get_repair_by_id] Error: {e}")
        return None
