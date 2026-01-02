from flask import Blueprint, jsonify, request
from services.notice_service import (
    get_all_notices,
    get_notice_by_id,
    create_notice,
    update_notice,
    delete_notice
)

notice_bp = Blueprint("notice_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@notice_bp.route("/", methods=["GET"])
def get_notices_api():
    data = get_all_notices()
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@notice_bp.route("/<int:notice_id>", methods=["GET"])
def get_notice_detail_api(notice_id):
    data = get_notice_by_id(notice_id)
    if not data:
        return fail("Notice Not Found", 404, {})
    return ok(data)

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

    if publish_time is None or publish_time == "":
        publish_time = old.get("publish_time")

    res = update_notice(notice_id, title, content, publish_time)
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
