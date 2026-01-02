from utils.db_utils import db

def get_all_fee_bills(owner_id=None, status=None, bill_month=None):
    base_sql = """
        SELECT
            b.id,
            b.owner_id,
            o.name AS owner_name,
            o.phone AS owner_phone,
            b.fee_type_id,
            t.name AS fee_type_name,
            b.amount,
            b.bill_month,
            b.status,
            b.pay_time,
            b.created_at,
            b.updated_at
        FROM fee_bill b
        JOIN owner_info o ON b.owner_id = o.id
        JOIN fee_type t ON b.fee_type_id = t.id
    """

    where = []
    args = []

    if owner_id is not None:
        where.append("b.owner_id = %s")
        args.append(owner_id)

    if status is not None:
        where.append("b.status = %s")
        args.append(status)

    if bill_month is not None:
        where.append("b.bill_month = %s")
        args.append(bill_month)

    if where:
        base_sql += " WHERE " + " AND ".join(where)

    base_sql += " ORDER BY b.id ASC"

    try:
        return db.fetch_all(base_sql, tuple(args) if args else None)
    except Exception as e:
        print(f"[get_all_fee_bills] Error: {e}")
        return None

def get_fee_bill_by_id(bill_id):
    sql = """
        SELECT
            b.id,
            b.owner_id,
            o.name AS owner_name,
            o.phone AS owner_phone,
            b.fee_type_id,
            t.name AS fee_type_name,
            b.amount,
            b.bill_month,
            b.status,
            b.pay_time,
            b.created_at,
            b.updated_at
        FROM fee_bill b
        JOIN owner_info o ON b.owner_id = o.id
        JOIN fee_type t ON b.fee_type_id = t.id
        WHERE b.id = %s
    """
    try:
        return db.fetch_one(sql, (bill_id,))
    except Exception as e:
        print(f"[get_fee_bill_by_id] Error: {e}")
        return None
