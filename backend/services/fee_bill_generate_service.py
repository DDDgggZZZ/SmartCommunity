from utils.db_utils import db

def fee_type_exists(fee_type_id):
    sql = "SELECT id, unit_price FROM fee_type WHERE id = %s"
    try:
        return db.fetch_one(sql, (fee_type_id,))
    except Exception as e:
        print(f"[fee_type_exists] Error: {e}")
        return None

def get_all_owner_ids():
    sql = "SELECT id FROM owner_info ORDER BY id ASC"
    try:
        rows = db.fetch_all(sql)
        if not rows:
            return []
        return [r["id"] for r in rows]
    except Exception as e:
        print(f"[get_all_owner_ids] Error: {e}")
        return None

def bill_exists(owner_id, fee_type_id, bill_month):
    sql = """
        SELECT id
        FROM fee_bill
        WHERE owner_id = %s AND fee_type_id = %s AND bill_month = %s
    """
    try:
        return db.fetch_one(sql, (owner_id, fee_type_id, bill_month))
    except Exception as e:
        print(f"[bill_exists] Error: {e}")
        return None

def insert_bill(owner_id, fee_type_id, amount, bill_month):
    sql = """
        INSERT INTO fee_bill (owner_id, fee_type_id, amount, bill_month)
        VALUES (%s, %s, %s, %s)
    """
    try:
        return db.execute_commit(sql, (owner_id, fee_type_id, amount, bill_month))
    except Exception as e:
        print(f"[insert_bill] Error: {e}")
        return None

def generate_bills_for_month(fee_type_id, bill_month):
    ft = fee_type_exists(fee_type_id)
    if not ft:
        return None

    unit_price = ft["unit_price"]

    owners = get_all_owner_ids()
    if owners is None:
        return None

    created = 0
    skipped = 0

    for owner_id in owners:
        ex = bill_exists(owner_id, fee_type_id, bill_month)
        if ex:
            skipped += 1
            continue
        res = insert_bill(owner_id, fee_type_id, unit_price, bill_month)
        if res is None:
            return None
        created += 1

    return {"created": created, "skipped": skipped}
