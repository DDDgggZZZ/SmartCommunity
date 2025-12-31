from flask import Blueprint, jsonify, request
from services.owner_room_rel_service import (
    owner_exists,
    room_exists,
    get_all_bindings,
    get_binding_by_id,
    create_binding,
    update_binding,
    delete_binding
)

binding_bp = Blueprint("binding_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def valid_rel_type(s):
    return s in ["户主", "租客"]

@binding_bp.route("/", methods=["GET"])
def get_bindings_api():
    owner_id = request.args.get("owner_id", default=None, type=int)
    room_id = request.args.get("room_id", default=None, type=int)
    data = get_all_bindings(owner_id, room_id)
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@binding_bp.route("/<int:binding_id>", methods=["GET"])
def get_binding_detail_api(binding_id):
    data = get_binding_by_id(binding_id)
    if not data:
        return fail("Binding Not Found", 404, {})
    return ok(data)

@binding_bp.route("/", methods=["POST"])
def create_binding_api():
    body = request.get_json() or {}
    owner_id = body.get("owner_id")
    room_id = body.get("room_id")
    rel_type = body.get("rel_type")

    if owner_id is None or room_id is None or rel_type is None:
        return fail("owner_id, room_id, rel_type are required", 400, {})

    if not valid_rel_type(rel_type):
        return fail("Invalid rel_type", 400, {})

    ex1 = owner_exists(owner_id)
    if not ex1:
        return fail("Owner Not Found", 404, {})

    ex2 = room_exists(room_id)
    if not ex2:
        return fail("Room Not Found", 404, {})

    res = create_binding(owner_id, room_id, rel_type)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@binding_bp.route("/<int:binding_id>", methods=["PUT"])
def update_binding_api(binding_id):
    body = request.get_json() or {}
    rel_type = body.get("rel_type")

    if rel_type is None:
        return fail("rel_type is required", 400, {})

    if not valid_rel_type(rel_type):
        return fail("Invalid rel_type", 400, {})

    old = get_binding_by_id(binding_id)
    if not old:
        return fail("Binding Not Found", 404, {})

    res = update_binding(binding_id, rel_type)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@binding_bp.route("/<int:binding_id>", methods=["DELETE"])
def delete_binding_api(binding_id):
    old = get_binding_by_id(binding_id)
    if not old:
        return fail("Binding Not Found", 404, {})

    res = delete_binding(binding_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
