from flask import Blueprint, jsonify, request
from services.owner_service import (
    get_all_owners,
    get_owner_by_id,
    create_owner,
    update_owner,
    delete_owner
)

owner_bp = Blueprint("owner_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@owner_bp.route("/", methods=["GET"])
def get_owners_api():
    data = get_all_owners()
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@owner_bp.route("/<int:owner_id>", methods=["GET"])
def get_owner_detail_api(owner_id):
    data = get_owner_by_id(owner_id)
    if not data:
        return fail("Owner Not Found", 404, {})
    return ok(data)

@owner_bp.route("/", methods=["POST"])
def create_owner_api():
    body = request.get_json() or {}
    name = body.get("name")
    phone = body.get("phone")
    id_card = body.get("id_card")
    move_in_date = body.get("move_in_date")

    if not name or not phone or not id_card:
        return fail("name, phone, id_card are required", 400, {})

    res = create_owner(name, phone, id_card, move_in_date)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@owner_bp.route("/<int:owner_id>", methods=["PUT"])
def update_owner_api(owner_id):
    body = request.get_json() or {}
    name = body.get("name")
    phone = body.get("phone")
    id_card = body.get("id_card")
    move_in_date = body.get("move_in_date")

    if not name or not phone or not id_card:
        return fail("name, phone, id_card are required", 400, {})

    old = get_owner_by_id(owner_id)
    if not old:
        return fail("Owner Not Found", 404, {})

    if move_in_date is None or move_in_date == "":
        move_in_date = None

    res = update_owner(owner_id, name, phone, id_card, move_in_date)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@owner_bp.route("/<int:owner_id>", methods=["DELETE"])
def delete_owner_api(owner_id):
    old = get_owner_by_id(owner_id)
    if not old:
        return fail("Owner Not Found", 404, {})

    res = delete_owner(owner_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
