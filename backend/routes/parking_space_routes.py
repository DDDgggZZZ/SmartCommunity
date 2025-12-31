from flask import Blueprint, jsonify, request
from services.parking_space_service import (
    get_all_spaces,
    get_space_by_id,
    create_space,
    update_space,
    delete_space
)

parking_bp = Blueprint("parking_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def valid_status(s):
    return s in ["闲置", "已租", "已售"]

@parking_bp.route("/", methods=["GET"])
def get_spaces_api():
    status = request.args.get("status", default=None, type=str)
    if status is not None and not valid_status(status):
        return fail("Invalid Status", 400, [])
    data = get_all_spaces(status)
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@parking_bp.route("/<int:space_id>", methods=["GET"])
def get_space_detail_api(space_id):
    data = get_space_by_id(space_id)
    if not data:
        return fail("Space Not Found", 404, {})
    return ok(data)

@parking_bp.route("/", methods=["POST"])
def create_space_api():
    body = request.get_json() or {}
    space_no = body.get("space_no")
    status = body.get("status")

    if not space_no:
        return fail("space_no is required", 400, {})

    if status is not None and not valid_status(status):
        return fail("Invalid Status", 400, {})

    res = create_space(space_no, status)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@parking_bp.route("/<int:space_id>", methods=["PUT"])
def update_space_api(space_id):
    body = request.get_json() or {}
    space_no = body.get("space_no")
    status = body.get("status")

    if not space_no or status is None:
        return fail("space_no and status are required", 400, {})

    if not valid_status(status):
        return fail("Invalid Status", 400, {})

    old = get_space_by_id(space_id)
    if not old:
        return fail("Space Not Found", 404, {})

    res = update_space(space_id, space_no, status)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@parking_bp.route("/<int:space_id>", methods=["DELETE"])
def delete_space_api(space_id):
    old = get_space_by_id(space_id)
    if not old:
        return fail("Space Not Found", 404, {})

    res = delete_space(space_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
