"""
init_data.py
作用：插入演示/联调数据（building/unit/room/owner/bill/repair/notice/parking）
前提：已执行 scripts/init.sql（表结构已存在）
用法：python scripts/init_data.py
"""

import pymysql
from config import Config


def get_conn():
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset=Config.DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def exec_sql(cursor, sql, params=None):
    cursor.execute(sql, params or ())


def main():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # 防重复：先清空（注意外键顺序：子表 -> 父表）
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for t in [
                "repair_request", "fee_bill", "parking_usage", "owner_room_rel",
                "owner_info", "community_room", "community_unit", "community_building",
                "parking_space", "sys_notice"
            ]:
                cur.execute(f"TRUNCATE TABLE {t};")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # 1) building/unit/room
            exec_sql(cur, "INSERT INTO community_building(building_no,total_floors,description) VALUES ('1栋',18,'1号楼');")
            exec_sql(cur, "INSERT INTO community_unit(building_id,unit_no) VALUES (1,'1单元'),(1,'2单元');")
            exec_sql(cur, """
                INSERT INTO community_room (unit_id, room_no, area, layout, status) VALUES
                (1, '301', 89.50, '2室1厅', '已售'),
                (1, '302', 92.00, '3室1厅', '已售'),
                (2, '501', 120.00, '3室2厅', '未售');
            """)

            # 2) owners
            exec_sql(cur, """
                INSERT INTO owner_info (name, phone, id_card, move_in_date) VALUES
                ('张三', '13800000001', '110101199001010011', '2024-01-01'),
                ('李四', '13800000002', '110101199202020022', '2024-06-01');
            """)

            # 3) owner-room relation
            exec_sql(cur, """
                INSERT INTO owner_room_rel (owner_id, room_id, rel_type) VALUES
                (1, 1, '户主'),
                (2, 2, '户主');
            """)

            # 4) parking
            exec_sql(cur, """
                INSERT INTO parking_space (space_no, status) VALUES
                ('A-001', '闲置'),
                ('A-002', '已租');
            """)
            exec_sql(cur, """
                INSERT INTO parking_usage (space_id, owner_id, plate_no, expire_date) VALUES
                (2, 1, '京A12345', '2026-12-31');
            """)

            # 5) notice
            exec_sql(cur, """
                INSERT INTO sys_notice (title, content) VALUES
                ('欢迎入住智慧社区', '本系统用于管理房屋、业主、缴费、报修等业务。');
            """)

            # 6) bills
            exec_sql(cur, """
                INSERT INTO fee_bill (owner_id, fee_type_id, amount, bill_month, status) VALUES
                (1, 1, 223.75, '2025-12', '未缴'),
                (1, 3, 300.00, '2025-12', '已缴'),
                (2, 1, 230.00, '2025-12', '未缴');
            """)

            # 7) repairs
            exec_sql(cur, """
                INSERT INTO repair_request (owner_id, content, status) VALUES
                (1, '厨房水龙头漏水', '待处理'),
                (2, '客厅灯不亮', '处理中');
            """)

        print("✅ init_data.py 执行完成：已插入演示/联调数据")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
