from utils.db_utils import db

# 1) 获取楼栋列表
def get_all_buildings():
    sql = """
        SELECT id, building_no, total_floors, description, created_at, updated_at
        FROM community_building
        ORDER BY id ASC
    """
    try:
        return db.fetch_all(sql)
    except Exception as e:
        print(f"[get_all_buildings] Error: {e}")
        return None


# 2) 获取楼栋详情
def get_building_by_id(building_id):
    sql = """
        SELECT id, building_no, total_floors, description, created_at, updated_at
        FROM community_building
        WHERE id = %s
    """
    try:
        return db.fetch_one(sql, (building_id,))
    except Exception as e:
        print(f"[get_building_by_id] Error: {e}")
        return None


# 3) 新增楼栋
def create_building(building_no, total_floors, description):
    sql = """
        INSERT INTO community_building (building_no, total_floors, description)
        VALUES (%s, %s, %s)
    """
    try:
        return db.execute_commit(sql, (building_no, total_floors, description))
    except Exception as e:
        print(f"[create_building] Error: {e}")
        return None


# 4) 更新楼栋
def update_building(building_id, building_no, total_floors, description):
    sql = """
        UPDATE community_building
        SET building_no = %s,
            total_floors = %s,
            description = %s
        WHERE id = %s
    """
    try:
        return db.execute(sql, (building_no, total_floors, description, building_id))
    except Exception as e:
        print(f"[update_building] Error: {e}")
        return None


# 5) 删除楼栋
def delete_building(building_id):
    sql = "DELETE FROM community_building WHERE id = %s"
    try:
        return db.execute(sql, (building_id,))
    except Exception as e:
        print(f"[delete_building] Error: {e}")
        return None
