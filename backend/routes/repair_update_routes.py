from flask import Blueprint, jsonify, request
from services.repair_update_service import (
    get_repair_basic,
    update_repair_status
)

repair_update_bp = Blueprint("repair_update_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def valid_status(s):
    return s in ["待处理", "处理中", "完成"]

@repair_update_bp.route("/<int:repair_id>/status", methods=["PUT"])
def update_repair_status_api(repair_id):
    old = get_repair_basic(repair_id)
    if not old:
        return fail("Repair Not Found", 404, {})

    body = request.get_json() or {}
    status = body.get("status")
    feedback = body.get("feedback")

    if not status:
        return fail("status is required", 400, {})

    if not valid_status(status):
        return fail("Invalid Status", 400, {})

    if feedback is None:
        feedback = old.get("feedback")

    if status == "完成" and (feedback is None or feedback == ""):
        return fail("feedback is required when status is 完成", 400, {})

    res = update_repair_status(repair_id, status, feedback)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")
