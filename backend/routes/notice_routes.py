from flask import Blueprint, jsonify, request
from services.notice_service import (
    get_all_notices,
    get_notice_by_id,
    create_notice,
    update_notice,
    delete_notice
)
from datetime import datetime, date

notice_bp = Blueprint("notice_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def format_item_dates(item):
    """辅助函数：将字典中的日期对象转为标准字符串"""
    if not item:
        return item
    for k, v in item.items():
        if isinstance(v, (datetime, date)):
            item[k] = v.strftime('%Y-%m-%d %H:%M:%S')
    return item

@notice_bp.route("/", methods=["GET"])
def get_notices_api():
    data = get_all_notices()
    if data is None:
        return fail("Database Error", 500, [])
    
    # ★ 修复关键：将所有日期字段转为字符串，防止前端日期控件或MySQL回写报错
    formatted_data = [format_item_dates(row) for row in data]
    
    return ok(formatted_data)

@notice_bp.route("/<int:notice_id>", methods=["GET"])
def get_notice_detail_api(notice_id):
    data = get_notice_by_id(notice_id)
    if not data:
        return fail("Notice Not Found", 404, {})
    return ok(format_item_dates(data))

@notice_bp.route("/", methods=["POST"])
def create_notice_api():
    body = request.get_json() or {}
    title = body.get("title")
    content = body.get("content")
    publish_time = body.get("publish_time")

    if not title or not content:
        return fail("title and content are required", 400, {})

    res = create_notice(title, content, publish_time)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@notice_bp.route("/<int:notice_id>", methods=["PUT"])
def update_notice_api(notice_id):
    body = request.get_json() or {}
    title = body.get("title")
    content = body.get("content")
    publish_time = body.get("publish_time")

    if not title or not content:
        return fail("title and content are required", 400, {})

    old = get_notice_by_id(notice_id)
    if not old:
        return fail("Notice Not Found", 404, {})

    # 如果前端传了空值（例如用户清空了时间），则保持原值
    if not publish_time:
        publish_time = old.get("publish_time")
        # 如果从数据库取出来是 datetime 对象，转为字符串
        if isinstance(publish_time, (datetime, date)):
             publish_time = publish_time.strftime('%Y-%m-%d %H:%M:%S')

    res = update_notice(notice_id, title, content, publish_time)
    
    # update操作返回影响行数，可能是0（未修改）或1，只要不是None就是成功
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@notice_bp.route("/<int:notice_id>", methods=["DELETE"])
def delete_notice_api(notice_id):
    old = get_notice_by_id(notice_id)
    if not old:
        return fail("Notice Not Found", 404, {})

    res = delete_notice(notice_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")