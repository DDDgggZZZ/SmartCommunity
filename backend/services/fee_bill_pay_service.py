from utils.db_utils import db

def get_bill_by_id(bill_id):
    sql = "SELECT id, status FROM fee_bill WHERE id = %s"
    try:
        return db.fetch_one(sql, (bill_id,))
    except Exception as e:
        print(f"[get_bill_by_id] Error: {e}")
        return None

def pay_bill_now(bill_id):
    sql = """
        UPDATE fee_bill
        SET status = '已缴',
            pay_time = NOW()
        WHERE id = %s AND status = '未缴'
    """
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (bill_id,))
        return db.execute_commit(sql, (bill_id,))
    except Exception as e:
        print(f"[pay_bill_now] Error: {e}")
        return None

def pay_bill_with_time(bill_id, pay_time):
    sql = """
        UPDATE fee_bill
        SET status = '已缴',
            pay_time = %s
        WHERE id = %s AND status = '未缴'
    """
    try:
        if hasattr(db, "execute"):
            return db.execute(sql, (pay_time, bill_id))
        return db.execute_commit(sql, (pay_time, bill_id))
    except Exception as e:
        print(f"[pay_bill_with_time] Error: {e}")
        return None
