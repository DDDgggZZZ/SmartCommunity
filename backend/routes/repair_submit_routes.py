from flask import Blueprint, jsonify, request
from services.repair_submit_service import (
    owner_exists,
    create_repair
)

repair_submit_bp = Blueprint("repair_submit_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@repair_submit_bp.route("/", methods=["POST"])
def submit_repair_api():
    body = request.get_json() or {}
    owner_id = body.get("owner_id")
    content = body.get("content")

    if owner_id is None or not content:
        return fail("owner_id and content are required", 400, {})

    try:
        owner_id = int(owner_id)
    except Exception:
        return fail("owner_id must be int", 400, {})

    ex = owner_exists(owner_id)
    if not ex:
        return fail("Owner Not Found", 404, {})

    res = create_repair(owner_id, content)
    if res is None:
        return fail("Submit Failed", 500, {})

    return ok({"inserted": res}, "created")
