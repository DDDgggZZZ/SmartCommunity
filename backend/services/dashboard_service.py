from utils.db_utils import db

def get_count(sql):
    try:
        row = db.fetch_one(sql)
        if not row:
            return 0
        return list(row.values())[0]
    except Exception as e:
        print(f"[get_count] Error: {e}")
        return None

def get_dashboard_stats():
    stats = {}

    stats["buildings"] = get_count("SELECT COUNT(*) AS c FROM community_building")
    stats["units"] = get_count("SELECT COUNT(*) AS c FROM community_unit")
    stats["rooms"] = get_count("SELECT COUNT(*) AS c FROM community_room")
    stats["owners"] = get_count("SELECT COUNT(*) AS c FROM owner_info")
    stats["parking_spaces"] = get_count("SELECT COUNT(*) AS c FROM parking_space")
    stats["fee_types"] = get_count("SELECT COUNT(*) AS c FROM fee_type")
    stats["bills_total"] = get_count("SELECT COUNT(*) AS c FROM fee_bill")
    stats["bills_unpaid"] = get_count("SELECT COUNT(*) AS c FROM fee_bill WHERE status = '未缴'")
    stats["repairs_total"] = get_count("SELECT COUNT(*) AS c FROM repair_request")
    stats["repairs_pending"] = get_count("SELECT COUNT(*) AS c FROM repair_request WHERE status = '待处理'")
    stats["notices"] = get_count("SELECT COUNT(*) AS c FROM sys_notice")
    stats["sys_users"] = get_count("SELECT COUNT(*) AS c FROM sys_user")

    if None in stats.values():
        return None

    return stats
